from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime, timedelta
import sqlite3
import requests
#import wikipedia
#import requests

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
		return render_template('searchNews.html')
	else:
		origin = request.form.get("origin")
		dest = request.form.get("destination")

		url = "https://api.travelpayouts.com/v1/prices/cheap"
		querystring = {"origin":origin,"destination":dest,"depart_date":"2021-05","return_date":"2021-12","currency":"AUD"}
		headers = {'x-access-token': 'c4ae3203facd6e9ea55b3f7f3cf03cd6'}
		
		response = requests.request("GET", url, headers=headers, params=querystring)

		flights = json.dumps(response.json(), indent=4)
		print(flights)
		
		return render_template('searchNews.html', flights=flights)

@app.route("/nearMe.html", methods=['POST', 'GET'])
def nearMe():
	return render_template('nearMe.html')

app.run()