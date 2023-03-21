import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re

# Define the initial url
url = "https://quotes.toscrape.com"

# Initialize ElementTree by creating a root object
root = ET.Element("Quotes")

# Start a loop that parses the data page by page
page_count = 1
while url:
    # Use requests to get the webpage
    response = requests.get(url)
    
    # Initialize BeautifulSoup by creating a soup object
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Parse the web page for all elements that are a division with the class "quote"
    quotes_class = soup.find_all('div', class_='quote')

    # Initialize page object as SubElement of root
    page = ET.SubElement(root, "Page", number=str(page_count))

    # Parse through each element found and extract the quote, author, and tags
    for quote_count,quote_class in enumerate((quotes_class), start=1):
        # Extract quotes, authors, and tags from quote_class
        quote = quote_class.find('span', class_='text').text.strip()
        author = quote_class.find('small', class_='author').text.strip()
        tags = quote_class.find('div', class_='tags').text.strip()
        tags = re.sub(r'\s+', ' ', tags)  # Replace multiple whitespace with a single space
        tags = re.sub(r',\s*', ',', tags)  # Remove whitespace after commas
        tags = re.sub(r'^Tags:|,$', '', tags) # Remove Tags: and trailing commas
        
        #tag_list = []
        #for tag in tags.split('\n'):
        #    words = tag.split(',')
        #    tag_list.extend(words)
        
        # Send the extracted data to quote_element SubElement
        quote_element = ET.SubElement(page, "Quote", number=str(quote_count))
        tag_element = ET.SubElement(quote_element, "Tags")       
        ET.SubElement(quote_element, "QuoteText").text = quote
        ET.SubElement(quote_element, "Author").text = author
        ET.SubElement(quote_element, "Tags").text = tags
        
        for tag_count,tag in enumerate(tags.split('\n'), start=1):
            words = tag.split(',')
            for word in words:
                ET.SubElement(tag_element, "Tag", number=str(tag_count)).text = word.strip()
 
    print("Page {} complete!".format(str(page_count)))
    page_count +=1
    # Check to see if there is a next page
    try:
        next_link = soup.find('li', class_='next').find('a')
        url = "https://quotes.toscrape.com" + next_link['href']
    except AttributeError:
        print("No more pages to parse")
        url = None
        break

# Convert the root Element to a string and write to .xml
xml_str = ET.tostring(root, encoding='unicode')       
with open('quotes.xml', 'w') as outfile:
    outfile.write(xml_str)
