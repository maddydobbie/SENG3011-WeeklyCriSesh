import requests
from bs4 import BeautifulSoup
import pickle
import re
from datetime import datetime

class WebScraper():
    def __init__(self, name, creationTime):
        self.name = name
        self.creationTime = creationTime
        with open('objects/symptoms' + '.pkl', 'rb') as f:
            self._symptoms = pickle.load(f)
        with open('objects/diseases' + '.pkl', 'rb') as f:
            self._diseases = pickle.load(f)

    def checkRegexString(self, regexString, text):
        if (re.search(regexString, text)):
            return True
        else:
            return False

    def getDateFromRegex(self, regexString, text):
        dateText = re.search(regexString, text)[0] #extracting the date from the text
        #Lists for different months
        monthFullList = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
        monthShortList = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "SEP", "OCT", "NOV", "DEC"]
        #if date format is in the form DD Month (in words) YYYY
        dateString = ""
        if (self.checkRegexString(r"[0-9]{2}-[a-z]+-[0-9]+", text)):
            day = (re.search("[0-9]{2}", dateText))[0]
            month = (re.search("[a-zA-Z]{3,}", dateText))[0].upper()
            year = (re.search("[0-9]{4}", dateText))[0]
            #extracting month of different formats (e.g. Feb vs February)
            if (month in monthFullList):
                index = monthFullList.index(month)
            elif (month in monthShortList):
                index = monthShortList.index(month)
            month = monthFullList[index]
            #combining all information

        elif (self.checkRegexString(r"[0-9]{4}_[0-9]{2}_[0-9]{2}", text)):
            #attaining all info in YYYY_MM_DD format
            year = (re.search("[0-9]{4}", dateText))[0]
            monthIndex = (re.search("_[0-9]{2}_", dateText))[0]
            monthIndex = int(monthIndex[1:-1]) - 1
            month = monthFullList[monthIndex]
            day = (re.search("[0-9]{2}$", dateText))[0]

        dateString += day + ' ' + month + ' ' + year
        return dateString

    def checkDate(self, URL):
        if (self.checkRegexString(r"[0-9]{2}-[a-z]+-[0-9]+", URL)):
            Date = self.getDateFromRegex(r"[0-9]{2}-[a-z]+-[0-9]+", URL)
        elif (self.checkRegexString(r"[0-9]{4}_[0-9]{2}_[0-9]{2}",URL)):
            Date = self.getDateFromRegex(r"[0-9]{4}_[0-9]{2}_[0-9]{2}", URL)
        else:
            Date = "Could not be found"
        return Date

    def checkCountry(self, title):
        if (self.checkRegexString(r"in\s[a-zA-z\s]*", title)):
            country = (re.search(r"in\s[a-zA-z\s]*", title))[0]
            country = country[3:]
        elif (self.checkRegexString(r"– .+", title)):
            country = (re.search(r"– .+", title))[0]
            country = country[2:]
        else:
            print("Country cannot be found")
            country = "Cannot be found."
        return country

    def checkSymptomsAndDiseases(self, pageParse):
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
        return symptoms, diseases

    def getBody(self, pageParse):
        bodyText = ""
        # isolate the body of the html
        try:
            body = pageParse.find(id='primary')
            body = body.find_all(['h3','p'], recursive=False)
            for child in body:
                if child.name == "h3":
                    break
                elif child.name == "p":
                    bodyText = bodyText + child.text
                else:
                    continue
        finally:
            return bodyText

    def getEventDate(self, body):
        dates = re.findall("[0-9]{1,2} [JFMASOND][aepuco][nbrylgptvc][urcieyut]?[auhlsebm]?[ratmeb][yrbe]?[yer]?[r]?[,]? [1-2][0-9]{3}", body)
        if dates:
            return dates[0].replace(",", "")
        else:
            return "Not Found"

    def returnScrapeData(self, links):
        articles = []
        for URL in links:
            page = requests.get(URL)
            pageParse = BeautifulSoup(page.content, 'html.parser')

            pageURL = page.url #url used for date
            title = (pageParse.find_all(class_="headline")[0]).text
            dateString = self.checkDate(pageURL)
            country = self.checkCountry(title).strip()
            symptoms, diseases = self.checkSymptomsAndDiseases(pageParse)

            mainText = self.getBody(pageParse)

            eventDate = self.getEventDate(mainText)

            reports = [{"diseases":diseases,"syndromes":symptoms,"event_date":eventDate,"locations":[country]}]
            articles.append({"url":pageURL,"date_of_publication":dateString,"headline":title,"datetime_accessed":datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),"data_gathered_by":"Weekly_Cri_Sesh","main_text":mainText,"reports":reports})
        return articles