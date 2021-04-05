import sqlite3
import json
from datetime import datetime

def dbSave(dbName, date, location, keywords, jsonOutput):
	conn = sqlite3.connect(dbName)
	jsonDouble = json.dumps(jsonOutput).replace("'","''")
	conn.execute("INSERT INTO ARTICLE (DATE, LOCATION, KEYWORDS, REPORTS) VALUES ('{date}', '{location}', '{keywords}', '{reports}')".format(date=date[0:10], location=location, keywords=keywords, reports=jsonDouble))
	conn.commit()
	conn.close()

def dbGetLatestDate(dbName):
	conn = sqlite3.connect(dbName)
	curr = conn.execute("SELECT DATE FROM ARTICLE ORDER BY DATE DESC LIMIT 1")
	date = curr.fetchall()
	if date:
		date = date[0][0]
	else:
		date = "1996-01-21"
	conn.close()
	return datetime.strptime(date, "%Y-%m-%d")

def dbGetArticles(dbName, startDate, endDate, location, keywords):
	conn = sqlite3.connect(dbName)
	# if there is no location or keywords
	if not location and not keywords:
		curr = conn.execute("SELECT REPORTS FROM ARTICLE WHERE DATE >= '{startDate}' AND DATE <= '{endDate}' ORDER BY DATE DESC".format(startDate=startDate[0:10], endDate=endDate[0:10]))
	# if there is location but no keywords
	elif location and not keywords:
		curr = conn.execute("SELECT REPORTS FROM ARTICLE WHERE DATE >= '{startDate}' AND DATE <= '{endDate}' AND LOCATION LIKE ? ORDER BY DATE DESC".format(startDate=startDate[0:10], endDate=endDate[0:10]), ('%'+location[0]+'%',))
	# if there is keywords but no location
	elif location and not keywords:
		curr = conn.execute("SELECT REPORTS FROM ARTICLE WHERE DATE >= '{startDate}' AND DATE <= '{endDate}' AND KEYWORDS LIKE ? ORDER BY DATE DESC".format(startDate=startDate[0:10], endDate=endDate[0:10]), ('%'+keywords[0]+'%',))	
	# if there is location and keywords
	else:
		curr = conn.execute("SELECT REPORTS FROM ARTICLE WHERE DATE >= '{startDate}' AND DATE <= '{endDate}' AND LOCATION LIKE ? AND KEYWORDS LIKE ? ORDER BY DATE DESC".format(startDate=startDate[0:10], endDate=endDate[0:10]), ('%'+location[0]+'%','%'+keywords[0]+'%'))	
	# pull the articles out of the db cursor and restore their proper json format
	articles = []
	for article in curr.fetchall():
		articles.append(article[0])
	return articles