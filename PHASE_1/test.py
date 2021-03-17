from requests.models import Response
import requests

resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'location':'', 'keywords':'variant'})
print(resp.json())