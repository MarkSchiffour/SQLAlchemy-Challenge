import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"After the slash enter the date that you want the min, avg, and max temperature observations for<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"After the slash enter the start date followed by another slash '/' then the end date that you want the min, avg, and max temperature observations for"
    )

@app.route("/api/v1.0/percipitation")
def precipitation():
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    # Calculate the date one year from the last date in data set.
    previous = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the date and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous).all()

    # dictionary with the date as the key and the precipitation as the value
    precip = {date: prcp for date, prcp in results}
    
    session.close()
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Design a query to show all of the stations available in this dataset
    Stations_All = session.query(Station.station).all()

    # inravel the results into a list
    stations = list(np.ravel(Stations_All))

    session.close()
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Returns a list of amounts of tobs with dates"""
    # Query all tobs
    Previous = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= Previous).filter(Measurement.date <= '2017-08-23').order_by(Measurement.date).all()
    tobs_dict= {date:tobs for date,tobs in results}

    session.commit()

    # Convert list of tuples into normal list
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def startOnly(start):
    day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.commit()

    # Convert list of tuples into normal list
    return jsonify(day_temp_results)

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    multi_day_temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.commit()

    # Convert list of tuples into normal list
    return jsonify(multi_day_temp_results)

if __name__ == '__main__':
    app.run(debug=True)