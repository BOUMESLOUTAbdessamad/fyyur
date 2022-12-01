#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy import func
from flask_migrate import Migrate
from config import SQLALCHEMY_DATABASE_URI, DEBUG, SECRET_KEY


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.secret_key = SECRET_KEY
moment = Moment(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

migrate = Migrate(app, db)
# DONE: connect to a local postgresql database

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

#---------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

	# DONE: replace with real venues data.
	#       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

    data = []
    regions= db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state).order_by('state').all()
    for r in regions:
        regionVenues = []
        dbVenues = Venue.query.filter_by(state = r.state).filter_by(city = r.city).order_by('name').all()
        for venue in dbVenues :
            regionVenues.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": 0
            })

        data.append({
            "city": r.city,
            "state" : r.state,
            "venues": regionVenues
        })

    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

	search = request.form.get('search_term', '')
	keyword = "%{}%".format(search.strip()) # use strip() to trim the keywords for exact matching 
	results = Venue.query.filter( Venue.name.ilike(keyword)).all()
	data = []
	for r in results:
                
		#Get Upcoming shows for each Venue
		upcoming_shows = Show.query.\
		filter(
			Show.venue_id == r.id,
			Show.start_time > datetime.now()
		).all()

		data.append({
			"id": r.id,
			"name": r.name,
			"num_upcoming_shows": len(upcoming_shows),
		})

	response={
	"count": len(data),
	"data": data
	}

	return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # DONE: replace with real venue data from the venues table, using venue_id
    
    venueData = Venue.query.get(venue_id)

    past_shows = Show.query.\
        filter(
            Show.venue_id == venue_id,
            Show.artist_id == Artist.id,
            Show.start_time < datetime.now()
        ).all()
    
    upcoming_shows = Show.query.\
        filter(
            Show.venue_id == venue_id,
            Show.artist_id == Artist.id,
            Show.start_time > datetime.now()
        ).all()

    past_shows_data = []
    for past_show in past_shows:
        past_shows_data.append({
            "artist_id": past_show.artist.id,
            "artist_name": past_show.artist.name,
            "artist_image_link": past_show.artist.image_link,
            "start_time": past_show.start_time.strftime("%m/%d/%Y, %H:%M"),
        })

    upcoming_shows_data = []
    for upcoming_show in upcoming_shows:
        upcoming_shows_data.append({
            "artist_id": upcoming_show.artist.id,
            "artist_name": upcoming_show.artist.name,
            "artist_image_link": upcoming_show.artist.image_link,
            "start_time": upcoming_show.start_time.strftime("%m/%d/%Y, %H:%M"),
        })

    data = {
        "id" : venueData.id,
        "name": venueData.name,
        "genres": venueData.genres,
        "address": venueData.address,
        "city":  venueData.city,
        "state":  venueData.state,
        "phone":  venueData.phone,
        "website":  venueData.website_link,
        "facebook_link":  venueData.facebook_link,
        "seeking_talent": venueData.seeking_talent,
        "image_link":  venueData.image_link,
        "upcoming_shows": upcoming_shows_data,
        "past_shows": past_shows_data,
        "past_shows_count": len(past_shows_data),
        "upcoming_shows_count": len(upcoming_shows_data),
    }

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion

	form = VenueForm(request.form)
	try:
		venue = Venue(
			name=form.name.data,
			city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone = form.phone.data,
			genres=form.genres.data,
      facebook_link=form.facebook_link.data,
			image_link = form.image_link.data,
			website_link=form.website_link.data,
      seeking_talent=form.seeking_talent.data,
			seeking_description=form.seeking_description.data
		)
		db.session.add(venue)
		db.session.commit()
        # on successful db insert, flash success
		flash('Venue ' + form.name.data + ' was successfully listed!')
	except:
		error=True
		db.session.rollback()
        #on unsuccessful db insert, flash an error instead.
		flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
	finally:
		db.session.close()

	return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete_venue', methods=['POST'])
