import os

class Config ():
    SECRET_KEY = ";\x01\r\xce\xa1\x87C\xf6\xb4fP\x18\xf2j\xdf3"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:adminpassword@atc-jbtr-web-app.cxbbsztdneyk.ap-southeast-2.rds.amazonaws.com/jbtrSiteDB"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
