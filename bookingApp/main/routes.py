from flask import render_template, request, Blueprint, redirect, url_for, flash, session
from bookingApp.main.forms import *
from bookingApp import db
from bookingApp.models import *
from wtforms import IntegerField
from flask_login import login_user, logout_user, current_user, login_required


main = Blueprint("main", __name__, template_folder='templates')

#####  Splash  #####
@main.route("/")
def splash():
    return render_template("main/splash.html", title="JBTR RSVP")


#####  RSVP - Page 1  #####
@main.route("/rsvp", methods=["GET", "POST"])
def rsvp():
    form = rsvpForm_1()
    
    if form.validate_on_submit():        
        Email = str(form.email.data).lower()
        customer = [form.forename.data, form.surname.data, Email, form.mobile.data, form.street.data, form.suburb.data, form.city.data, form.state.data, form.postcode.data]
        session['customer'] = customer
        session.modified = True

        return redirect(url_for('main.rsvp_2'))

    return render_template("main/rsvp_1.html", title="RSVP", form=form)


#####  RSVP - Page 2  #####
@main.route("/rsvp/2", methods=["GET", "POST"])
def rsvp_2():
    products = Products.query.all()
    for product in products:
        setattr(rsvpForm_2, product.name, IntegerField(product.name))
    form = rsvpForm_2()
    
    if form.validate_on_submit():
        orderedProducts = []
        for product in products:
            exec(f"""if form.{product.name}.data != 0:
                order = [product.id, form.{product.name}.data]
                session['{product.name}'] = order
                orderedProducts.append("{product.name}")""" )
        session['orderedProducts'] = orderedProducts
        session.modified = True

        return redirect(url_for('main.rsvp_3'))

    return render_template("main/rsvp_2.html", title="RSVP", form=form, products=products)


#####  RSVP - Page 3  #####
@main.route("/rsvp/3", methods=["GET", "POST"])
def rsvp_3():
    products = Products.query.all()
    form = rsvpForm_3()
    
    if form.validate_on_submit():
        customer = session.get('customer')
        Customer = Customers(forename=customer[0], surname=customer[1], email=customer[2], mobile=customer[3], street=customer[4], suburb=customer[5], city=customer[6], state=customer[7], postcode=customer[8])
        db.session.add(Customer)
        db.session.flush()

        refNo = ReferenceNumbers(customerID=Customer.id)
        db.session.add(refNo)
        db.session.flush()

        for product in products:
            if product.name in session.get('orderedProducts'):
                exec(f"""order = Orders(referenceNumber=refNo.referenceNo, productID=session.get('{product.name}')[0], quantity=session.get('{product.name}')[1])
db.session.add(order)""")
        
        db.session.commit()
        
        return redirect(url_for('main.splash'))

    return render_template("main/rsvp_3.html", title="RSVP", form=form, products=products)


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
    return render_template("main/login.html", title="Login", form=form)


#####  Logout  ######
@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.splash"))


#####  Generic  #####
@main.route("/generic")
def generic():
    return render_template("main/generic.html", title="*GENERIC*")


#####  Elements  #####
@main.route("/elements")
def elements():
    return render_template("main/elements.html", title="*ELEMENTS*")
