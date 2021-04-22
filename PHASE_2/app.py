from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime, timedelta
import sqlite3

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

@app.route("/searchNews.html", methods=['POST', 'GET'])
def searchNews():
	return render_template('searchNews.html')

@app.route("/nearMe.html", methods=['POST', 'GET'])
def nearMe():
	return render_template('nearMe.html')

app.run()