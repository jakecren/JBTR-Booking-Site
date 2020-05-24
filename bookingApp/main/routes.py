from flask import render_template, request, Blueprint, redirect, url_for, flash, session
from bookingApp.main.forms import *
from bookingApp import db, Mail, SGmail
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
    customer = session.get('customer')
    if session.get('customer') != None:
        form = rsvpForm_1(state=customer[7])
    else:
        form = rsvpForm_1()
    
    if form.validate_on_submit():
        if form.state.data == "":
            form.state.errors.append("Please select state.")     
        Email = str(form.email.data).lower()
        customer = [form.forename.data, form.surname.data, Email, form.mobile.data, form.street.data, form.suburb.data, form.city.data, form.state.data, form.postcode.data]
        session['customer'] = customer
        session.modified = True
        flash("Hell Yeah", "success")
        
        return redirect(url_for('main.rsvp_2'))
    return render_template("main/rsvp_1.html", title="RSVP", form=form, customer=customer)


#####  RSVP - Page 2  #####
@main.route("/rsvp/2", methods=["GET", "POST"])
def rsvp_2():
    if session.get('customer') == None:
        return redirect(url_for('main.rsvp'))
    
    products = Products.query.all()
    for product in products:
        setattr(rsvpForm_2, product.name, IntegerField(product.name))
    form = rsvpForm_2()

    customerOrders = []
    orderedProducts = session.get('orderedProducts')
    if session.get('orderedProducts') != None:
        for product in orderedProducts:
            exec(f"customerOrders.append(session.get('{product}'))")
    
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
    
    if session.get('orderedProducts') != None:
        return render_template("main/rsvp_2.html", title="RSVP", form=form, products=products, customerOrders=customerOrders)
        print("Customer Orders!")
    else:
        return render_template("main/rsvp_2.html", title="RSVP", form=form, products=products)


#####  RSVP - Page 3  #####
@main.route("/rsvp/3", methods=["GET", "POST"])
def rsvp_3():
    if session.get('orderedProducts') == None:
        return redirect(url_for('main.rsvp_2'))

    products = Products.query.all()
    form = rsvpForm_3()
    orders = Orders.query.all()
    customer = session.get('customer')

    customerOrders = []
    orderedProducts = session.get('orderedProducts')
    for product in orderedProducts:
        exec(f"customerOrders.append(session.get('{product}'))")
    
    if form.validate_on_submit():
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
        session.clear()

        message = Mail(
            from_email='donotreply@atcjbtrrsvp.com',
            to_emails="jakecrennie@gmail.com",
            subject='RSVP Successful',
            html_content='Hell yeah boi!')
        message.template_id = "d-25f51cfbf3ca459585aa2a61ff4feb82"
        with open('bookingApp/main/templates/main/emails/receipt.html', 'r') as f:
            content = f.read()
    
        total = 0.00
        contentStr = ""
        for order in orders:
            for product in products:
                if order.referenceNumber == 10:
                    if product.id == order.productID:
                        total += (order.quantity * product.price)
                        if product.name[:2] == "t_":
                            productName = product.name[2:]
                        else:
                            productName = product.name
                        contentStr += f"""
                        <tr>
                            <td>{productName.replace("_", " ")}</td>
                            <td>{order.quantity}</td>
                            <td>${product.price}</td>
                            <td>${(product.price * order.quantity)}</td>
                        </tr>
                        """

        message.dynamic_template_data = {
            'content': content.format(tbody=contentStr, total=total)}

        SGmail.send(message)

        return redirect(url_for('main.splash'))
    return render_template("main/rsvp_3.html", title="RSVP", form=form, products=products, customer=customer, customerOrders=customerOrders)

@main.route("/email")
def email():
    products = Products.query.all()
    orders = Orders.query.all()

    message = Mail(
        from_email='donotreply@atcjbtrrsvp.com',
        to_emails="jakecrennie@gmail.com",
        subject='RSVP Successful',
        html_content='Hell yeah boi!')
    message.template_id = "d-25f51cfbf3ca459585aa2a61ff4feb82"
    with open('bookingApp/main/templates/main/emails/test.html', 'r') as f:
        content = f.read()
    
    total = 0.00
    contentStr = ""
    for order in orders:
        for product in products:
            if order.referenceNumber == 10:
                if product.id == order.productID:
                    total += (order.quantity * product.price)
                    if product.name[:2] == "t_":
                        productName = product.name[2:]
                    else:
                        productName = product.name
                    contentStr += f"""
                    <tr>
                        <td>{productName.replace("_", " ")}</td>
                        <td>{order.quantity}</td>
                        <td>${product.price}</td>
                        <td>${(product.price * order.quantity)}</td>
                    </tr>
                    """

    message.dynamic_template_data = {
        'content': content.format(tbody=contentStr, total=total)}

    SGmail.send(message)

    return redirect(url_for('main.splash'))

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
    session.clear()
    return render_template("main/generic.html", title="*GENERIC*")


#####  Elements  #####
@main.route("/elements")
def elements():
    return render_template("main/elements.html", title="*ELEMENTS*")
