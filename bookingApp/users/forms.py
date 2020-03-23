from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from bookingApp.models import Users, Vendors, Products


class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired()])
    remember = BooleanField("Remember Me:")
    submit = SubmitField("Log In")


class RegisterVendorForm(FlaskForm):
    # Account Info
    forename = StringField("Forename:", validators=[DataRequired()])
    surname = StringField("Surname:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    mobile = StringField("Mobile:", validators=[DataRequired(), Length(10,12)])
    password = PasswordField("Password:", validators=[DataRequired()])
    confirmPassword = PasswordField("Confirm Password:", validators=[DataRequired(), EqualTo("password")])

    # Company Info
    companyName = StringField("Company Name:", validators=[DataRequired()])
    companyEmail = StringField("Company Email:", validators=[DataRequired(), Email()])
    companyMobile = StringField("Company Mobile:", validators=[DataRequired(), Length(10,12)])

    submit = SubmitField("Register")

    # Validate unique fields
    def validate_mobile(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is unavailable, please choose a different email.")

    def validate_mobile(self, mobile):
        user = Users.query.filter_by(mobile=mobile.data).first()
        if user:
            raise ValidationError("Mobile is unavailable, please choose a different mobile.")

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


class AddProductForm(FlaskForm):
    name = StringField("Product Name:", validators=[DataRequired()])
    description = StringField("Description:")
    price = FloatField("Price:", validators=[DataRequired()])
    submit = SubmitField("Add Product")

    # Validate unique fields
    def validate_name(self, name):
        vendor = Vendors.query.filter_by(name=name.data).first()
        if vendor:
            raise ValidationError("Name is unavailable, please choose a different name.")