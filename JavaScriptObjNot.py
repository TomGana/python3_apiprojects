#working with json files:
#creating object data
import json

data = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}
#write to json file:
with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)
#writing to python native script
json_string = json.dumps(data)
