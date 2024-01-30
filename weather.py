from configparser import ConfigParser
import argparse
import json
import sys
from urllib import parse, request, error
import style

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# weather conditions codes
THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)

def _get_API_key():
    config = ConfigParser()
    config.read("secrets.ini")
    return config["openweather"]["API_KEY"]

def command_line_args():
    parser = argparse.ArgumentParser(description="Acquires Weather and Temperature for a City")
    parser.add_argument("city", nargs="+", type=str, help="Enter the City Name")
    parser.add_argument("-i", "--imperial", action="store_true", help="Display the Temperature in Imperial Units",)
    return parser.parse_args()

def weather_query(city_name_input, imperial=False):
    api_key = _get_API_key()
    city_name = " ".join(city_name_input)
    encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (f"{WEATHER_URL}?q={encoded_city_name}&units={units}&appid={api_key}")
    return url

def get_weather_data(query_url):
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401:
            sys.exit("Access Denied. Check your API Key!")
        elif http_error.code == 404:
            sys.exit("Unable to find Weather Data for this City!")
        else:
            sys.exit(f"Something went wrong... ({http_error.code})")
    data = response.read()
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Could not read the Server response!")

def weather_data_display(weather_data, imperial=False):
    city = weather_data['name']
    weather_code = weather_data['weather'][0]['id']
    description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    
    style.change_color(style.REVERSE)
    print(f"{city:^{style.PADDING}}", end="")
    
    style.change_color(style.RESET)
    weather_icon, color = _select_display_parameters(weather_code)
    
    style.change_color(color)
    print(f"\t{weather_icon}", end=" ")
    print(f"{description.capitalize():^{style.PADDING}}", end= " ",)
    style.change_color(style.RESET)
    
    print(f"({temperature}°{'F' if imperial else 'C'})")

def _select_display_parameters(weather_code):
    # match/case statement to be included in update
    if weather_code in THUNDERSTORM:
        display_parameters = ("⚡", style.RED)
    elif weather_code in DRIZZLE:
        display_parameters = ("🌧️", style.CYAN)
    elif weather_code in RAIN:
       display_parameters = ("💧", style.BLUE)
    elif weather_code in SNOW:
        display_parameters = ("❄️", style.WHITE)
    elif weather_code in ATMOSPHERE:
        display_parameters = ("🌀", style.BLUE)
    elif weather_code in CLEAR:
        display_parameters = ("☀️", style.YELLOW)
    elif weather_code in CLOUDY:
        display_parameters = ("☁️", style.WHITE)
    else:
        display_parameters = ("🌎", style.RESET)
    return display_parameters

if __name__ == "__main__":
    user_args = command_line_args()
    query_url = weather_query(user_args.city, user_args.imperial)
    weather_data = get_weather_data(query_url)
    weather_data_display(weather_data, user_args.imperial)