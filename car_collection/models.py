from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from sqlalchemy.orm import backref

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import Secrets module (Givenby Python)
import secrets

#Imports for Login Manager
from flask_login import UserMixin, login_manager

#Imports for Flask Login
from flask_login import LoginManager

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String(150), primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    car = db.relationship('Car', backref='owner', lazy=True)

    def __init__(self, email, first_name='', last_name='', id='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database.'


class Car(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Numeric(precision=10, scale=2))
    car_model = db.Column(db.String(150), nullable=True)
    car_make = db.Column(db.String(100), nullable=True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    cost_of_product = db.Column(db.Numeric(precision=10, scale=2))
    series = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, name, description, price, car_model, car_make, max_speed, dimensions, weight, cost_of_product, series, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.car_model = car_model
        self.car_make = car_make
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_product = cost_of_product
        self.series = series
        self.user_token = user_token

    def __repr__(self):
        return f'The following car has been added: {self.name}'

    def set_id(self):
        return secrets.token_urlsafe()

# Creation of API Schema via the Marshmallow Object


class carSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'price', 'car_model', 'car_make','max_speed', 'dimensions', 'weight', 'cost_of_product', ' series']


car_schema = carSchema()

cars_schema = carSchema(many=True)
