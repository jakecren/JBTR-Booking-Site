from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from bookingApp import db, bcrypt
from bookingApp.users.forms import LoginForm
from bookingApp.models import Users

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
    return render_template("admin.html", title="Admin")