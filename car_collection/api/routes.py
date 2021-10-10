from flask import Blueprint, request, jsonify
from werkzeug.wrappers import response
from car_collection.helpers import token_required
from car_collection.models import db, User, Car, car_schema, cars_schema


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
@token_required
def get_data(current_user_token):
    return {'some': 'value'}

#Create car ENDPOINT


@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    car_model = request.json['car_model']
    car_make = request.json['car_make']
    max_speed = request.json['max_speed']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    cost_of_product = request.json['cost_of_product']
    series = request.json['series']
    user_token = current_user_token.token

    car = Car(name, description, price, car_model,  car_make,
                  max_speed, dimensions, weight, cost_of_product, series, user_token)
    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# RETRIEVE ALL carS ENDPOINT


@api.route('/cars', methods=['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token=owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# retrieve one car endpoint


@api.route('/cars/<id>', methods=['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

# UPDATE car ENDPOINT


@api.route('/cars/<id>', methods=['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)  # Get car Instance

    car.name = request.json['name']
    car.description = request.json['description']
    car.price = request.json['price']
    car.car_model = request.json['car_model']
    car.car_make = request.json['car_make']
    car.max_speed = request.json['max_speed']
    car.dimensions = request.json['dimensions']
    car.weight = request.json['weight']
    car.cost_of_product = request.json['cost_of_product']
    car.series = request.json['series']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)


# DELETE ENDPOINT

@api.route('/cars/<id>', methods=['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)
