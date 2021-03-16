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


# test route to return everything
@app.route('/all', methods=['GET'])
def api_all():
    return jsonify(data)

# testing taking params in the body
@app.route('/some', methods=['GET'])
def api_some():
	response = request.data.decode()
	json_data = json.loads(response)

	response = Response()

	# no start date
	if not jsonData.has_key('startDate'):
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "No start date." }'
		return response
	# no end date
	if not jsonData.has_key('endDate'):
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "No end date." }'
		return response
	# check start date in correct format
	try:
		startDateObj = datetime.fromisoformat(jsonData["startDate"])
	except:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "Start date in incorrect format." }'
		return response
	# check end date in correct format
	try:
		endDateObj = datetime.fromisoformat(jsonData["endDate"])
	except:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "End date in incorrect format." }'
		return response
	# check correct order 
	# check either date isn't in the future 
	if startDateObj > endDateObj:
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "End date before start date." }'
		return response
	if isfutureDate(startDateObj) or isfutureDate(endDateObj):
		response.error_type = "Bad Request"
		response.status_code = 400
		response._content = b'{ "reason" : "Dates are in the future." }'
		return response

	# call crawler here

	# if there is gibberish in location or disease: 404
	if "GIBBERISH":
		response.error_type = "Not Found"
		response.status_code = 404
		response._content = b'{ "reason" : "Filtered data for location/disease returned no matching articles." }'
		return response
	
	response.error_type = "Success"
	response.status_code = 200
	response._content = b'{ "_" : "_" }'
	
	return response

    scraper = WebScraper("webScraper", datetime.now())
    scraper.returnScrapeData()
    return jsonify(request.data.decode("utf-8"))
app.run()