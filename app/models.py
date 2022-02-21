from app import db

#Table for users
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    username = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)


#Table for scooters
#class Scooter(db.Model):
#    __tablename__ = 'scooters'
#    id =