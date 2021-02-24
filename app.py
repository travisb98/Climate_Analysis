from flask import Flask, jsonify
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func




## set up engine and connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine,reflect=True)




# Save references to each table
mt = Base.classes.measurement
st = Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)


###create the app
app = Flask(__name__)


#### defining the homepage
@app.route("/")
def home():
    print("sucessfully reached home page")

    route_dict={
    "Lists the precipitation by date":"/api/v1.0/precipitation",
    "Lists station names and their ID's":"/api/v1.0/stations",
    "Lists the last year of temperature data for the most active station":"/api/v1.0/tobs",
    "Returns the Average, Minimum and Maximum Temperature for all dates including and beyond the start date ":"/api/v1.0/<start>",
    "Returns the Average, Minimum and Maximum Temperature for the date range":"/api/v1.0/<start>/<end>",
    }

    return jsonify(route_dict)


#### defining the precipitation page
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("sucessfully reach the precipitation page")
    #### query to get the date and preciptation
    prec=dict(engine.execute('SELECT date,prcp FROM measurement').fetchall())
    return jsonify(prec)


#### definig the stations page
@app.route("/api/v1.0/stations")
def stations():
    print("sucessfully reached the stations page")
    #### gets the station id and name  for the stations page
    station=dict(engine.execute("SELECT station,name FROM station").fetchall())
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def temperature():
    print("sucessfully reached the temperature page")
    ### define the station id for the top 
    top_station_id = "USC00519281"

    ### gives the date range to use for a given station number in the "first_date,last_date" format
    top_last_date = dt.datetime.strptime(session.query(mt.date,mt.tobs).filter(mt.station==top_station_id).order_by(mt.date.desc()).all()[0][0],'%Y-%m-%d')
    top_first_date = top_last_date - dt.timedelta(days=365)

    ### query to get the last year of data for the top station
    temp_page_result = dict(session.query(mt.date,mt.tobs).filter(mt.station==top_station_id,mt.date>top_first_date).all())
    session.close()
    return jsonify(temp_page_result)


@app.route("/api/v1.0/<start>")
def start_page(start):
    print("sucessfully reach the start page")
    start_date=str(start)

    spr_max=engine.execute(f'SELECT MAX(measurement.tobs) FROM measurement WHERE measurement.date>{start_date}').fetchall()[0][0]
    spr_min=engine.execute(f'SELECT MIN(measurement.tobs) FROM measurement WHERE measurement.date>{start_date}').fetchall()[0][0]
    spr_avg=round(engine.execute(f'SELECT AVG(measurement.tobs) FROM measurement WHERE measurement.date>{start_date}').fetchall()[0][0],2)

    start_page_results_dict = {
        "Average":spr_avg,
        "Max":spr_max,
        "Min":spr_min
    }

    return jsonify(start_page_results_dict)

@app.route("/api/v1.0/<start>/<end>")
def startend_page(start,end):
    print("sucessfully reach the start_end date page")
    start_date=start
    end_date=end

    all_dates=engine.execute('SELECT measurement.date FROM measurement').fetchall()
    max_date_available=engine.execute('SELECT MAX(measurement.date) FROM measurement').fetchall()[0][0]
    min_date_available=engine.execute('SELECT MIN(measurement.date) FROM measurement').fetchall()[0][0]
 
    #clean up the all_dates list
    all_dates= [x[0] for x in all_dates]


    ### returns the results if the dates entered are within data
    if dt.datetime.strptime(start,'%Y-%m-%d') and dt.datetime.strptime(end,'%Y-%m-%d') in [dt.datetime.strptime(str(x),'%Y-%m-%d') for x in all_dates]:
        r_max=session.query(mt.tobs).filter(mt.date>=start_date,mt.date<=end_date).order_by(mt.tobs.desc()).first()[0]
        r_min=session.query(mt.tobs).filter(mt.date>=start_date,mt.date<=end_date).order_by(mt.tobs.asc()).first()[0]
        r_avg=round(session.query(func.avg(mt.tobs)).filter(mt.date>=start_date,mt.date<=end_date).order_by(mt.tobs.desc()).all()[0][0],2)
        session.close()
        start_end_results_dict = {
        "Average":r_avg,
        "Max":r_max,
        "Min":r_min
        }  

        return jsonify(start_end_results_dict)

    else:
        ### prints out the available date range if used enters date beyond data
        return f'your range must be between {min_date_available} and {max_date_available}'


if __name__== "__main__":
    app.run(debug=True)