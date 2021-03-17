import flask
from flask import request, jsonify
from crawlerWHO import crawlerWHO
import json
from requests.models import Response
from datetime import datetime
from WebScraper import WebScraper
import re

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Weekly Cri Sesh WHO API</h1>
<p>A prototype API for obtaining article data from WHO</p>'''

# testing taking params in the body
@app.route('/some', methods=['GET'])
def api_some():
	response = Response()

	if not request.data:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "No content specifying parameters." }'
	else:
		resp = request.data.decode()
		jsonData = json.loads(resp)

		# no start date
		if not 'startDate' in jsonData:
			response.error_type = "Bad Request"
			response.status_code = 400
			response._content = b'{ "reason" : "No start date." }'
		# no end date
		elif not 'endDate' in jsonData:
			response.error_type = "Bad Request"
			response.status_code = 400
			response._content = b'{ "reason" : "No end date." }'
		# check start date in correct format
		elif not re.findall("[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]", jsonData['startDate']):
			response.error_type = "Bad Request"
			response.status_code = 400
			response._content = b'{ "reason" : "Start date in incorrect format." }'
		# check end date in correct format
		elif not re.findall("[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]", jsonData['endDate']):
			response.error_type = "Bad Request"
			response.status_code = 400
			response._content = b'{ "reason" : "End date in incorrect format." }'
		# check correct order 
		# check either date isn't in the future 
		elif datetime.fromisoformat(jsonData['startDate']) > datetime.fromisoformat(jsonData['endDate']):
			response.error_type = "Bad Request"
			response.status_code = 400
			response._content = b'{ "reason" : "End date before start date." }'
		elif datetime.now() < datetime.fromisoformat(jsonData['startDate']) or datetime.now() < datetime.fromisoformat(jsonData['endDate']):
			response.error_type = "Bad Request"
			response.status_code = 400
			response._content = b'{ "reason" : "Dates are in the future." }'
		else:
			# if there are no keywords then create an empty list
			if not 'keywords' in jsonData:
				keywords = []
			else:
				keywords = [jsonData['keywords']]
			# if there is no location then create an empty list
			if not 'location' in jsonData:
				location = []
			else:
				location = [jsonData['location']]

			# call crawler here
			crawler = crawlerWHO()
			relevantLinks = crawler.searchPage(location, keywords, jsonData['startDate'], jsonData['endDate'])
			# call the scraper here
			scraper = WebScraper("scraper", datetime.now())
			articles = scraper.returnScrapeData(relevantLinks)

			# if there is gibberish in location or disease: 404
			if not articles:
				response.error_type = "Not Found"
				response.status_code = 404
				response._content = b'{ "reason" : "Filtered data for location/disease returned no matching articles." }'
			else:
				response.error_type = "Success"
				response.status_code = 200
				print(type(jsonify(articles)))
				print(type(articles))
				response._content = json.dumps(articles).encode()
	return (response.text, response.status_code, response.headers.items())

app.run()