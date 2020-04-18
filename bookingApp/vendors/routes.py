from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app, abort
from flask_login import login_user, current_user, logout_user, login_required
from bookingApp import db, bcrypt
from bookingApp.vendors.forms import *
from bookingApp.models import Users, Vendors, Products

vendors = Blueprint("vendors", __name__, template_folder='templates')


@vendors.route("/panel")
@login_required
def panel():
    vendors = Vendors.query.all()
    return render_template("vendors/admin.html", title="Admin", vendors=vendors)