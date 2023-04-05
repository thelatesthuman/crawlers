import csv
import requests
from bs4 import BeautifulSoup
import re

url = "https://quotes.toscrape.com"

author_list = []
quote_list = []
tags_list = []

page_count = 1
while url:
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    quotes_class = soup.find_all('div', class_='quote')

    # Parse through each element found and extract the quote, author, and tags
    for quote_class in quotes_class:
        author = quote_class.find('small', class_='author').text.strip()
        text = quote_class.find('span', class_='text').text.strip()
        tags = quote_class.find('div', class_='tags').text.lstrip().replace('Tags:', '').replace('\n', ',').rstrip(',')
        tags = re.sub(r'^,\s*,', '', tags) 
        author_list.append(author)
        quote_list.append(text)
        tags_list.append(tags)
    
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

# Format and write the data in .csv format
quote_tuples = list(zip(author_list, quote_list, tags_list))
fields = ['authors', 'quotes', 'tags']
with open('authors.csv', 'w') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fields)
    writer.writeheader()
    for quote_tuple in quote_tuples:
        author_dict = {'authors': quote_tuple[0]}
        quote_dict = {'quotes': quote_tuple[1]}
        tags_dict = {'tags': quote_tuple[2]}
        writer.writerow({**author_dict, **quote_dict, **tags_dict})
