import os
from flask import Flask


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.

basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

#Create the app
app = Flask(__name__)
app.secret_key = SECRET_KEY


# DONE IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/fyyur'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
