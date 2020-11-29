from flask import Flask, jsonify
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


############## review class notes on session.close to make sure this is set up right



## set up engine and connection, not sure if connection is needed
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine,reflect=True)

##### ---- not sure if I need this needed
# Base.metadata.create_all(conn)


# Save references to each table
mt = Base.classes.measurement
st = Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)


###create the app
app = Flask(__name__)

### gives the date range to use for a given station number in the "first_date,last_date" format
def first_last_date(station_num):
    last_date = dt.datetime.strptime(session.query(mt.date,mt.tobs).filter(mt.station==station_num).order_by(mt.date.desc()).all()[0][0],'%Y-%m-%d')
    first_date = last_date - dt.timedelta(days=365)
    return(first_date,last_date)


### to be used with the home page
route_list =[
    "/api/v1.0/precipitation",
    "/api/v1.0/stations",
    "/api/v1.0/tobs",
    "/api/v1.0/<start>",
    "/api/v1.0/<start>/<end>"
]
#### defining the homepage
@app.route("/")
def home():
    print("sucessfully reached home page")
    return jsonify(route_list)




#### query to get the date and preciptation for 
prec=dict(engine.execute('SELECT date,prcp FROM measurement').fetchall())
######## defining the precipitation page
#### this page has a button  to select "raw" or "parsed", not sure why this is
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("sucessfully reach the precipitation page")
    return jsonify(prec)



#### gets the station id and name  for the stations page
station=dict(engine.execute("SELECT station,name FROM station").fetchall())
#### definig the stations page
@app.route("/api/v1.0/stations")
def stations():
    print("sucessfully reached the stations page")
    return jsonify(station)


### define the station id for the top 
top_station_id = "USC00519281"

### find the first and last date we'll be using for the temperature page query
top_first_date, top_last_date = first_last_date(top_station_id)

### query to get the last year of data for the top station
temp_page_result = dict(session.query(mt.date,mt.tobs).filter(mt.station==top_station_id,mt.date>top_first_date).all())

@app.route("/api/v1.0/tobs")
def temperature():
    print("sucessfully reached the temperature page")
    return jsonify(temp_page_result)





# @app.route("/api/v1.0/<start>")
# def start_page():
#     print("sucessfully reach the start page")
#     return "Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date\When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.\When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."

# @app.route("/api/v1.0/<start>/<end>")
# def startend_page():
#     print("sucessfully reach the start_end date page")
#     return "Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.\When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.\When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."




if __name__== "__main__":
    app.run(debug=True)