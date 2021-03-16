import mechanicalsoup
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from datetime import datetime

class crawlerWHO:
	def __init__(self):
		self._browser = mechanicalsoup.Browser()
		self._page = self._browser.get("https://www.who.int/csr/don/archive/year/en/")
		self._homeURL = "https://www.who.int"

	@property
	def browser(self):
		return self._browser

	@property
	def page(self):
		return self._page

	@page.setter
	def page(self, p):
		self._page = p

	@property
	def homeURL(self):
		return self._homeURL
	

	def searchPage(self, keywords, startDate, endDate):
		content = self._page.soup.find(id="content")
		content = content.select('a')
		yearLinks = []
		startYear = int(startDate[0:4])
		endYear = int(endDate[0:4])
		startDateObj = datetime.fromisoformat(startDate)
		endDateObj = datetime.fromisoformat(endDate)
		# Isolate the year links
		for link in content:
			address = link["href"]
			if re.search("/csr/don/archive/year/[0-9]{4}/en/", address):
				# Isolate the year links that would have data from the right period
				year = re.findall("[0-9]{4}", address)
				year = int(year[0])
				if year >= startYear and year <= endYear:
					yearLinks.append(self._homeURL + address)
		# Open each year link and return the articles that are relevant
		articleLinks = []
		for yearLink in yearLinks:
			yearPage = self._browser.get(yearLink)
			yearContent = yearPage.soup.find(id="content")
			yearContent = yearContent.select('a')
			# Loop through each link
			for link in yearContent:
				# isolate the articles 
				if re.findall("[0-9]{1,2} [a-zA-Z]{3,9} [0-9]{4}", link.text):
					# isolate date then convert to datetime object
					articleDate = link.text
					articleDateObj = datetime.strptime(articleDate, "%d %B %Y")
					# check if in right time period
					if articleDateObj >= startDateObj and articleDateObj <= endDateObj:
						# if there are no keywords then return all articles within the time period
						if not keywords:
							address = link["href"]
							articleLinks.append(c.homeURL + address)
							print(c.homeURL + address)
						# if there are keywords then filter
						else:
							# loop the element siblings to find the span with the description
							for sibling in link.next_siblings:
								if sibling.name == "span":
									desc = sibling.text
									# loop through each keyword and if there is a match in the description
									# then include link
									for word in keywords:
										if word in desc:
											address = link["href"]
											articleLinks.append(c.homeURL + address)
											print(c.homeURL + address)


c = crawlerWHO()
startDate = "2008-01-01T00:00:00"
endDate = "2009-01-01T00:00:00"
keywords = ["Avian"]
c.searchPage(keywords, startDate, endDate)

# p = c.page.soup
# content = p.find(id='content')
# content = content.select('a')

# startDate = "2021-01-01T00:00:00"
# endDate = "2021-03-16T00:00:00"
# keywords = ["coronavirus"]
# startYear = int(startDate[0:4])
# endYear = int(endDate[0:4])
# startDateObj = datetime.fromisoformat(startDate)
# endDateObj = datetime.fromisoformat(endDate)
# yearLinks = []
# for link in content:
# 	address = link["href"]
# 	if re.search("/csr/don/archive/year/[0-9]{4}/en/", address):
# 		# Isolate the links that would have data from the right period
# 		year = re.findall("[0-9]{4}", address)
# 		year = int(year[0])
# 		if year >= startYear and year <= endYear:
# 			yearLinks.append(c.homeURL + address)
# # Open each year link and return the articles that are relevant
# articleLinks = []
# for yearLink in yearLinks:
# 	yearPage = c.browser.get(yearLink)
# 	yearContent = yearPage.soup.find(id="content")
# 	yearContent = yearContent.select('a')
# 	# Loop through each link
# 	for link in yearContent:
# 		# isolate the articles
# 		if re.findall("[0-9]{1,2} [a-zA-Z]{3,9} [0-9]{4}", link.text):
# 			# isolate date then convert to datetime object
# 			articleDate = link.text
# 			articleDateObj = datetime.strptime(articleDate, "%d %B %Y")
# 			# check if in right time period
# 			if articleDateObj >= startDateObj and articleDateObj <= endDateObj:
# 				# if there are no keywords then return all articles within the time period
# 				if not keywords:
# 					address = link["href"]
# 					print(c.homeURL + address)
# 				# if there are keywords then filter
# 				else:
# 					# loop the element siblings to find the span with the description
# 					for sibling in link.next_siblings:
# 						if sibling.name == "span":
# 							desc = sibling.text
# 							# loop through each keyword and if there is a match in the description
# 							# then include link
# 							for word in keywords:
# 								if word in desc:
# 									address = link["href"]
# 									articleLinks.append(c.homeURL + address)
# 									print(c.homeURL + address)
