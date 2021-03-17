import flask
from flask import request, jsonify
from crawlerWHO import crawlerWHO
import json
from requests.models import Response
from datetime import datetime
from WebScraper import WebScraper

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# TEST DATA
data = [
    {'id': 0, 'title': 'Swine Flu'},
    {'id': 1, 'disease': 'Coronavirus'}
]


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Weekly Cri Sesh WHO API</h1>
<p>A prototype API for obtaining article data from WHO</p>'''

# testing taking params in the body
@app.route('/some', methods=['GET'])
def api_some():

	resp = request.data.decode()
	jsonData = json.loads(resp)

	response = Response()

	# no start date
	if not 'startDate' in jsonData:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "No start date." }'
		return (response.text, response.status_code, response.headers.items())
	# no end date
	if not 'endDate' in jsonData:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "No end date." }'
		return (response.text, response.status_code, response.headers.items())
	# check start date in correct format
	print(jsonData["startDate"])
	print(type(jsonData["startDate"]))
	startDateObj = datetime.fromisoformat(jsonData["startDate"])
	print(startDateObj)
	try:
		print(jsonData["startDate"])
		print(type(jsonData["startDate"]))
		startDateObj = datetime.fromisoformat(jsonData["startDate"])
		print(startDateObj)
	except:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "Start date in incorrect format." }'
		return (response.text, response.status_code, response.headers.items())
	# check end date in correct format
	try:
		endDateObj = datetime.fromisoformat(jsonData["endDate"])
	except:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "End date in incorrect format." }'
		return (response.text, response.status_code, response.headers.items())
	# check correct order 
	# check either date isn't in the future 
	if startDateObj > endDateObj:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "End date before start date." }'
		return (response.text, response.status_code, response.headers.items())
	if datetime.now() < startDateObj or datetime.now() < endDateObj:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "Dates are in the future." }'
		return (response.text, response.status_code, response.headers.items())
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
		return (response.text, response.status_code, response.headers.items())
	else:
		response.error_type = "Success"
		response.status_code = 200
		print(type(jsonify(articles)))
		print(type(articles))
		response._content = json.dumps(articles).encode()
		return (response.text, response.status_code, response.headers.items())
	return jsonify("{'Maddy':'Yeah'}")

app.run()