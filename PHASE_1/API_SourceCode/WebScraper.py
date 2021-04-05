import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json

class WebScraper():
    def __init__(self, name, creationTime):
        self.name = name
        self.creationTime = creationTime
        # switch path for local vs pythonanywhere running
        # path = "/home/seng3011/SENG3011-WeeklyCriSesh/PHASE_1/objects/"
        path = "../objects/"
        with open(path + '/symptoms.txt') as json_file:
            self._symptoms = json.load(json_file)
        with open(path + 'diseases.txt') as json_file:
            self._diseases = json.load(json_file)
        with open(path + 'cities.txt') as json_file:
            self._cities = json.load(json_file)
        with open(path + 'countries.txt') as json_file:
            self._countries = json.load(json_file)

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
            date = self.getDateFromRegex(r"[0-9]{2}-[a-z]+-[0-9]+", URL)
            date = datetime.strptime(date.title(), "%d %B %Y").strftime("%Y-%m-%d") + " xx:xx:xx"
        elif (self.checkRegexString(r"[0-9]{4}_[0-9]{2}_[0-9]{2}",URL)):
            date = self.getDateFromRegex(r"[0-9]{4}_[0-9]{2}_[0-9]{2}", URL)
            date = datetime.strptime(date.title(), "%d %B %Y").strftime("%Y-%m-%d") + " xx:xx:xx"
        else:
            date = "Could not be found"
        return date

    def checkCountry(self, title):
        if (self.checkRegexString(r"in\s[a-zA-z\s]*", title)):
            country = (re.search(r"in\s[a-zA-z\s]*", title))[0]
            country = country[3:]
        elif (self.checkRegexString(r"– .+", title)):
            country = (re.search(r"– .+", title))[0]
            country = country[2:]
        else:
            country = "Cannot be found."
        return country

    #check countries and cities
    def checkCountriesAndCities(self, body, country):
        countries = []
        cities = []
        for country in self._countries:
            if country['name'] in body:
                # add if it is not already in the list
                if country['name'] not in countries:
                    countries.append(country['name'])
        # loop through each country to see if it appears in the paragraph
        # if it does add it to the country list
        for city in self._cities:
            if city['name'] in body:
                # add if it is not already in the list
                if city['name'] not in cities:
                    cities.append(city['name'])
        if not countries:
            countries.append(country)
        return countries, cities

    def checkSymptomsAndDiseases(self, body):
        symptoms = []
        diseases = []
        for symptom in self._symptoms:
            if symptom['name'].lower() in body.lower():
                # add if it is not already in the list
                if symptom['name'].lower() not in symptoms:
                    symptoms.append(symptom['name'].lower())
        # loop through each symptom to see if it appears in the paragraph
        # if it does add it to the symptoms list
        for disease in self._diseases:
            if disease['name'].lower() in body.lower():
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

    def getEventDate(self, body, date):
        dates = re.findall("[0-9]{1,2} [JFMASOND][aepuco][nbrylgptvc][urcieyut]?[auhlsebm]?[ratmeb][yrbe]?[yer]?[r]?[,]? [1-2][0-9]{3}", body)
        if dates:
            dateObjs = []
            for date in dates:
                # if the month is Sept then fix it September
                if date.split(" ")[1] == "Sept":
                    date = date.split(" ")[0] + " September " + date.split(" ")[2]
                dateObjs.append(datetime.strptime(date.replace(",",""),"%d %B %Y"))
            dateObjs.sort()
            if len(dateObjs) > 1 and dateObjs[0].strftime("%Y-%m-%d") != dateObjs[-1].strftime("%Y-%m-%d"):
                dateRange = dateObjs[0].strftime("%Y-%m-%d") + " xx:xx:xx to " + dateObjs[-1].strftime("%Y-%m-%d") + " xx:xx:xx"
                return dateRange
            else:
                return dateObjs[0].strftime("%Y-%m-%d") + " xx:xx:xx"
        else:
            return date

    def getReports(self, country, body, date):
        reports = []
        last = [0, 0]
        # get a iterator of all matches
        dateMatches = re.finditer("[0-9]{1,2} [JFMASOND][aepuco][nbrylgptvc][urcieyut]?[auhlsebm]?[ratmeb][yrbe]?[yer]?[r]?[,]? [1-2][0-9]{3}", body)
        # iterate through all the date matches
        for match in dateMatches:
            s = match.start()
            e = match.end()
            # if not the first iteration try find a disease in the space between the dates
            for disease in self._diseases:
                if disease['name'].lower() in body[last[1]:s].lower():
                    symptoms, diseases = self.checkSymptomsAndDiseases(body[last[1]:s])
                    countries, cities = self.checkCountriesAndCities(body[last[1]:s], country)
                    locations = {"country":countries[0], "locations":cities}
                    eventDate = self.getEventDate(body[last[1]:s], date)
                    reports.append({"diseases":diseases,"syndromes or symptoms":symptoms,"event_date":eventDate,"locations":locations})
                    last = [s, e]
        # if there is only one match then there is only one date so process the report on the entire body of team
        if len(reports) <= 1:
            symptoms, diseases = self.checkSymptomsAndDiseases(body)
            countries, cities = self.checkCountriesAndCities(body, country)
            locations = {"country":countries[0], "locations":cities}
            eventDate = self.getEventDate(body, date)
            reports.append({"diseases":diseases,"syndromes or symptoms":symptoms,"event_date":eventDate,"locations":locations})
        return reports



    def returnScrapeData(self, links):
        articles = []
        print(len(links))
        i = 0
        for URL in links:
            print(i)
            page = requests.get(URL)
            pageParse = BeautifulSoup(page.content, 'html.parser')

            pageURL = page.url #url used for date
            title = (pageParse.find_all(class_="headline")[0]).text
            dateString = self.checkDate(pageURL)
            mainText = self.getBody(pageParse)

            country = self.checkCountry(title).strip()
            reports = self.getReports(country, mainText, dateString)

            articles.append({"url":pageURL,"date_of_publication":dateString,"headline":title,"datetime_accessed":datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),"data_gathered_by":"Weekly_Cri_Sesh","main_text":mainText,"reports":reports})
            i += 1
        return articles
