from datetime import date
from sqlalchemy import ForeignKey, false
from app import db

#Table for users
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    username = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)


#Table for scooter
class Scooter(db.Model):
    __tablename__ = 'scooters'
    id = db.Column(db.Integer, primary_key=True)
    in_use = db.Column(db.Boolean, default = False)
    LocationID = db.Column(db.Integer, ForeignKey("locations.id"))


#Table for locations
class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)


#Table for orders/bookings
class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    ScooterID = db.Column(db.Integer, ForeignKey("scooters.id"))
    UserID = db.Column(db.Integer, ForeignKey("users.id"))
    numHours = db.Column(db.Integer, nullable = False)
    date = db.Column(db.DateTime, nullable = False)
    price = db.Column(db.Integer, nullable = False)