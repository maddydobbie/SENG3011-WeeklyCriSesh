import requests
from bs4 import BeautifulSoup

class WebScraper():
    def __init__(self, name, creationTime):
        self.name = name
        self.creationTime = creationTime

    def returnScrapeData(self):
        URL = 'https://www.who.int/csr/don/26-feb-2021-influenza-a-russian-federation/en/'
        page = requests.get(URL)
        pageParse = BeautifulSoup(page.content, 'html.parser')
        print("URL: ", page.url) #url used for date
        title = pageParse.find("meta",property ='og:title')
        print("TITLE: ", title) #title used for country

        print ("Data crawled and returned")