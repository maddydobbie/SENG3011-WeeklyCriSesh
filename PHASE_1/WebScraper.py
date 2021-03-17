import requests
from bs4 import BeautifulSoup
import pickle

class WebScraper():
    def __init__(self, name, creationTime):
        self.name = name
        self.creationTime = creationTime
        with open('objects/symptoms' + '.pkl', 'rb') as f:
            self._symptoms = pickle.load(f)
        with open('objects/diseases' + '.pkl', 'rb') as f:
            self._diseases = pickle.load(f)

    def returnScrapeData(self, links):
        articles = []
        for URL in links:
            page = requests.get(URL)
            pageParse = BeautifulSoup(page.content, 'html.parser')
            print("URL: ", page.url) #url used for date
            title = pageParse.find("meta",property ='og:title')
            print("TITLE: ", title) #title used for country

            print ("Data crawled and returned")
            symptoms = []
            diseases = []
            # isolate the body of the html
            body = pageParse.find(id='primary')
            # loop through each of the children to find each paragraph
            children = body.find_all("p", recursive=False)
            for child in children:
                # loop through each symptom to see if it appears in the paragraph
                # if it does add it to the symptoms list
                for symptom in self._symptoms:
                    if symptom['name'].lower() in child.text.lower():
                        # add if it is not already in the list
                        if symptom['name'].lower() not in symptoms:
                            symptoms.append(symptom['name'].lower())
                # loop through each symptom to see if it appears in the paragraph
                # if it does add it to the symptoms list
                for disease in self._diseases:
                    if disease['name'].lower() in child.text.lower():
                        # add if it is not already in the list
                        if disease['name'].lower() not in diseases:
                            diseases.append(disease['name'].lower())
            articles.append([{"symptoms":symptoms},{"diseases":diseases}])
        return articles