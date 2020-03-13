# import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set up the database
engine = create_engine("sqlite:///c:/Users/kenww/OneDrive/Desktop/GitHubProjects/Class/surfs_up/hawaii.sqlite")

# reflect the database into our classes
Base = automap_base()

# reflect the database
Base.prepare(engine, reflect=True)

# save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
# session = Session(engine)
# session = scoped_session(sessionmaker(bind=engine)) 

# define our Flask app
app = Flask(__name__)

# define the welcome route
@app.route("/")

# welscome function
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br>
    Available Routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/temp/start/end
    ''')

# route for for the precipitation analysis
@app.route("/api/v1.0/precipitation")

# precipitation function
def precipitation():
    
    # create a session link from Python to our database
    session = Session(engine)
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
	  filter(Measurement.date >= prev_year).all()
    
    session.close()
    
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# stations route
@app.route("/api/v1.0/stations")

# stations function
def stations():
    # create a session link from Python to our database
    session = Session(engine)
    
    results = session.query(Station.station).all()
    
    session.close()
    
    stations = list(np.ravel(results))
    return jsonify(stations)

# monthly temperature route
@app.route("/api/v1.0/tobs")

# temperature function
def temp_monthly():
    
    # create a session link from Python to our database
    session = Session(engine)
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()
    
    session.close()
    
    temps = list(np.ravel(results))
    return jsonify(temps)

# statistic route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# stats function
def stats(start=None, end=None):
    
    # create a session link from Python to our database
    session = Session(engine)
    
    # create a list for the min, avg, and max
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    results = session.query(*sel).filter(Measurement.date >= start)
    
    if end:
        results = results.filter(Measurement.date <= end)
    
    results = results.all()
    
    session.close()
    
    temps = list(np.ravel(results))
    return jsonify(temps)

    # if not end:
    #     results = session.query(*sel).filter(Measurement.date >= start).all()
    #     temps = list(np.ravel(results))
    #     return jsonify(temps)
    
    # results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # temps = list(np.ravel(results))
    # return jsonify(temps)
	    




