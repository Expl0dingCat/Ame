import requests
import json
 
# Enter openweathermap API key here (get it at https://openweathermap.org/api)
api_key = None

def get_weather(city):
    if api_key:
        url = f"http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}&units=metric"
        response = requests.get(url)
        response = json.loads(response.text)
        if response["cod"] != "404":
            temperature = response["main"]["temp"]
            pressure = response["main"]["pressure"]
            humidity = response["main"]["humidity"]
            feels_like = response["main"]["feels_like"]
            wind = response["wind"]["speed"]
            description = response["weather"][0]["description"]
        
            return {"city": city, "temperature": temperature, "pressure": pressure, "humidity": humidity, "description": description, "feels_like": feels_like, "wind": wind, "units": "metric"}
        else:
            return "Invalid city."
    else:
        return "No API key provided. Unable to fetch weather, add API key in weather.py."