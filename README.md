# OpenWeatherMap - Weather API

## Description

**Project Name**:      Weather Checker Application - OpenWeatherMap

**Owner**:             Asaf Henig (asafhenig1@gmail.com)

**Github repository**: https://github.com/Asafhenig1/OpenWeatherMap

**Overview**: Weather Checker Application - This OpenWeatherMap project focuses on the ability to provide users 
with weather information and exact hour for a provided one or more city names.


The project provides users with a menu that enables them to choose and run any of these options: 
1) **Core Functionality: Providing weather for a given city**
   Program is requesting user to enter a city name for which it will provide the weather (temperature is provided in Celsius)
2) **Enhanced Functionality A: Adding timezone and time to  the weather**
   Program is requesting user to enter a city name and will provide:
   A) User's location (server location) timezone and time
   B) City location timezone and time
   C) City weather (provided in Celsius)
3) **Enhanced functionality B: Using json files to store configuration**
   Program is requesting customer to provide the below list of details, all details are stored in setting.json file.
   A) 'default cityname' for which the program could provide timezone, time and weather in case no other city is chosen by the user.
   B) (Optional) List of cities for which the program could provide timezone, time and weather. 
   C) Temperature units: to be chosen from two alternatives: Celsius or Fahrenheit
4) **Exit the program**
   The program will gracefully exit

## usage
The program can run from shell or from your python editor environment.
Hereunder instructions how to run it from shell

1) Download all files form the github repository (see above) to a known location in your computer
2) Open shell and get to the folder to which you've downloaded the files
3) Run 'poetry install' and 'poetry build'
4) Run 'pyhon main.py'
5) Follow the program instruction on screen 

## Dependencies
Customer should make sure he has a python supporting environment.
