from modules.weather_data import get_latest_weather_inputs

# Shivamogga coordinates
latitude = 13.9299
longitude = 75.5681

try:
    weather = get_latest_weather_inputs(latitude, longitude)

    print("\nKRISHIMITRA AI - WEATHER INPUTS")
    print("--------------------------------")

    for key, value in weather.items():
        print(f"{key}: {value}")

except Exception as error:
    print("Weather data error:", error)