from . import db
from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy.types import  Enum
import enum


#db = database.AlchemyDB()
#db = database.AlchemyDB()
#db = SQLAlchemy()
class SexType(enum.Enum):
    m = 'male'
    f = 'female'



class Registration(db.Model):
    __tablename__ = 'register'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = True)
    age = db.Column(db.Integer, nullable = True)
    sex = db.Column(db.Enum(['male', 'female']), nullable = False)
    cardetail = db.Column(db.String(15))
    license_detail = db.Column(db.String(20))
    mobile = db.Column(db.Integer, nullable = True, unique = True)
    email = db.Column(db.String(20), nullable = True, unique = True)
    address = db.Column(db.String(30), nullable = True)
    registeredas = db.Column(db.Enum(['passenger', 'carowner/passenger']), nullable = False)
    loginid = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(20) )
    referalid = db.Column(db.Integer, db.ForeignKey('register.id'))

class Liftavailable(db.Model):
    __tablename__ = 'liftavailable'
    uid = db.Column(db.Integer, primary_key = True)
    id = db.Column(db.Integer, db.ForeignKey('register.id'))
    startlocation = db.Column(db.String(64), nullable = False)
    destination = db.Column(db.String(64), nullable = False)
    startdate = db.Column(db.DateTime)
    seatavailable = db.Column(db.Integer, nullable = False)
    totalseats = db.Column(db.Integer, nullable = False)

class Liftrequired(db.Model):
    __tablename__ = 'liftrequired'
    uid = db.Column(db.Integer, primary_key = True)
    id = db.Column(db.Integer, db.ForeignKey('register.id'))
    startlocation = db.Column(db.String(64), nullable = False)
    destination = db.Column(db.String(64), nullable = False)
    startdate = db.Column(db.DateTime)

class Travelrecord(db.Model):
    __tablename__ = 'travelrecord'
    travel_id = db.Column(db.Integer, primary_key = True)
    ownerid = db.Column(db.Integer, db.ForeignKey('register.id'))
    passengerid = db.Column(db.Integer, db.ForeignKey('register.id'))
    distancetravelled = db.Column(db.Float, nullable = False)
    g_pointsearnedbyowner = db.Column(db.Integer, nullable = False)
    g_pointsusedbypassenger = db.Column(db.Integer, nullable = False)
    refralpoints = db.Column(db.Integer)
