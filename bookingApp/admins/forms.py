from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, SelectField, TextAreaField, RadioField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from bookingApp.models import Users, Vendors, Products


class RegisterVendorForm(FlaskForm):
    # Company Info
    companyName = StringField("Company Name:", validators=[DataRequired()])
    companyEmail = StringField("Company Email:", validators=[DataRequired(), Email()])
    companyMobile = StringField("Company Mobile:", validators=[DataRequired(), Length(10,12)])

    submit = SubmitField("Register")

    # Validate unique fields
    def validate_companyName(self, companyName):
        vendor = Vendors.query.filter_by(name=companyName.data).first()
        if vendor:
            raise ValidationError("Company name is unavailable, please choose a different Company name.")
    
    def validate_companyEmail(self, companyEmail):
        vendor = Vendors.query.filter_by(email=companyEmail.data).first()
        if vendor:
            raise ValidationError("Company email is unavailable, please choose a different Company email.")
    
    def validate_companyMobile(self, companyMobile):
        vendor = Vendors.query.filter_by(mobile=companyMobile.data).first()
        if vendor:
            raise ValidationError("Company mobile is unavailable, please choose a different Company mobile.")
        if companyMobile.data.isnumeric() == False:
            raise ValidationError("Mobile number can only consist of numbers.")


class AddProductForm(FlaskForm):
    name = StringField("Product Name:", validators=[DataRequired()])
    description = TextAreaField("Description:")
    price = FloatField("Price:")
    category = RadioField("Category", choices=[("t_", "Ticket"), ("", "Catering")])
    submit = SubmitField("Add Product")

    # Validate unique fields
    def validate_name(self, name):
        vendor = Vendors.query.filter_by(name=name.data).first()
        if vendor:
            raise ValidationError("Name is unavailable, please choose a different name.")


class EditUserForm(FlaskForm):
    forename = StringField("Forename:", validators=[DataRequired()])
    surname = StringField("Surname:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    mobile = StringField("Mobile:", validators=[DataRequired(), Length(10,12)])
    password = PasswordField("Password:")
    confirmPassword = PasswordField("Confirm Password:", validators=[EqualTo("password")])
    oldPassword = PasswordField("Old Password:")
    submit = SubmitField("Save")

    def validate_mobile(self, mobile):
        if str(mobile.data).isnumeric() != True:
            raise ValidationError("Mobile number can only consist of numbers.")


class AddStudentsForm(FlaskForm):
    csv = FileField("Upload .CSV File", validators=[FileAllowed(["csv"]), FileRequired()])
    submit = SubmitField("Add Students")


class AddProductsCsvForm(FlaskForm):
    csv = FileField("Upload .CSV File", validators=[FileAllowed(["csv"]), FileRequired()])
    submit = SubmitField("Add Products")
