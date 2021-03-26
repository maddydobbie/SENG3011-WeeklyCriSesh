from requests.models import Response
import requests
import json
import pytest

# testing API error responses
# endpoint at: http://seng3011.pythonanywhere.com/articles

# invalid dates: no dates
def test_no_parameters():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={})
    assert (r.json()["reason"]) == "No start date."

# invald dates: no endDate
def test_no_end_date():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2020-03-01T00:00:00'})
    assert (r.json()["reason"]) == "No end date."

# invald dates: no startDate
def test_no_start_date():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'endDate':'2020-03-01T00:00:00'})
    assert (r.json()["reason"]) == "No start date."

# invalid time in startDate, valid endDate
def test_invalid_start_date_time():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2020-03-01T00:00:70', 'endDate':'2020-01-01T00:00:00'})
    assert (r.json()["reason"]) == "Start date in incorrect format."

# invalid day in startDate, valid endDate
def test_invalid_start_date_day():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2020-03-40T00:00:00', 'endDate':'2020-01-01T00:00:00'})
    assert (r.json()["reason"]) == "Start date in incorrect format."

# invalid month in startDate, valid endDate
#def test_invalid_start_date_month():
 #   r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2020-13-01T00:00:00', 'endDate':'2020-01-01T00:00:00'})
 #   assert (r.json()["reason"]) == "Start date in incorrect format."

# invalid year in startDate, valid endDate
def test_invalid_start_date_year():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'0001-13-01T00:00:00', 'endDate':'2020-01-01T00:00:00'})
    assert (r.json()["reason"]) == "Start date in incorrect format."

# invalid dates: startDate before endDate
def test_start_after_end():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-03-01T00:00:00', 'endDate':'2020-01-01T00:00:00'})
    assert (r.json()["reason"]) == "End date before start date."

# invalid dates: both dates in the future
def test_dates_in_future():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2022-03-01T00:00:00', 'endDate':'2023-01-01T00:00:00'})
    assert (r.json()["reason"]) == "Dates are in the future."

# invalid startDate - not a date
def test_date_not_date():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'this is a string', 'endDate':'2021-01-01T00:00:00'})
    assert (r.json()["reason"]) == "Start date in incorrect format."

# invalid startDate - doesn't have a time
def test_date_no_time():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2020-03-01', 'endDate':'2021-01-01T00:00:00'})
    assert (r.json()["reason"]) == "Start date in incorrect format."

# valid dates - successful API call
def test_good_dates():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00'})
    assert(r.status_code == 200)

# valid dates, empty keywords - successful API call
def test_good_dates_empty_keywords():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'keywords':''})
    assert(r.status_code == 200)

# valid dates, empty location - successful API call
def test_good_dates_empty_location():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'location':''})
    assert(r.status_code == 200)

# valid dates, empty location and keywords - successful API call
def test_good_dates_empty_location_and_keywords():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'keywords':'', 'location':''})
    assert(r.status_code == 200)

# valid dates, and location, empty keywords - successful API call
def test_good_dates_empty_location_with_keywords():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'keywords':'flu', 'location':''})
    assert(r.status_code == 200)

# valid dates, and keywords, empty location - successful API call
def test_good_dates_empty_keywords_with_location():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'keywords':'', 'location':'Congo'})
    assert(r.status_code == 200)

# valid dates, and keywords, and location - successful API call
#def test_good_dates_empty_keywords_with_location():
#    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2020-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'keywords':'covid', 'location':'China'})
#    assert(r.status_code == 200)

# valid dates, another input which is invalid is ignored - successful API call
def test_good_dates_invalid_input():
    r = requests.get("http://seng3011.pythonanywhere.com/articles", json={'startDate':'2021-01-01T00:00:00', 'endDate':'2021-03-01T00:00:00', 'invalid':''})
    assert(r.status_code == 200)