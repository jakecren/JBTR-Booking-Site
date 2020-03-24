from flask import render_template, request, Blueprint, redirect, url_for, flash
from bookingApp.main.forms import rsvpForm
from bookingApp import db
from bookingApp.models import Customers, Products, ReferenceNumbers, Orders
from wtforms import IntegerField


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
        """flash(f"{form.forename.data}, {form.surname.data}, {form.email.data}, {form.mobile.data}, {form.street.data}, {form.suburb.data}, {form.city.data}, {form.state.data}, {form.postcode.data}.")
        flash(f"Tickets:\n{formProducts}")
        for product in formProducts:
            print("Ticket:", product, "- #:", getattr(form, product).data)"""
        
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


#####  Generic  #####
@main.route("/generic")
def generic():
    return render_template("generic.html", title="*GENERIC*")


#####  Elements  #####
@main.route("/elements")
def elements():
    return render_template("elements.html", title="*ELEMENTS*")
