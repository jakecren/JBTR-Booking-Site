from flask import render_template, request, Blueprint, redirect, url_for, flash
from bookingApp.main.forms import rsvpForm
from bookingApp import db
from bookingApp.models import Customers


main = Blueprint("main", __name__)

#####  Splash  #####
@main.route("/")
def splash():
    return render_template("splash.html", title="JBTR RSVP")


#####  RSVP  #####
@main.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    form = rsvpForm()
    if form.validate_on_submit():
        flash(f"{form.forename.data}, {form.surname.data}, {form.email.data}, {form.mobile.data}, {form.street.data}, {form.suburb.data}, {form.city.data}, {form.state.data}, {form.postcode.data}.")

    return render_template("rsvp.html", title="RSVP", form=form)


#####  Generic  #####
@main.route("/generic")
def generic():
    return render_template("generic.html", title="*GENERIC*")


#####  Elements  #####
@main.route("/elements")
def elements():
    return render_template("elements.html", title="*ELEMENTS*")
