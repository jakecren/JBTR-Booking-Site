from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app, abort
from flask_login import login_user, current_user, logout_user, login_required
from bookingApp import db, bcrypt
from bookingApp.users.forms import LoginForm, RegisterVendorForm
from bookingApp.models import Users, Vendors

users = Blueprint("users", __name__)


#####  Login  #####
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.admin"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=str(form.email.data).lower()).first()
        if user and form.password.data == user.password:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("users.admin"))
        else:
            flash("Login unsuccessful.  Please check email and password!", "danger")
    return render_template("login.html", title="Login", form=form)


#####  Logout  ######
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.splash"))


#####  Admin  ######
@users.route("/admin")
@login_required
def admin():
    vendors = Vendors.query.all()
    return render_template("admin.html", title="Admin", vendors=vendors)


##### Register Vendor #####
@users.route("/registerVendor", methods=["GET", "POST"])
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
        db.session.commit()

        user = Users.query.filter_by(email=Email).first_or_404()
        vendor = Vendors(name=form.companyName.data, email=form.companyEmail.data, mobile=form.companyMobile.data, userID=user.id)
        db.session.add(vendor)
        db.session.commit()

        flash("Vendor Registered", "success")
        return redirect(url_for("users.admin"))
    return render_template("registerVendor.html", title="Register Vendor", form=form)