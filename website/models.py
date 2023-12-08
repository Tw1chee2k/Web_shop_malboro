from . import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import DateTime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    nickname = db.Column(db.String(150))
    
class Sklad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(150), unique=True)
    tovary = db.relationship('Tovar', backref='sklad', lazy=True)

class Tovar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    cost = db.Column(db.Float)
    status = db.Column(db.String(20), default = 'В наличии')
    type_of_decoration = db.Column(db.String(40))
    material = db.Column(db.String(20)) 
    opisanie = db.Column(db.String(500))
    sklad_id = db.Column(db.Integer, db.ForeignKey('sklad.id'), nullable=False)
    
class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(150), db.ForeignKey('user.email'), nullable=False)
    tovar_name = db.Column(db.String(150), db.ForeignKey('tovar.name'), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float, default = 0)
    size = db.Column(db.Integer)
        
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomerzakaza = db.Column(db.Integer)
    email = db.Column(db.String(150), db.ForeignKey('user.email'), nullable=False)
    telephone = db.Column(db.Integer)
    city = db.Column(db.String(20))
    fio = db.Column(db.String(50))
    adress = db.Column(db.String(100))
    coment = db.Column(db.String(200))
    promocod = db.Column(db.String(10))
    obsh_price = db.Column(db.Integer)
    tovar_name = db.Column(db.String(150), db.ForeignKey('tovar.name'), nullable=False)
    tovar_quantity = db.Column(db.Integer, default = 0)
    tovar_size = db.Column(db.Integer, default = 0)
    status = db.Column(db.String(20), default = 'На складе')
    created_at = db.Column(DateTime, default=datetime.now())
    