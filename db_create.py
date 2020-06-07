from bookingApp import db, create_app
from bookingApp.models import *
import bcrypt
db.create_all(app=create_app())
db.session.add(lambda: Users(forename="admin", email="admin@atc.jbtr", password=bcrypt.generate_password_hash("admin").decode("utf-8"), admin=1))
db.session.commit()