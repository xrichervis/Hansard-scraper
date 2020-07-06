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


# For this test, I'm collecting only the first 16 pages
for i in range(1,15):

    page = i

    # url which displays the data I'm looking for
    url = "https://hansard.parliament.uk/search/Contributions?endDate=2020-06-25&page=" + str(page) + "&searchTerm=%22civilian+casualties%22&startDate=2015-06-25&partial=True"

    response = get(url)

    # Parse the content of the request with BeautifulSoup
    html_soup = BeautifulSoup(response.text, 'html.parser')

    # Select all the 20 mention mention_containerss from a single page
    mention_containers = html_soup.find_all('div', class_ = "result contribution")

# I need to get data on each "container" of data: so for every mention
    for y in range((len(mention_containers))):

                mention = mention_containers[y]

                # the topic wherein civilian casualties was mentionned
                topic = mention.div.span.text
                topics.append(topic)

                # an SVG of either a Commons or Lords portcullis to designate
                # whether this mention was made in the House of Lords or House of Commons

                house = mention.find("img")["alt"]
                houses.append(house)

                # which MP or Lord mentionned civilian casualties
                name = mention.find('div', class_ = "secondaryTitle").text
                names.append(name)

                # what day this was
                date = mention.find('div', class_ = "").text
                dates.append(date)

# turning my data into columns
hansard_dataset = pd.DataFrame({'Date': dates, 'House': houses, 'Speaker': names, 'Topic': topics})

print(hansard_dataset.info())

print("Turning this into a CSV...")

time.sleep(1)

hansard_dataset.to_csv('hansard.csv', index=False, sep="#")
