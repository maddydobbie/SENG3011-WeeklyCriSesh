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

	scraper = WebScraper("webScraper", datetime.now())
	scraper.returnScrapeData()
	return jsonify(request.data.decode("utf-8"))

app.run()