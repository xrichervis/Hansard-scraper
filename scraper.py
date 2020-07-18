import requests
import pandas as pd
from bs4 import BeautifulSoup

def getNumbers(text):
    result =[]
    numberStr = ""
    for char in text:
        if char >= '0' and char <='9':
            numberStr += char
        elif numberStr: #if numberStr is not emprty
            result.append(numberStr)
            numberStr=""
        if numberStr: # if numberStr is not empty after loop ended
            result += [numberStr] # alternative to appened
    return result

s = open("term_file.txt", "r")
m = s.read().splitlines()

for i in range (0, len(m)):
    x = m[i]
    print ("Searching for data relating to the search term: " + x )

    search_query = '"' + x + '"'

    url = 'https://hansard.parliament.uk/search/Contributions'
    # MM/DD/YYYY
    params = {
        'searchTerm': search_query,
        'startDate':'01/01/1980 00:00:00',
        'endDate':'07/18/2020 00:00:00',
        'partial':'True',
        'page':1,
    }

    soup = BeautifulSoup(requests.get(url, params=params).content, 'html.parser')
    pageStr = soup.find_all('p', class_="pagination-total")[0].getText()
    numberList = getNumbers(pageStr)
    pages = int(numberList[-1]) + int(1)

    all_data = []

    # number of pages a search returns
    for page in range(1, int(pages)):
        params['page'] = page

        print('Page {}...'.format(page))

        soup = BeautifulSoup(requests.get(url, params=params).content, 'html.parser')
        mention_containers = soup.find_all('div', class_="result contribution")
        if not mention_containers:
            print('Empty container!')

        for mention in mention_containers:
            topic = mention.div.span.text
            house = mention.find("img")["alt"]

            if house == "Lords Portcullis":
                 house = "House of Lords"
            elif house == "Commons Portcullis":
                 house = "House of Commons"
            else:
                 house = "N/A"

            added_column = search_query
            name = mention.find('div', class_="secondaryTitle").text
            date = mention.find('div', class_="").get_text(strip=True)

            all_data.append({'Date': date, 'Search Query': added_column, 'House': house, 'Speaker': name, 'Topic': topic})

    df = pd.DataFrame(all_data)
    print(df)

    # Converts our pandas dataframe into a nice CSV, columns separated by a hashtag.
    df.to_csv(search_query + '.csv', index=False, sep="#")
