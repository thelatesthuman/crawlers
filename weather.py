import requests
import sys
from bs4 import BeautifulSoup

try:
    # Send an HTTP request to weather.com url
    url = str(sys.argv[1])
    response = requests.get(url)

    # Parse file and extract the temp, weather, and day/night temps
    soup = BeautifulSoup(response.content, 'html.parser')
    current_temp = soup.find('span', class_='CurrentConditions--tempValue--MHmYY').text.strip()
    current_weather = soup.find('div', class_='CurrentConditions--phraseValue--mZC_p').text.strip()
    daynight = soup.find('div', class_='CurrentConditions--tempHiLoValue--3T1DG').text.strip() 
    
    # print parsed data to terminal
    print(current_temp)
    print(current_weather)
    print(daynight)
except Exception as e:
    print("An error has occured", e)