def delete_venue(venue_id):
    # DOING: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

    try:
        Venue.query.filter(Venue.id == venue_id).delete()
        db.session.commit()
        flash('Venue was successfully Deleted!')
    except:
        db.session.rollback()
    finally: 
        db.session.close()

    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database
  
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
	# DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
	# seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
	# search for "band" should return "The Wild Sax Band".
	
	search = request.form.get('search_term', '')
	keyword = "%{}%".format(search.strip()) # use strip() to trim the keywords for exact matching
	results = Artist.query.filter( Artist.name.ilike(keyword)).all()
	data = []
	for r in results:
                
		#Get Upcoming shows for each Artist
		upcoming_shows = Show.query.\
		filter(
			Show.artist_id == r.id,
			Show.start_time > datetime.now()
		).all()

		data.append({
			"id": r.id,
			"name": r.name,
			"num_upcoming_shows": len(upcoming_shows),
		})

	response={
		"count": len(data),
		"data": data
	}

	return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # DONE: replace with real artist data from the artist table, using artist_id

    data = Artist.query.get(artist_id)
    artist = {
        "id": data.id,
        "name": data.name,
        "genres": data.genres,
        "city": data.city,
        "state": data.state,
        "phone": data.phone,
        "website": data.website_link,
        "facebook_link": data.facebook_link,
        "seeking_venue": data.seeking_venue,
        "seeking_description": data.seeking_description,
        "image_link": data.image_link,
    }
    return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id) :
    artistData = Artist.query.get(artist_id)
    form = ArtistForm(obj=artistData)
    artist = {
        "id": artistData.id,
        "name": artistData.name,
        "genres": artistData.genres,
        "city": artistData.city,
        "state": artistData.state,
        "phone": artistData.phone,
        "website_link": artistData.website_link,
        "facebook_link": artistData.facebook_link,
        "seeking_venue": artistData.seeking_venue,
        "seeking_description": artistData.seeking_description,
        "image_link": artistData.image_link,
    }

    # DONE: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

    editArtist=Artist.query.get(artist_id)
    form = ArtistForm(request.form)
    try:
        artist = Artist(
            name=form.name.data,
            city=form.city.data,
            genres=form.genres.data,
            state=form.state.data,
            phone = form.phone.data,
            image_link = form.image_link.data,
            facebook_link=form.facebook_link.data,
            website_link=form.website_link.data,
            seeking_venue=form.seeking_venue.data,
            seeking_description=form.seeking_description.data
        )
        
        editArtist.name = artist.name
        editArtist.city = artist.city
        editArtist.genres = artist.genres
        editArtist.state = artist.state
        editArtist.phone = artist.phone
        editArtist.image_link = artist.image_link
        editArtist.facebook_link = artist.facebook_link
        editArtist.website_link = artist.website_link
        editArtist.seeking_venue = artist.seeking_venue
        editArtist.seeking_description = artist.seeking_description

        db.session.commit()
    except:
        error=True
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  venueData = Venue.query.get(venue_id)
  form = VenueForm(obj=venueData)

  venue = {
    "id": venueData.id,
    "name": venueData.name,
    "genres": venueData.genres,
    "city": venueData.city,
    "state": venueData.state,
    "phone": venueData.phone,
    "address": venueData.address,
    "website": venueData.website_link,
    "facebook_link": venueData.facebook_link,
    "seeking_talent": venueData.seeking_talent,
    "seeking_description": venueData.seeking_description,
    "image_link": venueData.image_link,
  }

  # DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  editVenue =Venue.query.get(venue_id)
  form = VenueForm(request.form)
  try:
      venue = Venue(
          name=form.name.data,
          city=form.city.data,
          genres=form.genres.data,
          state=form.state.data,
          phone = form.phone.data,
          address = form.address.data,
          image_link = form.image_link.data,
          facebook_link=form.facebook_link.data,
          website_link=form.website_link.data,
          seeking_talent=form.seeking_talent.data,
          seeking_description=form.seeking_description.data
      )
      editVenue.name = venue.name
      editVenue.city = venue.city
      editVenue.genres = venue.genres
      editVenue.state = venue.state
      editVenue.phone = venue.phone
      editVenue.address = venue.address
      editVenue.image_link = venue.image_link
      editVenue.facebook_link = venue.facebook_link
      editVenue.website_link = venue.website_link
      editVenue.seeking_talent = venue.seeking_talent
      editVenue.seeking_description = venue.seeking_description

      db.session.commit()
  
  except:
      db.session.rollback()
  finally:
      db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
	# called upon submitting the new artist listing form
	# DONE: insert form data as a new Artist record in the db, instead
	# DONE: modify data to be the data object returned from db insertion

	error = False
	form = ArtistForm(request.form)
	try:
		artist = Artist(
			name=form.name.data,
			city=form.city.data,
			genres=form.genres.data,
			state=form.state.data,
			phone = form.phone.data,
			image_link = form.image_link.data,
			facebook_link=form.facebook_link.data,
			website_link=form.website_link.data,
			seeking_venue=form.seeking_venue.data,
			seeking_description=form.seeking_description.data
		)

		db.session.add(artist)
		db.session.commit()
	except:
		error=True
		db.session.rollback()
	finally:
		db.session.close()

	if not error :
	# on successful db insert, flash success
		flash('Artist ' + form.name.data + ' was successfully listed!')
	else:
		# Done: on unsuccessful db insert, flash an error instead.
		flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')

	return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real shows* data.
    shows = Show.query.all()
    data = []
    for show in shows:
      data.append({
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
      })

    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead
		# on successful db insert, flash success

    form = ShowForm(request.form)
    try:
        show = Show(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                start_time=form.start_time.data,
            )

        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()

	# DONE: on unsuccessful db insert, flash an error instead.
	# e.g., flash('An error occurred. Show could not be listed.')
	# see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=DEBUG)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
