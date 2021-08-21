import json
import requests

http = requests.get("https://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=a1311b63a19a3dd611a43a3dbec666b5&type=json")
var = http.json()["weather"][0]["description"]
print("The weather is", var)