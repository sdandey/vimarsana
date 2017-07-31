from bs4 import BeautifulSoup
import urllib.request
import csv
url = 'https://en.wikipedia.org/wiki/List_of_English_districts_by_population'

def get_wiki_url_for_each_country():
    city_extract_url ={}
    city_extract_url['india'] = 'https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population'
    city_extract_url['usa'] = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
    city_extract_url['canada'] = 'https://en.wikipedia.org/wiki/List_of_the_100_largest_municipalities_in_Canada_by_population'
    city_extract_url['uk'] = 'https://en.wikipedia.org/wiki/List_of_English_districts_by_population'
    return city_extract_url


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
        if (len(row) >= 4):
            cities.append(row[1])
    return cities


cities = extract_cities_information_from_wiki(url)
print ('total count:' + str(len(cities)))
for city in cities:
    print (city)


