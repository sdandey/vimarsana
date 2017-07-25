import json
import pprint
import urllib.request

import re
from bs4 import BeautifulSoup
import facebook
from pymongo import MongoClient

wikiCitiUrl = 'https://en.wikipedia.org/wiki/List_of_cities_in_India_by_population'
accesstoken = 'EAAXg2lcZCvBUBAHYq8SvI5eixorhcOxAslO2i0FUBQJp3mLuj9pFv9vh4QJeulIrmCfndmTwkwzdVvXClsz3ZBtBOcjrkwVZAnPyTbFoX0OSygHdVTva240AO2W7ZBCH1ZAZAhdWYjnBZBHXHBMZAHbAFI4DbzblUtowb25fxVG75AZDZD'
#name of the app vimarsana for santoshdandey user
fb_appid='1654603254840341'
fb_secret='147879469d33521da94c3c6df27dc3aa'
mongo_host= 'vps110824.vps.ovh.ca'

mongo_port= 27017

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



def extract_events(city):
    graph = facebook.GraphAPI(access_token=accesstoken, version=2.7)
    events = graph.request('/search?q='+city+'&type=event&limit=10000')
    return events['data']

def long_live_fb_access_token():
    graph = facebook.GraphAPI(access_token=accesstoken, version=2.7)
    graph.extend_access_token(fb_appid,fb_secret)

def extract_event_for_city():
    #Long Lived Access Token that's there for 60 days
    fbApi = "https://graph.facebook.com/v2.10/search?q=hyderabad%20events&type=event&limit=500&access_token=" + accesstoken
    data = json.load(urllib.request.urlopen(fbApi))
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

def insert_record_in_database(data, city):
    client = MongoClient(mongo_host, mongo_port)
    db = client['vimarsana']
    fb_events=db.fb_events
    result=fb_events.insert_many(data)
    print('inserted ' + str(len(result.inserted_ids)) + ' events in the database for city ' + city)


def extract_event_information():
    cities = extract_cities_information_from_wiki(wikiCitiUrl)
    total_events = 0
    for city in cities:
        regex = re.compile('[^a-zA-Z]')
        events = extract_events(regex.sub('',city))
        # print('grabbed ' + str(len(events)) + ' events for city ' + city)
        if (len(events) > 0):
            insert_record_in_database(events, city)
        total_events = total_events + len(events)
    print("total events from different cities:" + str(total_events))


extract_event_information()
#print('saving all events into a json file')

#with open('events.json', 'w') as outfile:
#    json.dump(json.dumps(total_events),outfile)




