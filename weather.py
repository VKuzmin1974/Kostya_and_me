import requests

URL = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"


def get_weather():
    response = requests.get(URL).json()
    # print(response)
    return {
        "temperature": response["current"]["temperature_2m"],
        "wind": response["current"]["wind_speed_10m"],
    }


# print(get_weather())


def get_weather_info():
    response = requests.get(URL).json()

    return {
        "temperature": (str(response["current"]["temperature_2m"])
                        + response["current_units"]["temperature_2m"]),
        "wind": (str(response["current"]["wind_speed_10m"])
                 + response["current_units"]["wind_speed_10m"]),
    }


