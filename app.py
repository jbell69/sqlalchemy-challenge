# import dependances
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import Flask, jsonify
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create an app
app = Flask(__name__)


# Index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to Hawaii Climate homepage!<br/>"
	    f"Available Routes:<br/>"
        f'<a href="http://127.0.0.1:5000/api/v1.0/precipitation">All Station Precipitation</a><br/>'
        f'<a href="http://127.0.0.1:5000/api/v1.0/stations">All Station List</a><br/>'
	    f'<a href="http://127.0.0.1:5000/api/v1.0/tobs">Observed Temperatures</a><br/>'
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_end_date"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
   # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipition data by date"""
    # Query all measurement
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precipitations
    all_precipitations = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["Precipitation"] = prcp
        
        all_precipitations.append(precipitation_dict)

    return jsonify(all_precipitations)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Stations"""
    # Query all stations
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations) 

# Observed Temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Observed Temperature' page...")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Stations"""
    # Query for all temperature for last year
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    Temp_last_year = session.query(Measurement.date,Measurement.tobs).\
    filter((Measurement.date) >= query_date).all()

    session.close()

    # Convert list of tuples into normal list
    temps = list(np.ravel(Temp_last_year))

    return jsonify(temps)

# Start Date route
@app.route("/api/v1.0/start_date")
def start_date():
    print("Server received request for 'Start Date Temperature' page...")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for max, min, avg temperature for starting date

    query_date = dt.date(2011, 8, 23)

    start_date_temps = session.query(
        (func.min(Measurement.tobs)),
        (func.max(Measurement.tobs)),
        (func.avg(Measurement.tobs))).\
    filter(Measurement.date >= query_date).all()

    session.close()

    # Convert list of tuples into normal list
    temps = list(np.ravel(start_date_temps))

    return jsonify(temps)

# Start and End Date route
@app.route("/api/v1.0/start_end_date")
def start_end_date():
    print("Server received request for 'Start/End Date Temperature' page...")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query for max, min, avg temperature for starting date

    start_date = dt.date(2011, 8, 23)
    end_date = dt.date(2011, 9, 30)

    #query_date = start_date - end_date

    start_end_date_temps = session.query(
        (func.min(Measurement.tobs)),
        (func.max(Measurement.tobs)),
        (func.avg(Measurement.tobs))).\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Convert list of tuples into normal list
    temps = list(np.ravel(start_end_date_temps))

    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)	