from flask_sqlalchemy import SQLAlchemy
from config import app
from flask_migrate import Migrate


db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'venues'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255))
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120), nullable=True)
  phone = db.Column(db.String(120), nullable=True)
  image_link = db.Column(db.String(500), nullable=True)
  facebook_link = db.Column(db.String(120), nullable=True)
  website_link = db.Column(db.String(120), nullable=True)
  genres = db.Column(db.ARRAY(db.String), nullable=False)
  seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', backref='venue', lazy=True)  
  # DONE: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
  __tablename__ = 'artists'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.ARRAY(db.String), nullable=True)
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website_link = db.Column(db.String(120), nullable=True)
  seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', backref='artist', lazy=True) 

class Show(db.Model):
    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key=True)
    start_time=db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    # DONE: implement any missing fields, as a database migration using Flask-Migrate ***DONE***

# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration. #IN PROGRESS#