import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':

    page = 1
    while True:
        print("Page:", page)
        url = f"http://quotes.toscrape.com/page/{page}/"

        # get the raw HTML response
        response = requests.get(url)

        # parse it to a soup object allowing us to manipulate it
        soup = BeautifulSoup(response.text, 'html.parser')

        # get all spans that have 'text' as a css class
        quotes = soup.find_all('div', class_='quote')

        # we have reached the last page (that is empty)
        if not quotes:
            break

        # iterate all the specified divs
        for quote in quotes:

            # get the attributes of interest
            text = quote.find('span', class_='text').text
            author = quote.find('small').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]

            # print them
            print("Quote:", text)
            print("Author:", author)
            print("Tags:", tags)
            print()  # change line

        page += 1

