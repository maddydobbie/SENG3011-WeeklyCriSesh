import flask
from flask import request, jsonify
from crawlerWHO import crawlerWHO
import json
from requests.models import Response
from datetime import datetime, timedelta
from WebScraper import WebScraper
from dbHandler import dbSave, dbGetLatestDate, dbGetArticles
import re

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Weekly Cri Sesh WHO API</h1>
<p>A prototype API for obtaining article data from WHO v1</p>'''

# testing taking params in the body
@app.route('/articles', methods=['GET'])
def api_articles():
	response = Response()
	response.headers['Access-Control-Allow-Origin']='*'
	# append log file to store the request and request data
	try:
		# switch path for local vs pythonanywhere running
		path = "/home/seng3011/SENG3011-WeeklyCriSesh/PHASE_1/API_SourceCode/logs/"
		# path = "logs/"
		f = open(path + "log.txt", "a")
		now = datetime.now()
		f.write("############################################################\n")
		f.write(str(request) + '\n')
		f.write("Time: " + datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + '\n')
		if not request.args:
			f.write("No request content specifying parameters\n")
		else:
			f.write("Request Query Parameters:\n")
			resp = request.args
			f.write(resp + '\n')
		f.close()
	except:
		print("ERROR: Log File Not Found\nUnable to record request")

	print(request)
	if not request.args:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "No query parameters." }'
	# no start date
	elif not 'startDate' in request.args:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "No start date." }'
		return (response.text, response.status_code, response.headers.items())
	# no end date
	elif not 'endDate' in request.args:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "No end date." }'
		return (response.text, response.status_code, response.headers.items())
	# check start date in correct format
	elif not re.findall("[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]", request.args.get('startDate')):
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "Start date in incorrect format." }'
		return (response.text, response.status_code, response.headers.items())
	# check end date in correct format
	elif not re.findall("[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]",request.args.get('endDate')):
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "End date in incorrect format." }'
		return (response.text, response.status_code, response.headers.items())
	try:
		end = datetime.fromisoformat(request.args.get('endDate'))
	except ValueError:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "End date in incorrect format." }'
		return (response.text, response.status_code, response.headers.items())
	try:
		start = datetime.fromisoformat(request.args.get('startDate'))
	except ValueError:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "Start date in incorrect format." }'
		return (response.text, response.status_code, response.headers.items())

	# check correct order
	# check either date isn't in the future
	if datetime.fromisoformat(request.args.get('startDate')) > datetime.fromisoformat(request.args.get('endDate')):
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "End date before start date." }'
		return (response.text, response.status_code, response.headers.items())
	elif datetime.now() < datetime.fromisoformat(request.args.get('startDate')) or datetime.now() < datetime.fromisoformat(request.args.get('endDate')):
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "Dates are in the future." }'
		return (response.text, response.status_code, response.headers.items())
	else:
		# if there are no keywords then create an empty list
		if not 'keywords' in request.args:
			keywords = []
		else:
			keywords = [request.args.get('keywords')]
		# if there is no location then create an empty list
		if not 'location' in request.args:
			location = []
		else:
			location = [request.args.get('location')]

		# switch path for local vs pythonanywhere running
		pathDB = "/home/seng3011/SENG3011-WeeklyCriSesh/PHASE_1/objects/"
		# pathDB = "../objects/"

		# check if the dates are outside cached data if they are then run the craler and scraper go get
		# articles the arent cached
		dbLastDate = dbGetLatestDate(pathDB + "cache.db")
		if datetime.fromisoformat(request.args.get('endDate')) > dbLastDate:
			# call crawler here
			crawler = crawlerWHO()
			# send the crawler to look for links outside the cached data
			dateSearchFrom = dbLastDate + timedelta(days=1)
			relevantLinks = crawler.searchPage([], [], dateSearchFrom.strftime("%Y-%m-%d"), request.args.get('endDate'))
			# call the scraper here
			scraper = WebScraper("scraper", datetime.now())
			articles = scraper.returnScrapeData(relevantLinks)	
			# save each article individually
			for article in articles:
				cacheDate = article['date_of_publication']
				cacheLocation = cacheKeywords = article['headline']
				dbSave(pathDB + "cache.db", cacheDate, cacheLocation, cacheKeywords, article)
		# access the cache to get all the data to output
		articles = dbGetArticles(pathDB + "cache.db", jrequest.args.get('startDate')), request.args.get('endDate')), location, keywords)
		# if there is gibberish in location or keywords: 404
		if not articles:
			response.error_type = "Not Found"
			response.status_code = 404
			response._content = b'{ "reason" : "Filtered data for location/disease returned no matching articles." }'
		else:
			response.error_type = "Success"
			response.status_code = 200
			response._content = json.dumps(articles).encode()

	try:
		f = open("logs/log.txt", "a")
		f.write("Response Status Code: " + str(response.status_code) + "\n")
		f.close()
	finally:
		return (response.text, response.status_code, response.headers.items())

# comment out for pythonanywhere
#app.run()
