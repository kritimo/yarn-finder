import requests
from bs4 import BeautifulSoup
import csv


# get user input for yarn specifications and url
print("Enter yarn yards per 50 grams:")
desired_yards = float(input())

print("Enter acceptable deviation in yarns per 50 grams:")
plus_minus = float(input())

print("How many products should we find?")
goal_products = int(input())

print("Enter website url: ")
input_url = input()


# initialize lists
urls = [input_url]
visited_urls = ["https://www.yarn.com/"]
yarns = []
numYarns = 0


# TODO: add check to make sure input url is valid

while len(urls) != 0:

    # pop top url
    current_url = urls.pop()

    print(current_url)

    # HTTP GET request
    response =requests.get(current_url)

    # add to list of visited urls to prevent revisiting
    visited_urls.append(current_url)

    # feed HTML doc to BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # identify link elements
    link_elements = soup.select("a[href]")

    # add all valid links to urls list
    for link_element in link_elements:
        url = link_element['href']
        if "https://www.yarn.com/" in url:
            if url not in visited_urls:
                urls.append(url)

    # determine if page is a yarn product page
    isProductPage = False
    isYarn = False
    subtitle = ""

    if soup.select_one(".subtitle"):

        isProductPage = True
        subtitle = soup.select_one(".subtitle").text

        if("yds" in subtitle):
            isYarn = True


    if isYarn:
        # parse subtitle string for relevant information

        comma_index = subtitle.find(", ")
        yds_index = subtitle.find("yds")
        slash_index = subtitle.find(")/")
        grams_index = subtitle.find("g")

        # calculate how many yards of yarn per fifty grams
        grams = 0
        yards = 0
        yards_per_fifty = 0

        grams = float(subtitle[slash_index+2:grams_index])
        yards = float(subtitle[comma_index+2:yds_index])
        yards_per_fifty = (yards/grams) * 50.0

        # if yarn is within range of yardage, add to list

        if desired_yards - plus_minus <= yards_per_fifty and desired_yards + plus_minus >= yards_per_fifty:

            yarn = {}
            yarn["url"] = current_url
            yarn["name"] = soup.select_one(".sf-heading__title").text.strip()
            yarn["price"] = float(soup.select_one(".product-price__regular").text.strip().replace('$',''))
            yarn["grams"] = grams
            yarn["yards"] = yards

            numYarns += 1
            yarns.append(yarn)
    
    if numYarns > goal_products:
        break


# write output to csv file
with open('yarns.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["URL", "Name", "Price", "Grams", "Yards"])

    for yarn in yarns:
        writer.writerow(yarn.values())

