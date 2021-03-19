from requests.models import Response
import requests
import json

resp = requests.get("http://127.0.0.1:5000/articles", json={'maddy':'2020-03-01T00:00:00'})

resp = requests.post("http://127.0.0.1:5000/articles", json={'maddy':'2020-03-01T00:00:00'})

resp = requests.delete("http://127.0.0.1:5000/articles", json={'maddy':'2020-03-01T00:00:00'})

resp = requests.get("http://127.0.0.1:5000/articles", json={'startDate':'2020-03-01T00:00:00'})

resp = requests.get("http://127.0.0.1:5000/articles", json={'endDate':'2020-03-01T00:00:00'})

resp = requests.get("http://127.0.0.1:5000/articles", json={'startDate':'2020-03-01T00:00:70', 'endDate':'2021-01-01T00:00:00'})

resp = requests.get("http://127.0.0.1:5000/articles", json={'startDate':'2020-03-01T00:00:00', 'endDate':'2021-01-01T00:00:70'})

resp = requests.get("http://127.0.0.1:5000/articles", json={'startDate':'2020-03-01T00:00:70', 'endDate':'2021-01-01T00:00:70'})

resp = requests.get("http://127.0.0.1:5000/articles", json={'startDate':'2020-03-01T00:00jhjhhjjh:70', 'endDate':'2021-01-01T00:00:00'})

resp = requests.get("http://127.0.0.1:5000/articles", json={'startDate':'2020-03-01T00:00:00', 'endDate':'2021-01-01T00hhujh:00:70'})

resp = requests.get("http://127.0.0.1:5000/articles", json={'startDate':'2020-03-01Tgh00:00:70', 'endDate':'2021-01-01T00:00ggg:70'})

resp = requests.get("http://127.0.0.1:5000/articles", json={'startDate':'2021-03-01T00:00:00', 'endDate':'2020-01-01T00:00:00'})

resp = requests.get("http://127.0.0.1:5000/articles", json={'startDate':'2022-03-01T00:00:00', 'endDate':'2020-01-01T00:00:00'})

resp = requests.get("http://127.0.0.1:5000/articles", json={'startDate':'2021-03-01T00:00:00', 'endDate':'2022-01-01T00:00:00'})

resp = requests.get("http://127.0.0.1:5000/articles", json={'startDate':'2022-03-01T00:00:00', 'endDate':'2023-01-01T00:00:00'})

resp = requests.get("http://127.0.0.1:5000/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00'})
print(json.dumps(resp.json(), indent=4))
