from bookingApp import db, create_app
from bookingApp.models import *
db.create_all(app=create_app())