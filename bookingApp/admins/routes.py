from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app, abort
from flask_login import login_user, current_user, logout_user, login_required
from bookingApp import db, bcrypt
from bookingApp.admins.forms import *
from bookingApp.models import *
from werkzeug.utils import secure_filename
import os, csv

admins = Blueprint("admins", __name__, template_folder='templates', static_folder='static')


#####  Panel  ######
@admins.route("/panel")
@login_required
def panel():
    products = Products.query.all()
    orders = Orders.query.all()
    users = Users.query.all()
    vendors = Vendors.query.all()
    customers = Customers.query.all()
    return render_template("admins/index.html", title="Admin", products=products, orders=orders, totalTransactions=len(customers), vendors=vendors, userE=False)

#####  Panel - Edit User Modal  ######
@admins.route("/panel/Edit", methods=["GET","POST"])
@login_required
def panelEdit():
    form = EditUserForm()
    products = Products.query.all()
    orders = Orders.query.all()
    users = Users.query.all()
    vendors = Vendors.query.all()

    if form.validate_on_submit():
        current_user.forename = form.forename.data
        current_user.surname = form.surname.data
        current_user.email = str(form.email.data).lower()
        current_user.mobile = form.mobile.data

        if form.password.data != "":
            if bcrypt.check_password_hash(current_user.password, form.oldPassword.data):
                current_user.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for('admins.panel'))

    elif request.method == "GET":
        form.forename.data = current_user.forename
        form.surname.data = current_user.surname
        form.email.data = current_user.email
        form.mobile.data = current_user.mobile

    return render_template("admins/index.html", title="Admin", products=products, orders=orders, totalTransactions=len(users), vendors=vendors, userE=True, form=form)


####  attendee List - View  ####
@admins.route("/attendeeList")
@login_required
def attendeeList():
    attendees = Customers.query.all()
    orders = Orders.query.all()
    products = Products.query.all()
    return render_template("admins/attendeeList.html", title="attendee List", attendees=attendees, orders=orders, products=products, customerD=None)

####  attendee List - Delete Modal  ####
@admins.route("/attendeeList/<int:customerID>")
@login_required
def attendeeListDelete(customerID):
    customerD = Customers.query.get_or_404(customerID)
    attendees = Customers.query.all()
    orders = Orders.query.all()
    products = Products.query.all()
    return render_template("admins/attendeeList.html", title="attendee List", attendees=attendees, orders=orders, products=products, customerD=customerD)

####  Delete Customer  ####
@admins.route("/DC/<int:customerID>")
@login_required
def deleteCustomer(customerID):
    if current_user.admin != 1:
        abort(403)
    customerD = Customers.query.get_or_404(customerID)
    orders = Orders.query.all()

    for order in orders:
        if order.referenceNumber == customerD.id:
            db.session.delete(order)

    db.session.delete(customerD)
    db.session.commit()
    flash(f"Customer: {customerD.forename} {customerD.surname} and Associated Orders Deleted", "success")
    return redirect(url_for("admins.attendeeList"))


####  Vendor List  ####
@admins.route("/vendorList")
@login_required
def vendorList():
    vendors = Vendors.query.all()
    vendorD = None
    return render_template("admins/vendorList.html", title="Vendor List", vendors=vendors, vendorD=vendorD)


#####  Vendor List - Delete Modal  #####
@admins.route("/vendorList/<int:vendorID>")
@login_required
def vendorListDelete(vendorID):
    vendors = Vendors.query.all()
    vendorD = Vendors.query.get_or_404(vendorID)
    return render_template("admins/vendorList.html", title="Vendor List", vendors=vendors, vendorD=vendorD)


