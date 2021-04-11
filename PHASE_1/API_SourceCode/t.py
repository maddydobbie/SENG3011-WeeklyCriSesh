from requests.models import Response
import requests
import json

resp = requests.get("http://127.0.0.1:5000/articles", json={'startDate':'2020-03-01T00:00:70', 'endDate':'2021-01-01T00:00:00'})

print(json.dumps(resp.json(), indent=4))