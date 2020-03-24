from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from bookingApp.models import Customers, Products

class rsvpForm(FlaskForm):
    # Customer Details
    forename = StringField("Forename:", validators=[DataRequired()])
    surname = StringField("Surname:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired(), Email()])
    mobile = StringField("Mobile:", validators=[DataRequired(), Length(10, 12)])
    street = StringField("Street Address (#, Name):", validators=[DataRequired()])
    suburb = StringField("Suburb:", validators=[DataRequired()])
    city = StringField("City:", validators=[DataRequired()])
    state = StringField("State:", validators=[DataRequired()])
    postcode = StringField("Postcode", validators=[DataRequired(), Length(4, 4)])

    # Submit
    submit = SubmitField("Submit")