####  Delete Vendor  ####
@admins.route("/vendorList/DV/<int:vendorID>")
@login_required
def deleteVendor(vendorID):
    if current_user.admin != 1:
        abort(403)
    vendorD = Vendors.query.get_or_404(vendorID)
    orders = Orders.query.all()
    products = Products.query.all()
    users = Users.query.all()
    
    for order in orders:
        for product in products:
            if product.vendorID == vendorD.id:
                if order.productID == product.id:
                    db.session.delete(order)
    
    for product in products:
        if product.vendorID == vendorD.id:
            db.session.delete(product)
    
    db.session.delete(vendorD)

    for user in users:
        if user.id == vendorD.userID:
            db.session.delete(user)

    db.session.commit()
    flash(f"Vendor: {vendorD.name} and Associated Products and Orders Deleted", "success")
    return redirect(url_for("admins.vendorList"))


#####  Register Vendor  #####
@admins.route("/vendorList/add", methods=["GET", "POST"])
@login_required
def registerVendor():
    if current_user.admin != 1:
        abort(403)
    form = RegisterVendorForm()
    if form.validate_on_submit():
        Email = str(form.companyEmail.data).lower()
        vendor = Vendors(name=form.companyName.data, email=Email, mobile=form.companyMobile.data)
        db.session.add(vendor)
        db.session.commit()

        flash("Vendor Registered", "success")
        return redirect(url_for("admins.vendorList"))
    return render_template("admins/registerVendor.html", title="Register Vendor", form=form)


####  Product List  ####
@admins.route("/productList")
@login_required
def productList():
    products = Products.query.all()
    vendors = Vendors.query.all()
    return render_template("admins/productList.html", title="Product List", products=products, productD=None, vendors=vendors)


#####  Product List - Delete Modal  #####
@admins.route("/productList/<int:productID>")
@login_required
def productListDelete(productID):
    products = Products.query.all()
    productD = Products.query.get_or_404(productID)
    vendors = Vendors.query.all()
    return render_template("admins/productList.html", title="Product List", products=products, productD=productD, vendors=vendors)

####  Delete Product  ####
@admins.route("/productList/DP/<int:productID>")
@login_required
def deleteProduct(productID):
    productD = Products.query.get_or_404(productID)
    orders = Orders.query.all()
    products = Products.query.all()
    
    for order in orders:
        if order.productID == productD.id:
            db.session.delete(order)
    
    db.session.delete(productD)

    db.session.commit()
    if productD.name[:2] == "t_":
        productName = productD.name[2:].replace("_", " ")
    else:
        productName = productD.name.replace("_", " ")
    flash(f"Product: {productName} and Associated Orders Deleted", "success")
    return redirect(url_for("admins.productList"))


####  Add Product  ####
@admins.route("/productList/add", methods=["GET", "POST"])
@login_required
def addProduct():
    vendors = Vendors.query.all()
    choices = [("", "ATC")]
    for vendor in vendors:
        choices.append((f"{vendor.id}", f"{vendor.name}"))
    setattr(AddProductForm, "selectVendor", SelectField('Vendor:', choices=choices))
    form = AddProductForm()

    if form.validate_on_submit():
        name = form.category.data + form.name.data.replace(" ", "_")
        if form.selectVendor.data == "":
            product = Products(name=name, description=form.description.data, price=form.price.data)
        else:
            product = Products(name=name, description=form.description.data, vendorID=form.selectVendor.data, price=form.price.data)
        db.session.add(product)
        db.session.commit()
        flash("Product Added", "success")
        return redirect(url_for("admins.productList"))
    return render_template("admins/addProduct.html", title="Register Vendor", form=form)

