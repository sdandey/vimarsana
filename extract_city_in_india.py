from bs4 import BeautifulSoup
import urllib.request
import csv
url = 'https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population'


def extract_cities_information_from_wiki(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), "lxml")
    # cities_list = soup.find("table",{"class":"wikitable"})
    cities_list = soup.findAll("table")
    rows = list()
    for cities in cities_list:
        if cities.findParent("table") is None:
            for row in cities.findAll("tr"):
                cols = row.findAll('td')
                cols = [ele.text.strip() for ele in cols]
                rows.append([ele for ele in cols if ele])
    cities = list()
    for row in rows:
        if (len(row) > 4):
            cities.append(row[1])
    return cities

cities = extract_cities_information_from_wiki(url)
for city in cities:
    print (city)


