from flask import Flask
import requests, json, os, psycopg2

app = Flask(__name__)

name = os.environ['NAME']
city = os.environ['CITY']
api = os.environ['API_KEY']



@app.route('/')
def main_app():
	params = {'q': {city}, 'appid': {api}}
	request = requests.get("https://api.openweathermap.org/data/2.5/weather?units=metric", params=params)
	description = request.json()["weather"][0]["description"]
	temp = request.json()['main']['temp']
	db_connect(temp)
	return f"Hi {name}! It's {temp} degrees in {city} now, {description}."

def db_connect(temp):
	connection = psycopg2.connect(user='postgres', password='postgres', database='postgres', host="db")
	try:
		cursor = connection.cursor()
		cursor.execute('CREATE TABLE IF NOT EXISTS weather (id SERIAL PRIMARY KEY, VALUE VARCHAR(255) NOT NULL)')
		sql = f"INSERT INTO weather (value) VALUES ( {temp} )"
		cursor.execute(sql)
		connection.commit()
	except (Exception, psycopg2.DatabaseError) as error:
		print("Error while connecting to PostgreSQL", error)
	finally:
		if(connection):
			cursor.close()
			connection.close()
        

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)