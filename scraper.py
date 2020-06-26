from requests import get
from bs4 import BeautifulSoup
import pandas as pd

# lists which will become columns
topics = []
names = []
dates = []
quotes = []

# For this test, I'm collecting only the first 16 pages
for i in range(1,16):

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

                # which MP or Lord mentionned civilian casualties
                name = mention.find('div', class_ = "secondaryTitle").text
                names.append(name)

                # what day this was
                date = mention.find('div', class_ = "").text
                dates.append(date)

                # what was the fuller context of this mention
                quote = mention.find('div', class_ = "content hidden-xs").text
                quotes.append(quote)

# turning my data into columns
hansard_dataset = pd.DataFrame({'Date': dates, 'Speaker': names, 'Topic': topics, 'Full Quote': quotes})

print(hansard_dataset.info())

print(hansard_dataset)
