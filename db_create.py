from bookingApp import db, create_app, bcrypt
from bookingApp.models import *
app = create_app()
app.app_context().push()
db.create_all()
adminDefault = Users(forename="admin", email="admin@atc.jbtr", password=bcrypt.generate_password_hash("admin").decode("utf-8"), admin=1)
defaultVendor = Vendors(name="ATC Catering")
db.session.add(adminDefault)
db.session.add(defaultVendor)
db.session.commit()
print("All Done!")