from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz, requests, json, tzlocal
import pandas as pd


WEATHER_MAP_API_KEY = '7232dcb9557726a814f5309e43503e5b'
WEATHER_MAP_USER = 'asafhenig'
IPINFO_TOKEN_KEY = 'b37d8bc2d98b9e'

# ========================================== CORE FUNCTION with Stretch Goal Alpha
'''
def get_local_timezone():
    local_timezone = tzlocal.get_localzone()
    return local_timezone

def get_ip_address():
    response = requests.get('https://api.ipify.org?format=json')
    ip_address = response.json()['ip']
    return ip_address

#This function returns the local longitude and latitude of my current location
def get_ip_location():
    my_ip = get_ip_address() 
    print(my_ip)
    response = requests.get(f"https://ipinfo.io/{my_ip}/json?token={IPINFO_TOKEN_KEY}")
    if response.status_code == 200:       
       data = response.json()
       localtimezone = data['timezone']
       print(f"Asaf 1: {localtimezone}")
       location = data['loc'].split(',')
       latitude = location[0]
       longitude = location[1]
       print(f'Asaf2 lon: {longitude} , lat:{latitude}')
       return longitude, latitude
    else:
        return f"Failed to retrieve current location data: {response.status_code}" 
'''


# This function returns timezone string given longitude and latitude values
def get_full_cityname(longitude, latitude):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)  # Find the timezone string
    if timezone_str:
        return timezone_str
    else:
        return None


# This function prints local timezone and weather location timezone
def display_date_time(user_timezone=None, location_timezone=None):
    # Fetch current date and time in user's timezone
    if user_timezone == None:
        local_timezone = tzlocal.get_localzone()  # Get the local timezone
        user_time = datetime.now(local_timezone)  # Get the current time in the local timezone
    else:
        user_time = datetime.now(pytz.timezone(user_timezone))

    formatted_user_time = user_time.strftime("%A, %B %d, %Y, %I:%M %p")
    print(f"Your current date and time in {user_timezone} is: {formatted_user_time}")

    # Optional: Convert and display the date and time for the specified location
    if location_timezone:
        location_time = user_time.astimezone(pytz.timezone(location_timezone))
        formatted_location_time = location_time.strftime("%A, %B %d, %Y, %I:%M %p")
        print(f"Date and time in {location_timezone} is: {formatted_location_time}")


# retrieve the needed weather data from the full weather JSON
# temperature, weather conditions, and humidity.
def focused_weather_string(complete_weather_json, city, unit):
    # print(json.dumps(complete_weather_json, indent=4))
    return f"The weather in {city} is: Temprature: {complete_weather_json['main']['temp']} ({unit}), Condition: {complete_weather_json['weather'][0]['description']}, Humidity: {complete_weather_json['main']['humidity']}"


# Function to retrieve the weather in a given location
def return_weather_in_city(cityname, unit = 'metric'):
    url = "http://api.openweathermap.org/data/2.5/weather"
    units = 'metric' if unit == 'Celsius' else 'imperial'
    params = {
        'q': cityname,
        'appid': WEATHER_MAP_API_KEY,
        'units': unit
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to retrieve weather date: {response.status_code}"

    # =====================================


# ===================================== Stretch Goal A ================


# Function to set default location
def default_location_setting(filename):
    data = {}
    default_location = input('Please provide a default location for weather: ')

    # add default location to data dictionary
    data['default location'] = default_location

    # write to json file
    write_data_to_json_file(data, filename)


# writing data to json file
# input dictionary , json filename
def write_data_to_json_file(data, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"An error occurred while trying to write a json file {filename}: {e}")
        return False
    else:
        print(f"Json file {filename} was stored locally.")
        return True


# return dictionary from json file
def get_dict_from_json_filename(filename):
    data = {}
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"An error occurred while trying to read a json file {filename}: {e}")
        return None


# Function to enable user to add more location and put them in a list
def weather_location_setting(filename):
    data = {}
    location_list = []
    data = get_dict_from_json_filename(filename)
    if data:
        prompt = "Please place a city name you are interested to know its weather. If you do not want to add more cities wrtie \'stop\': "
        while True:
            user_input = input(prompt)
            if user_input != 'stop':
                location_list.append(user_input)
            else:
                data['cities'] = location_list
                return write_data_to_json_file(data, filename)


# Functino to set Units for weather
def weather_units_setting(filename):
    data = {}
    units = ['Celsius', 'Fahrenheit']
    data = get_dict_from_json_filename(filename)

    if data:
        prompt = "Please choose a units to be used for weather:\n1. Celsius\n2. Fahrenheit\nEnter 1 or 2: "
        while True:
            user_input = input(prompt)
            if user_input in ['1', '2']:
                data['unit'] = 'Celsius' if user_input == '1' else 'Fahrenheit'
                return write_data_to_json_file(data, filename)
            else:
                print("Invalid choice, please enter 1 or 2.")

#This functions returns the local timezone as a string
def get_local_timezone():
    # Get the local timezone
    local_tz = tzlocal.get_localzone()

    # Get the current time in the local timezone
    local_time = datetime.now(local_tz)

    # Get the timezone as a string
    timezone_str = local_time.tzname()
    return timezone_str

# stretch_goal_Alpha main function
def main_stretch_goal_Alpha():
    # Ask user for a city name input
    city_name = input('Please provide the name of the city for which you would like to get the weather: ')
    weather_data = return_weather_in_city(city_name)

    if type(weather_data) == dict:
        weather_str = focused_weather_string(weather_data, city_name)

        full_cityname = get_full_cityname(weather_data['coord']['lon'], weather_data['coord']['lat'])
        user_timezone = get_local_timezone()
        display_date_time(user_timezone, full_cityname)
        print(weather_str)

    else:
        print(weather_data)

 # stretch_goal_A main function
def main_stretch_goal_A(filename):
    data = {}
    cities = []


    #Open setting file and present weather for each city
    data = get_dict_from_json_filename(filename)
    if data:
        cities = data['cities']
        unit = data['unit']
        for city in cities:
            weather_data = return_weather_in_city(city, unit)
            if type(weather_data) == dict:
                weather_str = focused_weather_string(weather_data, city, unit)

                full_cityname = get_full_cityname(weather_data['coord']['lon'], weather_data['coord']['lat'])
                display_date_time('Asia/Jerusalem', full_cityname)
                print(weather_str)
            else:
                print(weather_data)
    else:
        print(f'Cannot get {filename} file')

def main():
    data = {}
    filename = 'setting.json'

    # Default location setting
    default_location_setting(filename)

    # multiple locations setting
    weather_location_setting(filename)

    # Units setting
    weather_units_setting(filename)

    data = get_dict_from_json_filename(filename)
    print(f"The local {filename} file has this data:\n" + json.dumps(data, indent=4))

    # run main_stretch_goal
    main_stretch_goal_A(filename)


if __name__ == '__main__':
    main()