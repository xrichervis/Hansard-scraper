from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import time

# lists which will become columns
topics = []
houses = []
names = []
dates = []

time.sleep(1)

print("Scraping some data...")

# the range will be the number of pages that your search returns
for i in range(2):

    page = i

    # add your url here // MAKE SURE THE "PARTIAL" PARAMETER EQUALS "TRUE" AND NOT "FALSE" otherwise scraping will return only blank values
    url = "https://hansard.parliament.uk/search/Contributions?startDate=2010-06-16&endDate=2020-06-25&searchTerm=%22civilian%20casualties%22&partial=True" + "&page=" + str(page)

    response = get(url)

    # BeautifulSoup is required for this scraper
    html_soup = BeautifulSoup(response.text, 'html.parser')

    # finds all the little contrainers that contain the data we want
    mention_containers = html_soup.find_all('div', class_="result contribution")

    # so for every mention we want to collect:
    for y in range((len(mention_containers))):

        mention = mention_containers[y]

        # the topic wherein civilian casualties was mentionned;
        topic = mention.div.span.text
        topics.append(topic)

        # either a Commons or Lords portcullis which designates which house of Parliament this mention was made
        house = mention.find("img")["alt"]

        #  and we then assign a text value to that image;
        if house == "Lords Portcullis":
            houses.append("House of Lords")
        elif house == "Commons Portcullis":
            houses.append("House of Commons")
        else:
            houses.append("N/A")

        # which MP or Lord mentionned civilian casualties;
        name = mention.find('div', class_="secondaryTitle").text
        names.append(name)

        # the date this mention was made;
        date = mention.find('div', class_="").text
        dates.append(date)

# turns your data into proper columns
hansard_dataset = pd.DataFrame(
    {'Date': dates, 'House': houses, 'Speaker': names, 'Topic': topics})

# allows us to check if we collected the correct amount of data we were expecting
print(hansard_dataset.info())

print("Turning this into a CSV...")

time.sleep(1)

# converts your pandas dataframe into a proper csv, separated with a hashtag to allow for easy delimitation when imported into an Excel spreadsheet or Google Sheet
hansard_dataset.to_csv('hansard.csv', index=False, sep="#")

# data this scraper collects with still need to be cleaned, but it's a good start 
