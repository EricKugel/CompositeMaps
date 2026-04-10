import requests
import json


response = requests.post(
    "https://overpass-api.de/api/interpreter",
    """
    [bbox:30.618338,-96.323712,30.591028,-96.330826]
    [out:json]
    [timeout:90]
    ;
    way(30.626917110746, -96.348809105664, 30.634468750236, -96.339893442898);
    out geom;
    """
)

# with open("out.json", "w") as file:
#     file.write(json.dumps(response.json()))
data = response.json()
with open("out.json", "w") as file:
    file.write(json.dumps(data))