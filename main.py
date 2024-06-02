from datetime import datetime
from timezonefinder import TimezoneFinder
import pandas as pd
import streamlit as st
import pytz, requests, json, tzlocal


WEATHER_MAP_API_KEY = '7232dcb9557726a814f5309e43503e5b'
WEATHER_MAP_USER = 'asafhenig'

# ========================================== CORE FUNCTION with Stretch Goal Alpha

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



# ===================================== Stretch Goal A ================


# Function to set default location and return it for Stretch Goal A
def default_location_setting(filename):
    data = {}
    default_location = input('Please provide a default location for weather: ')

    # add default location to data dictionary
    data['default location'] = default_location

    # write to json file
    return default_location if write_data_to_json_file(data, filename) else None

# Function to set default location and return it for Stretch Goal C
def default_location_setting_web(filename):
    data = {}

    default_location = st.text_input('Please provide a default location for yor Weather Application','')

    if default_location:
       st.write(f'You have set the beautify city of \'{default_location}\', as the default location for this Weather App!')

    #add default location to data dictionary
    data['default location'] = default_location

    #write to json file
    return default_location if write_data_to_json_file_web(data, filename) else None




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

# writing data to json file
# input dictionary , json filename
def write_data_to_json_file_web(data, filename):
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        st.write(f"An error occurred while trying to write a json file {filename}: {e}")
        return False
    else:
        st.write(f"Json file {filename} was stored locally.")
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
    data = get_dict_from_json_filename(filename)
    if data:
        prompt = f"If you are interested to know the weather in \'{default_location}\',pease press Enter.\n\
Alternatively, write down a list of other cities separated by commas (\',\'): "
        user_input = input(prompt)
        if user_input != '':
            location_list = user_input.split(',')
            data['cities'] = location_list
            return write_data_to_json_file(data, filename)
        else:
            return False
    else:
        return False



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
def retrieve_data_from_setting_file(filename, city_list):
    data = {}
    cities = []


    #Open setting file and present weather for each city
    data = get_dict_from_json_filename(filename)

    print(f"The local {filename} file has this data:\n" + json.dumps(data, indent=4))

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
                display_date_time('Asia/Jerusalem', full_cityname)
                print(weather_str)
            else:
                print(weather_data)
    else:
        print(f'Cannot get {filename} file')

#WeatherMap Project Main Function which implements Stretch Goal A
def main_stretch_goal_A():
    data = {}
    city_list = True
    filename = 'setting.json'

    # Default location setting
    default_location = default_location_setting(filename)

    if default_location:

        # multiple locations setting
        city_list = weather_location_setting(filename, default_location)

        # Units setting
        weather_units_setting(filename)

        # run main_stretch_goal
        retrieve_data_from_setting_file(filename, city_list)

    else:
        print('Failed to store default location')

def set_streamlit_markdown():
    # Custom CSS to increase the font size
    css = """
    <style>
    /* Increase the font size for the label of the input field */
    /* Targeting the label of the text input */
    div.stTextInput > label {
        font-size: 18px !important;
    }
    label {
        font-size: 25px !important;
    }
    /* Increase the font size for the input field */
    input {
        font-size: 25px !important;
        height: auto;  /* Adjust height to fit larger text if necessary */
    }
    
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

#Main for Stretch Goal C (Use of streamlit)
def main_goal_stretch_goal_c():
    data = {}
    city_list = True
    filename = 'setting.json'

    set_streamlit_markdown()

    # Default location setting
    default_location = default_location_setting_web(filename)

#main
def main():

    st.title('WeatherMap App')

    main_goal_stretch_goal_c()


if __name__ == '__main__':
    main()