	# Make a get request to get the latest position of the international space station from the opennotify api.
from pip._vendor import requests
import os
import json
#response = requests.get("http://api.open-notify.org/iss-now.json")
# Print the status code of the response.
#print(response.status_code)
# Set up the parameters we want to pass to the API.
# This is the latitude and longitude of New York City.
#parameters = {"lat": 40.71, "lon": -74}
# Make a get request with the parameters.
#response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
# Print the content of the response (the data the server returned)
#iss = response.content.decode('utf-8')
#with open("data_file.json", 'w') as file:
    #file.write(iss)
# This gets the same data as the command aboveresponse = requests.get("http://api.open-notify.org/iss-pass.json?lat=40.71&lon=-74")
#print(iss)
#response = requests.get("api.openweathermap.org/data/2.5/forecast?zip=07722,us")
#print(response.content.decode('utf-8'))
api_key = os.environ.get("weather_key")

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Give city name
city_name = input("Enter city name : ")

# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

# get method of requests module
# return response object
response = requests.get(complete_url)

# json method of response object
# convert json format data into
# python format data



x = response.json()
y = x["main"]
temp = y["temp"]
temp = temp - 273
temp = (temp*(9/5)) + 32
print(temp)
temperature= "Location: " + city_name + " Temperature in Farenheit" + temp
with open("weather.txt", 'w') as file:
    file.write(temperature)
