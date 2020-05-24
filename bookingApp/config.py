import os
import datetime

class Config():
    # Encryption:
    SECRET_KEY = ";\x01\r\xce\xa1\x87C\xf6\xb4fP\x18\xf2j\xdf3"

    # Databasing
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:adminpassword@atc-jbtr-web-app.cxbbsztdneyk.ap-southeast-2.rds.amazonaws.com/jbtrSiteDB"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Sessions
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=1)

    # Email
    SENDGRID_API_KEY = "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"