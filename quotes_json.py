import requests
from bs4 import BeautifulSoup
import json
import re

# Define the initial url
url = "https://quotes.toscrape.com"

# Create an empty dictionary to add parsed data 
parsed_dict = {}

# Start a loop that represents a parsed_page being added to the parsed_dict
page_count = 1
while url:
    # Use requests to get the webpage
    response = requests.get(url)
    
    # Initialize BeautifulSoup and the html.parser
    soup = BeautifulSoup(response.content, 'html.parser')
    # Parse the web page for all elements that are a division with the class "quote"
    quotes_class = soup.find_all('div', class_='quote')
    
    parsed_page = {}
    # Parse through each element found and extract the quote, author, and tags
    quote_count = 1
    for quote_class in quotes_class:
        # Extract quotes, authors, and tags from quote_class
        quote = quote_class.find('span', class_='text').text.strip()
        author = quote_class.find('small', class_='author').text.strip()
        tags = quote_class.find('div', class_='tags').text.strip()
        # Clean tags data
        tags = quote_class.find('div', class_='tags').text.lstrip().replace('Tags:', '').replace('\n', ',').rstrip(',')
        tags = re.sub(r'^,\s*,', '', tags) 


        # Split each tag into a separate object 
        tag_list = []
        for tag in tags.split('\n'):
            words = tag.split(',')
            tag_list.extend(words)
                
        # Send the extracted data to parsed_page dict
        parsed_page.update({'Quote' + str(quote_count):{'quote': quote, 'author': author, 'tags': tag_list}})
        quote_count += 1
    
    # Send the parsed_page to the parsed_dict
    parsed_dict.update({'Page' + str(page_count): parsed_page})
    print(f'page {page_count} is complete!')
    page_count +=1
    # Check to see if there is a next page; if there isn't, then stop the while loop
    try:
        next_link = soup.find('li', class_='next').find('a')
        url = "https://quotes.toscrape.com" + next_link['href'] 
    except AttributeError:
        print("No more pages to parse")
        url = None
        break
       
# Dump all extracted data into a json file 
with open('quotes.json', 'w') as outfile:
    json.dump(parsed_dict, outfile)
