from flask import render_template, request, Blueprint, redirect, url_for, flash


main = Blueprint("main", __name__)

#####  Splash  #####
@main.route("/")
def splash():
    return render_template("splash.html", title="JBTR RSVP")


#####  Generic  #####
@main.route("/generic")
def generic():
    return render_template("generic.html", title="*GENERIC*")


#####  Elements  #####
@main.route("/elements")
def elements():
    return render_template("elements.html", title="*ELEMENTS*")
