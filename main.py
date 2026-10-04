import requests
import json
import os
from distance_cal import distance_calculation_haversine

# 1. Get data
if os.path.exists("data/osm_data.json"):
    with open("data/osm_data.json", "r") as file:
        opass_data = json.load(file)
else:
    
    headers = {
        "User-Agent": "CityDigitalTwin/0.1"
    }

    opass_url = "https://overpass-api.de/api/interpreter"
    opass_query = """
    [out:json];

    (
    way["name"="Janpath"](28.61,77.20,28.64,77.23);
    way["name"="Outer Circle"](28.61,77.20,28.64,77.23);
    );

    out body;
    >;
    out skel qt; 
    """
    response = requests.get(
        opass_url, 
        params={"data":opass_query}, 
        headers=headers
        )

    print(response.status_code)
    opass_data = response.json()

    with open("data/osm_data.json", "w") as file:
        json.dump(opass_data, file, indent=4)

# 2. Process data
# Find nodes belonging to each road
janpath_nodes = set()
outer_circle_nodes = set()

for element in opass_data["elements"]:
    if element["type"] == "way":
        if element["tags"]["name"] == "Janpath":
            janpath_nodes.update(element["nodes"])

        if element["tags"]["name"] == "Outer Circle":
            outer_circle_nodes.update(element["nodes"])

# Find nodes shared by both roads
shared_nodes = janpath_nodes & outer_circle_nodes

# Store coordinates of the shared nodes
node_coordinates = {}

for element in opass_data["elements"]:
        if element["type"] == "node":
            node_coordinates[element['id']] = (
                 element['lat'], 
                 element['lon']
                 )

# Find the way containing both shared nodes
for element in opass_data["elements"]:
     if element["type"] == "way":
        found_all = True
        for node in shared_nodes:
            if node not in element["nodes"]:
                found_all = False 

        if found_all:
            nodes = element["nodes"]

            segments = []

            for start_node, end_node in zip(nodes, nodes[1:]):
                start_coordinates = node_coordinates[start_node]
                end_coordinates = node_coordinates[end_node]

                start_lat, start_lon = start_coordinates
                end_lat, end_lon = end_coordinates

                distance = distance_calculation_haversine(
                    start_lat,
                    start_lon,
                    end_lat,
                    end_lon
                )

                segment = {
                    "start_node": start_node,
                    "end_node": end_node,
                    "length": distance,
                    "road_name": element["tags"]["name"],
                    "lanes": element["tags"]["lanes"],
                    "oneway": element["tags"]["oneway"]
                            }
                segments.append(segment)

            for segment in segments:
                print(json.dumps(segment, indent=4))
            print(len(segments))

     
