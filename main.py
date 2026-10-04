import requests
from distance_cal import distance_calculation_haversine

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
        if element["type"] == "node" and element["id"] in shared_nodes:
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

            # Find positions of the shared nodes
            positions = []
            for node in shared_nodes:
                positions.append(nodes.index(node))
            positions.sort()

            # Get the positions
            start_position = positions[0]
            end_position = positions[1]

            # Get the actual node IDs
            start_node = nodes[start_position]
            end_node = nodes[end_position]

            # Get their coordinates
            start_coordinates = node_coordinates[start_node]
            end_coordinates = node_coordinates[end_node]

            start_lat, start_lon = start_coordinates
            end_lat, end_lon = end_coordinates

            distance = distance_calculation_haversine(start_lat, start_lon, end_lat, end_lon)
            print(f"{distance:.2f} meters")
     
