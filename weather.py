import requests
from bs4 import BeautifulSoup

try:
    # Send an HTTP request to weather.com url
    url = 'your weather.com url here'
    response = requests.get(url)

    # Parse file and extract the temp, weather, and day/night temps
    soup = BeautifulSoup(response.content, 'html.parser')
    location = soup.find('h1', class_='CurrentConditions--location--1YWj_').text.strip()
    current_temp = soup.find('span', class_='CurrentConditions--tempValue--MHmYY').text.strip()
    current_weather = soup.find('div', class_='CurrentConditions--phraseValue--mZC_p').text.strip()
    daynight = soup.find('div', class_='CurrentConditions--tempHiLoValue--3T1DG').text.strip() 
    
    # print parsed data to terminal
    print('\nWeather in {}\n------------------------'.format(location))
    print('Current Temp: {}'.format(current_temp))
    print('Current Weather: {}'.format(current_weather))
    print(daynight)
except Exception as e:
    print("An error has occured", e)
