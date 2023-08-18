from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api', __name__, url_prefix='/api')

# Create car route
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    year = request.json['year']
    make = request.json['make']
    model = request.json['model']
    color = request.json['color']
    mileage = request.json['mileage']
    user_token = current_user_token.token

    print(f'Car Maker: {user_token}')

    car = Car(name, year, make, model, color, mileage, user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# Route to get all cars in inventory
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    the_user = current_user_token.token
    cars = Car.query.filter_by(user_token = the_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# Route to get single car in inventory
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

# Update car route
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.name = request.json['name']
    car.year = request.json['year']
    car.make = request.json['make']
    car.model = request.json['model']
    car.color = request.json['color']
    car.mileage = request.json['mileage']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# Delete car route
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)