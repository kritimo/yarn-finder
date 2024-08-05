import requests
from bs4 import BeautifulSoup


# get user input for yarn specifications and url
print("Enter yarn yards per 50 grams:")
yards = input()

print("Enter website url: ")
input_url = input()

# initialize lists
urls = [input_url]
yarns = []


# TODO: add check to make sure input url is valid

while len(urls) != 0:

    # pop top url
    current_url = urls.pop()

    # HTTP GET request
    response =requests.get(current_url)

    # feed HTML doc to BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # identify link elements
    link_elements = soup.select("a[href]")

    for link_element in link_elements:
        url = link_element['href']
        if input_url in url:
            urls.append(url)
    
    # TODO: add check for correct yarn weight

    # determine yarn information

    yarn = {}
    yarn["url"] = current_url
    yarn["name"] = soup.select_one(".sf-heading__title").text()
    yarn["price"] = soup.select_one(".product-price__regular")

    yarns.append(yarn)

# TODO: open CSV output file

