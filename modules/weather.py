import requests
import json

def get_weather(location):
    print("Weather module loaded.")
    return f"Sunny, 7C, 20% chance of rain in {location}."