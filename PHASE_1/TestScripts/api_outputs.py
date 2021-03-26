from requests.models import Response
import requests
import json

# testing API outputs
# endpoint at: http://seng3011.pythonanywhere.com/articles
print("-----------------------------------------------------------------")
print("testing: no JSON input")
r = requests.get("http://seng3011.pythonanywhere.com/articles", json={})
print(json.dumps(r.json(), indent=4))

print("-----------------------------------------------------------------")
print("testing: no end date")
r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2020-03-01T00:00:00'})
print(json.dumps(r.json(), indent=4))

print("-----------------------------------------------------------------")
print("testing: 1 week of output")
r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-01-07T00:00:00'})
print(json.dumps(r.json(), indent=4))

print("-----------------------------------------------------------------")
print("testing: location: China")
r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'location':'China'})
print(json.dumps(r.json(), indent=4))

print("-----------------------------------------------------------------")
print("testing: location: Russia")
r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'location':'Russia'})
print(json.dumps(r.json(), indent=4))

print("-----------------------------------------------------------------")
print("testing: keywords: malaria")
r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'keywords':'flu'})
print(json.dumps(r.json(), indent=4))

print("-----------------------------------------------------------------")
print("testing: keywords: fever")
r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'keywords':'fever'})
print(json.dumps(r.json(), indent=4))

print("-----------------------------------------------------------------")
print("testing: keywords: cholera")
r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'keywords':'cholera'})
print(json.dumps(r.json(), indent=4))