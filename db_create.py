from bookingApp import db, create_app
from bookingApp.models import *
import bcrypt
db.create_all(app=create_app())
db.session.add(lambda: Users(forename="admin", email="change@me.please", password=bcrypt.generate_password_hash("password").decode("utf-8")))
db.session.commit()