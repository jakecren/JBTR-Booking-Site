from bookingApp import db, login_manager
from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(60), nullable=False)
    surname = db.Column(db.String(60), nullable=True)
    email = db.Column(db.String(110), nullable=False, unique=True)
    mobile = db.Column(db.String(12), nullable=True, unique=True)
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Integer, nullable=False)

    vendor = db.relationship("Vendors")


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(60), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    mobile = db.Column(db.String(12), nullable=False)
    street = db.Column(db.String(60), nullable=False)
    suburb = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60))
    state = db.Column(db.String(60))
    postcode = db.Column(db.String(4))

    order = db.relationship("Orders")


class Vendors(db.Model): #Company info (company name, company email etc.)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=True, unique=True)
    mobile = db.Column(db.String(12), nullable=True, unique=True)
    userID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    products = db.relationship("Products")


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    description = db.Column(db.String(255))
    vendorID = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=True)
    price = db.Column(db.Float, nullable = False)

    orders = db.relationship("Orders")


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referenceNumber = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    productID = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(60), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    year = db.Column(db.Integer)
    email = db.Column(db.String(60), nullable=False)
    mobile = db.Column(db.String(12))
    type = db.Column(db.String(1), nullable=False)
