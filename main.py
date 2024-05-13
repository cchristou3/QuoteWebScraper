import csv
from typing import List

import requests
from bs4 import BeautifulSoup, Tag

from models import Quote


def extract_quote_info(quote: Tag) -> Quote:
    # get the attributes of interest
    text = quote.find_next('span', class_='text').text
    author = quote.find_next('small').text
    tags = [tag.text for tag in quote.find_all('a', class_='tag')]

    # print them
    print("Quote:", text)
    print("Author:", author)
    print("Tags:", tags)
    print()  # change line

    return Quote(text=text, author=author, tags=tags)


def get_next_page_quotes(page_number: int):
    print("Page:", page_number)
    url = f"http://quotes.toscrape.com/page/{page_number}/"

    # get the raw HTML response
    response = requests.get(url)

    if response.status_code != 200:
        return []

    # parse it to a soup object allowing us to manipulate it
    soup = BeautifulSoup(response.text, 'html.parser')

    # get all spans that have 'text' as a css class
    return soup.find_all('div', class_='quote')


def store_to_csv(csv_name: str, quote_rows: List[Quote]):
    # open the csv file, create a new one if it does not exist
    with open(csv_name, 'w', newline='', encoding='utf-8') as csv_file:
        # the first row are the headers
        field_names = ['Quote', 'Author', 'Tags']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

        # next, write each row to the sheet
        for quote in quote_rows:
            writer.writerow(quote.to_excel_row())


if __name__ == '__main__':

    quote_rows = []

    page_number = 1

    while True:

        # get all spans that have 'text' as a css class
        quotes = get_next_page_quotes(page_number)

        # we have reached the last page (that is empty)
        if not quotes:
            break

        # iterate all the specified divs
        for quote in quotes:
            quote_rows.append(extract_quote_info(quote))

        page_number += 1

    store_to_csv('quotes.csv', quote_rows)
