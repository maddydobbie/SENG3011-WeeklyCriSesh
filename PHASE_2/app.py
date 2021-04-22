from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime, timedelta
import sqlite3
import requests

app = Flask(__name__)
app.config["DEBUG"] = True

'''
Dedicated page for "page not found"
'''
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404


'''
 Home Start Page
'''
@app.route("/", methods=['POST', 'GET'])
def home():
	return render_template('index.html')

@app.route("/index.html", methods=['POST', 'GET'])
def homeReroute():
	return render_template('index.html')

@app.route("/about.html", methods=['POST', 'GET'])
def about():
	return render_template('about.html')

@app.route("/apiDocs.html", methods=['POST', 'GET'])
def apiDocs():
	return render_template('apiDocs.html')

@app.route("/searchFlights", methods=['POST', 'GET'])
def searchNews():
	if request.method == "GET":
		return render_template('searchNews.html', flightFlag=0)
	else:
		flightList = []
		origin = request.form.get("origin")
		dest = request.form.get("destination")
		start = request.form.get("start")
		end = request.form.get("end")

		print(type(start))
		print(end)


		# convert city to IATA code
		with open("./static/json/airports.json") as json_file:
			airportsJSON = json.load(json_file)
		airports = []
		for a in list(airportsJSON.values()):
			airports.append({"city":a["city"], "iata":a["iata"], "country":a["country"]})
		
		originCode = destCode = ""
		for d in airports:
		
			if d["city"].lower() == origin.lower():
				originCode = d["iata"].upper()
				break
		for d in airports:
			if d["city"].lower() == dest.lower():
				destCode = d["iata"].upper()
				break

		if originCode == "" or destCode == "":
			return render_template('searchNews.html', flightFlag=3)

		url = "https://api.travelpayouts.com/v1/prices/cheap"
		querystring = {"origin":originCode,"destination":destCode,"depart_date":start,"return_date":end,"currency":"AUD"}
		headers = {'x-access-token': 'c4ae3203facd6e9ea55b3f7f3cf03cd6'}
		
		response = requests.request("GET", url, headers=headers, params=querystring)

		flights = response.json()["data"]
		if not flights:
			return render_template('searchNews.html', flights=flightList, origin=origin, dest=dest, flightFlag=2)
		for key, value in flights.items():
			for flightID, flightValues in flights.get(key).items():
				flightNum = flightValues.get("airline")+str(flightValues.get("flight_number"))
				f = {"price":flightValues.get("price"),"flight_number":flightNum,"depart_date":flightValues.get("departure_at"),"return_date":flightValues.get("return_at")}
				flightList.append(f)

		return render_template('searchNews.html', flights=flightList, origin=origin, dest=dest, flightFlag=1)

@app.route("/outbreakMap", methods=['POST', 'GET'])
def outbreakMap():
	return render_template('outbreakMap.html')

@app.route("/nearMe.html", methods=['POST', 'GET'])
def nearMe():
	return render_template('nearMe.html')

app.run()