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

# Table for reported issues
class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    resolved = db.Column(db.Boolean, default=False)
    issue = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=3)

#for merge

#Table for scooters
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
    expiry = db.Column(db.DateTime)
    price = db.Column(db.Integer, nullable = False)
    cancelled = db.Column(db.Boolean, default = False, nullable=False)
    
class Card(db.Model):
    __tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, ForeignKey("users.id"))
    name = db.Column(db.String, nullable = False)
    cardnum = db.Column(db.Integer, nullable = False)
    expiry = db.Column(db.DateTime, nullable = False)
    address1 = db.Column(db.String, nullable = False)
    address2 = db.Column(db.String)
    city = db.Column(db.String, nullable = False)
    postcode = db.Column(db.String, nullable = False)
    
class Price(db.Model):
    __tablename__ = "pricing"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable = False)