import requests
from bs4 import BeautifulSoup


# get user input for yarn specifications and url
print("Enter yarn yards per 50 grams:")
yards = input()

print("Enter website url: ")
input_url = input()

# HTTP GET request
response =requests.get(url="https://www.yarn.com/")

# feed HTML doc to BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# identify link elements
link_elements = soup.select("a[href]")

urls = []

for link_element in link_elements:
    url = link_element['href']
    if input_url in url:
        urls.append(url)