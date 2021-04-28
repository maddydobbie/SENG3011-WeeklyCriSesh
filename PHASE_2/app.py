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

@app.route("/planTrip", methods=['POST', 'GET'])
def planTrip():
	if request.method == "GET":
		return render_template('searchFlights.html', flightFlag=0, riskScore=0)
	else:
		flightList = []
		origin = request.form.get("origin")
		dest = request.form.get("destination")
		start = request.form.get("start")

		# convert city to IATA code
		with open("./static/json/airports.json") as json_file:
			airportsJSON = json.load(json_file)
		airports = []
		for a in list(airportsJSON.values()):
			airports.append({"city":a["city"], "iata":a["iata"], "country":a["country"]})
		
		#get the corresponding codes for the origin and dest cities		
		originCode = ""
		for d in airports:
			if d["city"].lower() == origin.lower():
				originCode = d["iata"].upper()
				break
		destAirports = []
		for d in airports:
			if d["city"].lower() == dest.lower():
				destAirports.append({"dest_code":d["iata"].upper(), "dest_city":d["city"].title(), "dest_country":d["country"]})
		# THIS IS THE CODE FOR IMPLEMENTING ALL CITIES FROM A COUNTRY
		# # if the destCity has returned no match check if it is a country
		# if not destAirports:
		# 	for d in airports:
		# 		if d["country"].lower() == dest.lower():
		# 			destAirports.append({"dest_code":d["iata"].upper(), "dest_city":d["city"].title(), "dest_country":d["country"]})
		print(destAirports)
		if originCode == "" or not destAirports:
			return render_template('searchFlights.html', flightFlag=3, riskScore=0)

		for destAirport in destAirports:
			url = "https://api.travelpayouts.com/v1/prices/cheap"
			querystring = {"origin":originCode,"destination":destAirport.get("dest_code"),"depart_date":start,"currency":"AUD"}
			headers = {'x-access-token': 'c4ae3203facd6e9ea55b3f7f3cf03cd6'}
			
			response = requests.request("GET", url, headers=headers, params=querystring)

			flights = response.json()["data"]
			print(flights)
			if not flights:
				continue
			for key, value in flights.items():
				for flightID, flightValues in flights.get(key).items():
					flightNum = flightValues.get("airline")+str(flightValues.get("flight_number"))
					# edit dates to make them readable
					departDateOG = datetime.strptime(flightValues.get("departure_at"), "%Y-%m-%dT%H:%M:%SZ")
					departTime = departDateOG.strftime("%H:%M")
					departDay = departDateOG.strftime("%A") + " "
					departDate = departDateOG.strftime("%d %B %Y")
					if int(departDate[1]) in [1,2,3] and int(departDate[0:2]) not in [11,12,13]:
						if departDate[1] == "1":
							departDate = departDate[0:2] + "st" + departDate[2:]
						elif departDate[1] == "2":
							departDate = departDate[0:2] + "nd" + departDate[2:]
						else:
							departDate = departDate[0:2] + "rd" + departDate[2:]
					else:
						departDate = departDate[0:2] + "th" + departDate[2:]
					if departDate[0] == "0":
						departDate = departDay + departDate[1:]
					else:
						departDate = departDay + departDate
					# create a dictionary for all the relevant flight data
					f = {"price":flightValues.get("price"),"flight_number":flightNum,"depart_date_OG": departDateOG, "depart_date":departDate,"depart_time":departTime, "destination":destAirport.get("dest_city")}
					flightList.append(f)
			# remove duplicates from the list occurs due to a bug in the API
			flightList = [dict(t) for t in {tuple(d.items()) for d in flightList}]
			# sort the list by depature date
			flightList = sorted(flightList, key=lambda i: i.get("depart_date_OG"))
		
		# if there are no flights then dont bother with a risk score
		if not flightList:
			return render_template('searchFlights.html', flights=flightList, origin=origin.title(), dest=dest.title(), flightFlag=2, riskScore=0)
		
		# do WHOAPI call to get warnings for potential outbreaks. at the destination
		url = "http://seng3011.pythonanywhere.com/articles"
		endDate = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d") + "T00:00:00"
		startDate = (datetime.now() - timedelta(weeks=52)).strftime("%Y-%m-%d") + "T00:00:00"
		querystring = {"startDate":startDate,"endDate":endDate, "location":destAirports[0].get("dest_country")}
		r = requests.request("GET", url, params=querystring)
		# if there is data in the response then identify how recent it was and calculate risk score
		currentRiskScore = 0
		articles = []
		if r.status_code == 200:
			articles = r.json()
			currDate = datetime.now()
			# analyse the data to find calculate a risk score
			# risk score of 10 or above is high risk
			# risk score between 3 and 10 is medium risk
			# risk score between 0 and 3 is low risk 
			# risk score of 0 is safe
			for article in articles:
				date = datetime.strptime(article.get("date_of_publication")[0:10], "%Y-%m-%d")
				month = int(date.strftime("%m"))
				# gives a minimum score of 1 for an incident 12 months ago up to a max of 13 for an
				# incident this month
				currentRiskScore += 13 - ((currDate.year - date.year) * 12 + currDate.month - date.month)
		# get individual riskScores for each flight dependent on their date
		for flight in flightList:
			date = flight.get("depart_date_OG")
			cumulativeRiskScore = 0
			for article in articles:
				articleDate = datetime.strptime(article.get("date_of_publication")[0:10], "%Y-%m-%d")
				riskScore = 13 - ((date.year - articleDate.year) * 12 +  date.month - articleDate.month)
				if riskScore < 0:
					riskScore = 0
				cumulativeRiskScore += riskScore
			flight.update({"risk_score": cumulativeRiskScore})	
		return render_template('searchFlights.html', flights=flightList, origin=origin.title(), dest=dest.title(), flightFlag=1, riskScore=currentRiskScore, articles=articles)

@app.route("/outbreakMap", methods=['POST', 'GET'])
def outbreakMap():
	return render_template('outbreakMap.html')

app.run()