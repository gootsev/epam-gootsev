from flask import Flask
import requests, json, os

app = Flask(__name__)

@app.route('/')
def main_app():

	if os.environ['NAME'] == "none":
		name = "Max Payne"
	else:
		name = os.environ['NAME']

	if os.environ['CITY'] == "none":
		city = "Moscow"
	else:
		city = os.environ['CITY']

	if os.environ['API_KEY'] == "none":
		api = "a1311b63a19a3dd611a43a3dbec666b5"
	else:
		api = os.environ['API_KEY']
	

	params = {'q': {city}, 'appid': {api}}
	request = requests.get("https://api.openweathermap.org/data/2.5/weather?units=metric", params=params)
	description = request.json()["weather"][0]["description"]
	temp = request.json()['main']['temp']

	return f"Hi {name}! Now in {city} {temp} C, {description}."

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)