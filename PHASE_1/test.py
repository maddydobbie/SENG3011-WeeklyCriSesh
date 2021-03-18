from requests.models import Response
import requests

# resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'location':'', 'keywords':'covid'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'location':'Sydney', 'keywords':'covid'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'maddy':'2020-03-01T00:00:00'})

# resp = requests.post("http://127.0.0.1:5000/some", json={'maddy':'2020-03-01T00:00:00'})

# resp = requests.delete("http://127.0.0.1:5000/some", json={'maddy':'2020-03-01T00:00:00'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2020-03-01T00:00:00'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'endDate':'2020-03-01T00:00:00'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2020-03-01T00:00:70', 'endDate':'2021-01-01T00:00:00'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2020-03-01T00:00:00', 'endDate':'2021-01-01T00:00:70'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2020-03-01T00:00:70', 'endDate':'2021-01-01T00:00:70'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2020-03-01T00:00jhjhhjjh:70', 'endDate':'2021-01-01T00:00:00'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2020-03-01T00:00:00', 'endDate':'2021-01-01T00hhujh:00:70'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2020-03-01Tgh00:00:70', 'endDate':'2021-01-01T00:00ggg:70'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2021-03-01T00:00:00', 'endDate':'2020-01-01T00:00:00'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2022-03-01T00:00:00', 'endDate':'2020-01-01T00:00:00'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2021-03-01T00:00:00', 'endDate':'2022-01-01T00:00:00'})

# resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2022-03-01T00:00:00', 'endDate':'2023-01-01T00:00:00'})

# works
resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2020-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'location':'Ethiopia', 'keywords':'fever'})

#  empty - 400
resp = requests.get("http://127.0.0.1:5000/some", json={})

# no start date - 400
resp = requests.get("http://127.0.0.1:5000/some", json={'endDate':'2023-01-01T00:00:00', 'location':'Ethiopia', 'keywords':'fever'})

# no end date
resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2021-01-01T00:00:00', 'location':'Ethiopia', 'keywords':'fever'})

# check start date in correct format
resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2021-01-1', 'endDate':'2023-01-01T00:00:00', 'location':'Ethiopia', 'keywords':'fever'})

# check end date in correct format
resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2020-01-01T00:00:00', 'endDate':'2021-03-1', 'location':'Ethiopia', 'keywords':'fever'})

# check correct order
resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2021-01-03T00:00:00', 'endDate':'2021-01-01T00:00:00', 'location':'Ethiopia', 'keywords':'fever'})

# check start date isnt in the future
resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2022-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'location':'Ethiopia', 'keywords':'fever'})

# check start date isnt in the future
resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2022-03-01T00:00:00', 'location':'Ethiopia', 'keywords':'fever'})

# no keywords (should work)
resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2020-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'location':'Ethiopia', 'keywords':''})

# no location (should work)
resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'location':'', 'keywords':'fever'})

# no location no keywords (should work)
resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'location':'', 'keywords':''})


# gibberish in location
resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2020-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'location':'asdnadnafn', 'keywords':'fever'})


# gibberish in disease
resp = requests.get("http://127.0.0.1:5000/some", json={'startDate':'2020-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'location':'Ethiopia', 'keywords':'dsfsfs'})