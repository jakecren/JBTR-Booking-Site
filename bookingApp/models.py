from bookingApp import db, login_manager
from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    forename = db.Column(db.String(60), nullable=False)
    surname = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(110), nullable=False, unique=True)
    mobile = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Integer, nullable=False)

    vendor = db.relationship("Vendors")

    
    def __repr__(self):
        return f"User: {self.forename} {self.surname} ({self.email}, {self.mobile}, {self.admin}, {self.id})"


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

    referenceNo = db.relationship("ReferenceNumbers")

    def __repr__(self):
        return f"Customer: {self.forename} {self.surname} ({self.email}, {self.mobile}, {self.street}, {self.suburb}, {self.city}, {self.state}, {self.postcode}, {self.id})"


class Vendors(db.Model): #Company info (company name, company email etc.)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False, unique=True)
    mobile = db.Column(db.String(12), nullable=False, unique=True)
    userID = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    products = db.relationship("Products")

    def __repr__(self):
        return f"Vendors: {self.name} ({self.email}, {self.mobile}, {self.userID}, {self.id})"


class ReferenceNumbers(db.Model):
    __tablename__ = 'referenceNumbers'
    referenceNo = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)

    order = db.relationship("Orders")

    def __repr__(self):
        return f"Reference Number: {self.referenceNo}, {self.customerID}"


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    description = db.Column(db.String(255))
    vendorID = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=False)
    price = db.Column(db.Float, nullable = False)

    orders = db.relationship("Orders")

    def __repr__(self):
        return f"Product: {self.name}, {self.description} (${self.price}, {self.vendorID}, {self.id})"


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referenceNumber = db.Column(db.Integer, db.ForeignKey("referenceNumbers.referenceNo"), nullable=False)
    productID = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Order: {self.referenceNo}, {self.productID}, {self.quantity}"
