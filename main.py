import openmeteo_requests

import requests_cache
from retry_requests import retry

import weather_codes

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)
url = "https://api.open-meteo.com/v1/forecast"

while True:
    user_input = input("Enter latitude and longitude (for example, '52.52 13.41') "
                       "for get weather info or enter 'quit' to quit from program: ").split(' ')

    try:
        if user_input[0] == 'quit':
            print('Program stopping...')
            exit()

        latitude = float(user_input[0])
        longitude = float(user_input[1])

        if latitude > 90 or latitude < -90:
            print(f"Latitude must be in range of -90 to 90°. Given: {latitude}.")
            continue
        if longitude > 180 or longitude < -180:
            print(f"Longitude must be in range of -180 to 180°. Given: {longitude}.")
            continue
    except ValueError:
        print("Bad format.")
        print('\n')
        continue
    except IndexError:
        print("Bad format.")
        print('\n')
        continue

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "is_day", "weather_code", "cloud_cover", "wind_speed_10m",
                    "wind_direction_10m", "wind_gusts_10m"]
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    current = response.Current()
    current_temperature_2m = round(current.Variables(0).Value(), 2)
    current_relative_humidity_2m = round(current.Variables(1).Value(), 2)
    current_is_day = 'day' if current.Variables(2).Value() else 'night'
    current_weather_code = round(current.Variables(3).Value(), 2)
    current_cloud_cover = round(current.Variables(4).Value(), 2)
    current_wind_speed_10m = round(current.Variables(5).Value(), 2)
    current_wind_direction_10m = round(current.Variables(6).Value(), 2)
    current_wind_gusts_10m = round(current.Variables(7).Value(), 2)

    print('\n')

    print(f"Latitude: {response.Latitude()}°N")
    print(f"Longitude: {response.Longitude()}°E")
    print('\n')

    print(f"Time of day: {current_is_day}")
    print('\n')

    print(f"Temperature: {current_temperature_2m}°C")
    print(f"Humidity: {current_relative_humidity_2m}%")
    print(f"Weather: {weather_codes.WEATHER_CODES[str(int(current_weather_code))][current_is_day]['description']}")
    print('\n')

    print(f"Cloud cover: {current_cloud_cover}%")
    print('\n')

    print(f"Wind speed: {current_wind_speed_10m} km/h")
    print(f"Wind direction: {current_wind_direction_10m}°")
    print(f"Wind gusts: {current_wind_gusts_10m} km/h")

    print('\n')
