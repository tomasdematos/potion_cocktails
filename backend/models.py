import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Potman(db.Model):
    __tablename__ = 'potmen'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    stores = db.relationship("Store")


class Store(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('potmen.id'))
    name = db.Column(db.String(50), nullable=False)
    fame = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    stokes = db.relationship("Stock")


class Stock(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    potion_id = db.Column(db.Integer, db.ForeignKey('potions.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())


class Potion(db.Model):
    __tablename__ = 'potions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
