from flask import Flask

app = Flask(__name__)


### to be used with the home page, not sure if i should put this within the definition
route_list =[
    "/api/v1.0/precipitation",
    "/api/v1.0/stations",
    "/api/v1.0/tobs",
    "/api/v1.0/<start>",
    "/api/v1.0/<start>/<end>"
]

@app.route("/")
def home():
    print("sucessfully reached home page")
    return route_list


@app.route("/api/v1.0/precipitation")
def precipitation():
    print("sucessfully reach the precipitation page")
    return "Convert the query results to a dictionary using date as the key and prcp as the value.Return the JSON representation of your dictionary. "


@app.route("/api/v1.0/stations")
def stations():
    print("sucessfully reached the stations page")
    return "Return a JSON list of stations from the dataset."

@app.route("/api/v1.0/tobs")
def temperature():
    print("sucessfully reached the temperature page")
    return "Query the dates and temperature observations of the most active station for the last year of data.\Return a JSON list of temperature observations (TOBS) for the previous year."


@app.route("/api/v1.0/<start>")
def start_page():
    print("sucessfully reach the start page")
    return "Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date\When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.\When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."

@app.route("/api/v1.0/<start>/<end>")
def startend_page():
    print("sucessfully reach the start_end date page")
    return "Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.\When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.\When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."




if __name__== "__main__":
    app.run(debug=True)