from datetime import datetime
from timezonefinder import TimezoneFinder
import pandas as pd
import streamlit as st
import pytz, requests, json, tzlocal

WEATHER_MAP_API_KEY = '7232dcb9557726a814f5309e43503e5b'
WEATHER_MAP_USER = 'asafhenig'
DEFAULT_FILENAME = 'setting.json'


# This function returns timezone string given longitude and latitude values
def get_full_cityname(longitude, latitude):
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lat=latitude, lng=longitude)  # Find the timezone string
    if timezone_str:
        return timezone_str
    else:
        return None


# This function prints local timezone and weather location timezone
def display_date_time(original_city_name, location_timezone=None):
    # Fetch current date and time in user's timezone
    user_timezone = tzlocal.get_localzone()  # Get the local timezone
    user_time = datetime.now(user_timezone)  # Get the current time in the local timezone

    formatted_user_time_str = user_time.strftime("%A, %B %d, %Y, %I:%M %p")
    print(f"Your user's date and time in timezone = {user_timezone} is: {formatted_user_time_str}")

    # Optional: Convert and display the date and time for the specified location
    if location_timezone:
        location_time = user_time.astimezone(pytz.timezone(location_timezone))
        formatted_location_time = location_time.strftime("%A, %B %d, %Y, %I:%M %p")
        print(f"The chosen date and time in the city \'{original_city_name}\': Timezone {location_timezone} is: {formatted_location_time}")


# retrieve the needed weather data from the full weather JSON
# temperature, weather conditions, and humidity.
def focused_weather_string(complete_weather_json, city, unit):
    # print(json.dumps(complete_weather_json, indent=4))
    return f"The weather in \'{city}\' is: Temperature: {complete_weather_json['main']['temp']} ({unit}), Condition: {complete_weather_json['weather'][0]['description']}, Humidity: {complete_weather_json['main']['humidity']}%"


