from flask import render_template, request, Blueprint, redirect, url_for, flash
from bookingApp.main.forms import *
from bookingApp import db
from bookingApp.models import *
from wtforms import IntegerField
from flask_login import login_user, logout_user, current_user, login_required


main = Blueprint("main", __name__)

#####  Splash  #####
@main.route("/")
def splash():
    return render_template("splash.html", title="JBTR RSVP")


#####  RSVP  #####
@main.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    products = Products.query.all()
    for product in products:
        setattr(rsvpForm, product.name, IntegerField(product.name))
    form = rsvpForm()
    
    if form.validate_on_submit():        
        Email = str(form.email.data).lower()
        customer = Customers(forename=form.forename.data, surname=form.surname.data, email=Email, mobile=form.mobile.data, street=form.street.data, suburb=form.suburb.data, city=form.city.data, state=form.state.data, postcode=form.postcode.data)
        db.session.add(customer)
        db.session.flush()

        refNo = ReferenceNumbers(customerID=customer.id)
        db.session.add(refNo)
        db.session.flush()

        for product in products:
            exec(f"""if form.{product.name}.data != 0:
                order = Orders(referenceNumber=refNo.referenceNo, productID=product.id, quantity=form.{product.name}.data)
                db.session.add(order)
                db.session.flush()""")

        db.session.commit()

    return render_template("rsvp.html", title="RSVP", form=form, products=products)


#####  Login  #####
@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admins.panel"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=str(form.email.data).lower()).first()
        if user and form.password.data == user.password:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("admins.panel"))
        else:
            flash("Login unsuccessful.  Please check email and password!", "danger")
    return render_template("login.html", title="Login", form=form)


#####  Logout  ######
@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.splash"))


#####  Generic  #####
@main.route("/generic")
def generic():
    return render_template("generic.html", title="*GENERIC*")


#####  Elements  #####
@main.route("/elements")
def elements():
    return render_template("elements.html", title="*ELEMENTS*")
