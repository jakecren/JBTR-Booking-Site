from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app, abort
from flask_login import login_user, current_user, logout_user, login_required
from bookingApp import db, bcrypt
from bookingApp.admins.forms import *
from bookingApp.models import Users, Vendors, Products

admins = Blueprint("admins", __name__, template_folder='templates', static_folder='static')



#####  Panel  ######
@admins.route("/panel")
@login_required
def panel():
    return render_template("admins/index.html", title="Admin")


#####  Vendor Product View  #####
@admins.route("/VPView/<int:id>")
@login_required
def vendorProductView(id):
    vendor = Vendors.query.filter_by(id=id).first_or_404()
    products = Products.query.filter_by(vendorID=id)
    return render_template("tempAdmins/vendorProductView.html", title="Vendor Product View", vendor=vendor, products=products)


#####  Register Vendor  #####
@admins.route("/registerVendor", methods=["GET", "POST"])
@login_required
def registerVendor():
    if current_user.admin != 1:
        abort(403)
    form = RegisterVendorForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        Email = str(form.email.data).lower()

        user = Users(forename=form.forename.data, surname=form.surname.data, email=Email, mobile=form.mobile.data, password=hashedPassword, admin=0)
        db.session.add(user)
        db.session.flush()

        vendor = Vendors(name=form.companyName.data, email=form.companyEmail.data, mobile=form.companyMobile.data, userID=user.id)
        db.session.add(vendor)
        db.session.commit()

        flash("Vendor Registered", "success")
        return redirect(url_for("users.admin"))
    return render_template("tempAdmins/registerVendor.html", title="Register Vendor", form=form)


#####  Add Vendor Product  #####
@admins.route("/addVProduct/<int:id>", methods=["GET", "POST"])
@login_required
def addProduct(id):
    form = AddProductForm()
    if form.validate_on_submit():
        product = Products(name=form.name.data, description=form.description.data, price=form.price.data, vendorID=id)
        db.session.add(product)
        db.session.commit()
        flash("Product Added", "success")
        return redirect(url_for("users.admin"))
    return render_template("tempAdmins/addProduct.html", title="Add Product", form=form)