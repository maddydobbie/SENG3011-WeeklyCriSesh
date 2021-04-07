import mechanicalsoup
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from datetime import datetime

class crawlerWHO:
	def __init__(self):
		self._browser = mechanicalsoup.Browser()
		self._page = self._browser.get("https://www.who.int/emergencies/disease-outbreak-news")
		self._homeURL = "https://www.who.int/emergencies/disease-outbreak-news"

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

	def incrementUrl(self,n):
		self._page = self._browser.get("https://www.who.int/emergencies/disease-outbreak-news"+"/"+str(n))

	def checkEmptyPage(self,content):
		content = content.select('a')
		if len(content) < 5:
			return True
		else:
			return False

	

	def searchPage(self, location, keywords, startDate, endDate):
		yearLinks = []
		startYear = int(startDate[0:4])
		endYear = int(endDate[0:4])
		startDateObj = datetime.fromisoformat(startDate)
		endDateObj = datetime.fromisoformat(endDate)


		n = 1
		while(True):
			content = self._page.soup.find(id="PageContent_C010_Col00")
			if self.checkEmptyPage(content) == True:
				for year in yearLinks:
					print(year)
				return yearLinks
			content = content.select('a')
			# isolate each link to check date
			for link in content:
				address = link["href"]
				#isolate date in each link
				children = link.findChildren("span")
				for child in children:
					if re.search("[0-9]{1,2}[ ][A-Z][a-z]+[ ][0-9]{4}", child.text):
						webDate = re.findall("[0-9]{1,2}[ ][A-Z][a-z]+[ ][0-9]{4}", child.text)
						webDate = str(webDate[0])
						webDate = datetime.strptime(webDate, '%d %B %Y')
						webDate = webDate.isoformat()

						#check if date in range and add to year links

						if startDate <= webDate:
							if webDate <= endDate:
								yearLinks.append(address)
						else:
							for year in yearLinks:
								print(year)
							return yearLinks
			n += 1
			self.incrementUrl(n)
		return yearLinks

c = crawlerWHO()
links = c.searchPage("China","covid","2021-02-10T00:00:00","2021-04-27T00:00:00")