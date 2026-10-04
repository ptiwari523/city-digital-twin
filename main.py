import requests
import json

url = f'https://nominatim.openstreetmap.org/search'
param = {
    "q": "Indira Chowk, Connaught Place, New Delhi",
    "format":"json",
}
headers = {
    "User-Agent": "CityDigitalTwin/0.1"
}

response = requests.get(url, params=param, headers=headers)
data = response.json()
for item in data:
    if item["osm_type"] == "way":
        print(json.dumps(item, indent=4))

opass_url = "https://overpass-api.de/api/interpreter"
opass_query = """
[out:json];
way(around:100,28.6233692,77.2190542)[highway];
out geom; 
"""
# response = requests.get(opass_url, params={"data":opass_query}, headers=headers)
# opass_data = response.json()

# for element in opass_data["elements"]:
#     print(json.dumps(element, indent=4))

# print(response.status_code)
# print(response.headers.get("Content-Type"))
# print(response.text[:1000])