# Function to retrieve the weather in a given location
def return_weather_in_city(cityname, unit='Celsius', print_error=True):
    url = "http://api.openweathermap.org/data/2.5/weather"
    units = 'metric' if (unit == 'Celsius' or unit == 'metric') else 'imperial'
    params = {
        'q': cityname,
        'appid': WEATHER_MAP_API_KEY,
        'units': units
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to retrieve weather date: {response.status_code}" if print_error else None


# Function to set default location and return it for Stretch Goal A
def default_location_setting(filename):
    data = {}
    default_location_exist = False

    while not default_location_exist:

        default_location = input('Please provide a city name to be used as a default location for weather: ')

        #Check if such a City exist by trying to fetch its weather
        #If fetching weather than default_location_exist = True
        if return_weather_in_city(default_location, 'Celsius', False):
            default_location_exist = True
        else:
            print(f'City Name \'{default_location}\' is not recognized. Enter a new city name')
            continue

        # add default location to data dictionary
        data['default location'] = default_location

    # write to json file
    return default_location if write_data_to_json_file(data, filename) else None


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
def weather_location_setting(filename, default_location):
    data = {}
    location_list = []
    location_list_is_empty = True

    #pull out json dictionary
    data = get_dict_from_json_filename(filename)
    if data:
        prompt = f"If you are interested to know the weather in your default city \'{default_location}\',please press Enter.\n\
Alternatively, start a new list of cities you are interested in by writing down their names and press Enter after each one.\n\
Once you are done with the list simply Press Enter: "
        user_input = input(prompt).strip()
        while user_input:
            if not return_weather_in_city(user_input, 'Celsius', False):
                print(f'The city \'{user_input}\' is not known.')
            else:
                location_list_is_empty = False
                location_list.append(user_input)

            user_input = input('Enter another city name or press Enter to end your city list: ').strip()

        if not location_list_is_empty:
            data['cities'] = location_list
            return write_data_to_json_file(data, filename)
        else:
            return False


# Function to set Units for weather
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


# stretch_goal_A main function
def retrieve_data_from_setting_file(filename, city_list):
    data = {}
    cities = []

    #Open setting file and present weather for each city
    data = get_dict_from_json_filename(filename)

    print(f"The configuration json file \'{filename}\' file has this data:\n" + json.dumps(data, indent=4))

    if data:
        if city_list:
            cities = data['cities']
        else:
            cities.append(data['default location'])
        unit = data['unit']
        for city in cities:
            weather_data = return_weather_in_city(city, unit)
            if type(weather_data) == dict:
                weather_str = focused_weather_string(weather_data, city, unit)

                full_cityname = get_full_cityname(weather_data['coord']['lon'], weather_data['coord']['lat'])
                display_date_time(city, full_cityname)
                print(weather_str)
            else:
                print(weather_data)
    else:
        print(f'Cannot get {filename} file')


# stretch_goal_A main function
def main_stretch_goal_a():
    #Default location setting
    if default_location := default_location_setting(DEFAULT_FILENAME):

        # multiple locations setting
        city_list_was_created = weather_location_setting(DEFAULT_FILENAME, default_location)

        # Units setting
        weather_units_setting(DEFAULT_FILENAME)

        # run main_stretch_goal
        retrieve_data_from_setting_file(DEFAULT_FILENAME, city_list_was_created)

    else:
        print('Failed to store default location')


# stretch_goal_Alpha main function
def main_stretch_goal_alpha():
    city_exist = False

    while not city_exist:

        city_name = input('Please provide the name of the city for which you would like to get the weather: ')
        weather_data = return_weather_in_city(city_name)

        if type(weather_data) == dict:
            weather_str = focused_weather_string(weather_data, city_name, 'Celsius')
            full_cityname = get_full_cityname(weather_data['coord']['lon'], weather_data['coord']['lat'])
            #user_timezone = get_local_timezone()
            display_date_time(city_name, full_cityname)
            print(weather_str)
        else:
            print(f'City Name \'{city_name}\' is not recognized. Enter a new name')
            continue
        break


#This function implements the core request of this project
def run_core_function():
    city_exist = False

    while not city_exist:

        city_name = input('Please provide the name of the city for which you would like to get the weather: ')

        weather_data = return_weather_in_city(city_name, 'Celsius', False)
        if weather_data:
            print(
                f"The weather in \'{city_name}\' is: Temperature: {weather_data['main']['temp']} (Celsius), Condition: {weather_data['weather'][0]['description']}, Humidity: {weather_data['main']['humidity']}%")
            city_exist = True
        else:
            print(f'City Name \'{city_name}\' is not recognized. Enter a new name')
            continue


#This function is a simple welcome message and instruction string
def welcome_message_and_instructions():
    print("\n")
    print("Welcome to the Weather Checker Application.")
    print("===========================================")
    print("In this application users fetch the weather conditions of a given city or cities.\n")


def main_menu():
    print('Choose one of the options below:')
    print('1) Core Functionality: Providing weather for a given city')
    print('2) Enhanced functionality A: Adding timezones and time to weather')
    print('3) Enhanced functionality B: Using json files to store configuration')
    print('4) Exit the program\n')
    while True:
        try:
            user_choice = int(input("Enter 1,2,3 or 4: "))
            if user_choice in range(1, 5):
                return user_choice
            else:
                print(f'Your chose \'{user_choice}\' which is neither 1, 2, 3 or 4. Try again')
        except ValueError:
            print('You did not provide a number. Try again')


#WeatherMap Project Main Function (Stretch Goal C)  which implements Stretch Goal A
def main():
    data = {}
    city_list = True

    welcome_message_and_instructions()

    while True:

        project_menu = main_menu()

        #I am using simple if statement as 'match'-'case' was only introduced in python 3.10
        if project_menu == 1:
            run_core_function()
        elif project_menu == 2:
            main_stretch_goal_alpha()
        elif project_menu == 3:
            main_stretch_goal_a()
        elif project_menu == 4:
            print("Thank you for using the program.\nGoodbye")
            exit(0)

        print('\n')

if __name__ == '__main__':
    main()
