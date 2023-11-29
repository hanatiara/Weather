from pyswip import Prolog
from pprint import pprint #debug only
import requests
from flask import Flask, jsonify
from datetime import datetime
from flask import request
from swiplserver import PrologMQI, PrologThread, create_posix_path



def ambil_data_cuaca_openweathermap(city, month):
    api_key = "7ed58f30b93ef05ed426b86b7212369a"
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    url_frontend = "http://localhost:8000"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    response = requests.get(base_url, params=params)
    data_cuaca = response.json()

    if "weather" in data_cuaca and "main" in data_cuaca:
        return {
            "city": city,
            "month": month,
            "weather": data_cuaca["weather"][0]["main"],
            "temperature": data_cuaca["main"]["temp"],
            "humidity": data_cuaca["main"]["humidity"],
            "wind_speed": data_cuaca["wind"]["speed"],
        }
    else:
        return None
    

def prediksi_cuaca(city, month,weather,temperature,humidity,speed):
    prolog = Prolog()
    prolog.consult("prediksi_cuaca.pl")

    query = f"weather_prediction({city}, {month}, {weather},{temperature},{humidity},{speed})."
    hasil_query = list(prolog.query(query))

    if hasil_query:
        return hasil_query
    else:
        return "Tidak ada prediksi."

def main():
    # pprint(prediksi_cuaca("malang", "oktober",ambil_data_cuaca_openweathermap("malang", "oktober")['weather']))
    city = "malang"
    month = "oktober"

    data_cuaca_api = ambil_data_cuaca_openweathermap(city, month)
    if data_cuaca_api:
        print("Data Cuaca dari OpenWeatherMap API:", data_cuaca_api)

        prolog_result = prediksi_cuaca(city, month,data_cuaca_api['weather'],data_cuaca_api['temperature'],data_cuaca_api['humidity'],data_cuaca_api['wind_speed'])
        print(f"Prediksi Cuaca dari Prolog: {prolog_result}")
    else:
        print("Gagal mendapatkan data cuaca dari OpenWeatherMap API.")


def predictWeather(city, month,weather,temperature,humidity,speed):
    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog_thread:
            path = create_posix_path("C:\\Users\\Hana\\OneDrive\\Documents\\Kulyah Part 2\\Prolog\\Weather\\prediksi_cuaca.pl")
            result = prolog_thread.query(f'consult("{path}").')
            # result = prolog_thread.query("consult(\"/prediksi-cuaca.pl\").")
            result = prolog_thread.query(f"weather_prediction({city}, {month}, {weather},{temperature},{humidity},{speed}).")
            hasil_query = list(result)
            return hasil_query


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello"

# send REST API to Frontend 
# ToDo: get API from frontend and calculate weather here, add http response

@app.route('/calculate', methods=['GET'])
def handle_post():
    city = request.args.get("city")
    month = request.args.get("month")
    data_cuaca_api = ambil_data_cuaca_openweathermap(city="malang", month="juni")
    if data_cuaca_api:
        message = predictWeather(city, month,data_cuaca_api['weather'],data_cuaca_api['temperature'],data_cuaca_api['humidity'],data_cuaca_api['wind_speed'])
        response = ""
        # print(f"Prediksi Cuaca dari Prolog: {prolog_result}")
    else:
        message = "Gagal mendapatkan data cuaca dari OpenWeatherMap API."
        
    data = {
         "city" : request.args.get("city"),
         "month" : request.args.get("month"),
         "message" : message
    }

    if (data): return jsonify(data)

    return data

if __name__ == "__main__":
    # with app.app_context():
    #     send_request("wwww")
    app.run()

# if __name__ == "__main__":
#     main()
