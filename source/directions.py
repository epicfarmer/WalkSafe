import requests
import pprint


def api_key():
    with open("/Users/Kathryn/Desktop/GoogleMapKey", 'r') as fh:
        return fh.read().strip()

API_KEY = api_key()

base_url = 'https://maps.googleapis.com/maps/api/directions/json'
params = {"origin": "11 Yogurt Lane, Baltimore, MD",
          "destination": "615 N Wolfe Street, Baltimore, MD",
          "mode": "walking",
          "key": API_KEY}

r = requests.get(base_url, params=params)
print r.url

pprint.pprint(r.json())