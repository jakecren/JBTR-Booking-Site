from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from bookingApp.models import Customers, Products

class rsvpForm_1(FlaskForm):
    # Customer Details
    forename = StringField("Forename:", validators=[DataRequired()])
    surname = StringField("Surname:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    mobile = StringField("Mobile:", validators=[DataRequired(), Length(10, 12)])
    street = StringField("Street Address (#, Name):", validators=[DataRequired()])
    suburb = StringField("Suburb:", validators=[DataRequired()])
    city = StringField("City:", validators=[DataRequired()])
    state = SelectField("State:", validators=[DataRequired()], choices=[("", "--- Select State ---"), ("QLD", "QLD"), ("NSW", "NSW"), ("VIC", "VIC"), ("NT", "NT"), ("SA", "SA"), ("WA", "WA"), ("Tas", "Tas")])
    postcode = StringField("Postcode", validators=[DataRequired()])

    # Submit
    submit = SubmitField("Continue")

    def validate_mobile(self, mobile):
        if str(mobile.data).isnumeric() == False:
            raise ValidationError("Mobile number can only consist of numbers.")
    
    def validate_postcode(self, postcode):
        if len(str(postcode.data)) != 4:
            raise ValidationError("Postcode must be 4 numbers long.")
        if str(postcode.data).isnumeric() == False:
            raise ValidationError("Post code can only consist of numbers.")

class rsvpForm_2(FlaskForm):
    # Submit
    submit = SubmitField("Continue")


class rsvpForm_3(FlaskForm):
    # Submit
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired()])
    remember = BooleanField("Remember Me:")
    submit = SubmitField("Log In")