####  Add CSV Products  ####
@admins.route("/productList/add/csv", methods=["GET", "POST"])
@login_required
def addCsvProducts():
    form = AddProductsCsvForm()
    products = Products.query.all()
    vendors = Vendors.query.all()

    if form.validate_on_submit():
        productsCsvFN = secure_filename(form.csv.data.filename)
        productsCsv = form.csv.data
        csvPath = os.path.join(current_app.root_path, "admins/static/temp/", productsCsvFN)
        productsCsv.save(csvPath)

        newVendors = []
        duplicateProducts = []

        with open(csvPath) as csvFile:
            readCSV = csv.reader(csvFile, delimiter=',')
            i = 1
            for row in readCSV:
                if i != 1:
                    products = Products.query.all()
                    vendors = Vendors.query.all()
                    vendorID = None
                    for vendor in vendors:
                        if vendor.name == row[2]:
                            vendorID = vendor.id
                    if vendorID == None:
                        newVendor = Vendors(name=row[2])
                        db.session.add(newVendor)
                        db.session.flush()
                        newVendors.append(newVendor.name)
                        newProduct = Products(name=row[0], price=int(row[1]), vendorID=newVendor.id)
                    else:
                        newProduct = Products(name=row[0], price=int(row[1]), vendorID=vendorID)
                    for product in products:
                        if newProduct.name == product.name:
                            duplicateProducts.append(newProduct.name)
                    if newProduct.name not in duplicateProducts:
                        db.session.add(newProduct)
                        db.session.commit()
                    else:
                        db.session.rollback()
                else:
                    i += 1
        if newVendors != []:
            flash(f"The products were added successfully.  The following vendors were added: {', '.join(newVendors)}.  The following products were detected as duplicates, and were not added: {', '.join(duplicateProducts)}.", "success")
        else:
            flash(f"The products were added successfully.  The following products were detected as duplicates, and were not added: {', '.join(duplicateProducts)}.", "success")
        return redirect(url_for('admins.productList'))

    return render_template("admins/productList.html", title="Product List", products=products, productD=None, vendors=vendors, form=form, addProducts=True)


####  Student Volunteers  ####
@admins.route("/students/")
@login_required
def students():
    students = Students.query.all()
    volunteers = []
    performers = []
    for student in students:
        if student.type == "P":
            performers.append(student)
        else:
            volunteers.append(student)
    return render_template("admins/students.html", title="Students", performers=performers, volunteers=volunteers, addStudents=False, studentD=None)

####  Student Volunteers - Add Students Modal  ####
@admins.route("/students/add", methods=["GET", "POST"])
@login_required
def addStudents():
    form = AddStudentsForm()
    students = Students.query.all()
    volunteers = []
    performers = []
    for student in students:
        if student.type == "P":
            performers.append(student)
        else:
            volunteers.append(student)
    
    if form.validate_on_submit():
        studentsCsvFN = secure_filename(form.csv.data.filename)
        studentsCsv = form.csv.data
        csvPath = os.path.join(current_app.root_path, "admins/static/temp/", studentsCsvFN)
        studentsCsv.save(csvPath)

        with open(csvPath) as csvFile:
            i = 1
            for line in csvFile:
                if i != 1:
                    if line[0] == '"':
                        line = line[1:-2].split(",")
                    student = Students(forename=line[0], surname=line[1], year=line[2], type=line[3], mobile=line[4], email=line[5])
                    db.session.add(student)
                else:
                    i += 1
                db.session.commit()
        return redirect(url_for('admins.students'))
    return render_template("admins/students.html", title="Students", performers=performers, volunteers=volunteers, form=form, addStudents=True, studentD=None)

####  Student Volunteers - Delete Student Modal  ####
@admins.route("/students/delete/<int:studentID>")
@login_required
def deleteStudentModal(studentID):
    students = Students.query.all()
    studentD = Students.query.get_or_404(studentID)
    volunteers = []
    performers = []
    for student in students:
        if student.type == "P":
            performers.append(student)
        else:
            volunteers.append(student)
    return render_template("admins/students.html", title="Students", performers=performers, volunteers=volunteers, addStudents=False, studentD=studentD)

####  Student Volunteers - Delete Record ####
@admins.route("/students/delete/<int:studentID>/d")
@login_required
def deleteStudent(studentID):
    studentD = Students.query.get_or_404(studentID)
    db.session.delete(studentD)
    db.session.commit()
    return redirect(url_for('admins.students'))