from datetime import datetime, timedelta
import requests
import time

import sqlalchemy
import urllib3.exceptions
from bs4 import BeautifulSoup

# imports for db
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, DateTime, create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

siteAddress = "https://www.kijiji.ca"
siteToronto = "/b-apartments-condos/city-of-toronto/page-"
siteCategory = "/c37l1700273?ad=offering"
sitePageNum = 84
site_first_page = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273?ad=offering'
allPages = []  # list of all pages
elementId = 0  # test element
is_last_page = True

# lists for data from all pages
image_url_items = []
title_items = []
date_items = []
location_items = []
bedrooms_items = []
description_items = []
price_items = []

# db area------------------------------------------------------------------------------

DeclarativeBase = declarative_base()


class Apartment(DeclarativeBase):
    __tablename__ = 'apartment'

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    imageURL = Column('imageURL', String)
    title = Column('title', String)
    date = Column('date', String)
    location = Column('location', String)
    bedrooms = Column('bedrooms', String)
    description = Column('description', String)
    price = Column('price', String)

    def __repr__(self):
        return "".format()


# create Postgres engine
engine = sqlalchemy.create_engine("postgresql+psycopg2://postgres:password@localhost/postgres")
engine.connect()

DeclarativeBase.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# session = Session()

print(f'Session with Postgres is open!')

#for item in session.query(Apartment):
#    print(item)


# db area------------------------------------------------------------------------------

# function for get dates(today and yesterday)
def get_dates(day):
    date_format = '%d-%m-%Y'
    now = datetime.now()
    if day == 't':
        today = now.strftime(date_format)
        return today
    else:
        yesterday = (now - timedelta(days=1)).strftime(date_format)
        return yesterday


# function for extracting text from tags
def extractTextFromTags(allItemsWithTag):
    allItemsClearText = []
    for i in allItemsWithTag:
        clearItem = i.get_text(strip=True)
        allItemsClearText.append(clearItem)
    return allItemsClearText


headers = {
    'authority': 'www.yeezysupply.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'accept-language': 'en-US,en;q=0.9',
}

page = requests.get(siteAddress + siteToronto + str(sitePageNum) + siteCategory)

# main function
while is_last_page == True:
    sitePageNum += 1
    # allPages.append(siteAddress + siteToronto + str(sitePageNum) + siteCategory)
    # if siteURL == exact_url:
    #    break
    # print(allPages)
    # print(len(allPages))

    if page.status_code == 200:
        print(f'Connection Open! Status Code: ' + str(page.status_code))
        try:
            session = requests.session()
            siteURL = siteAddress + siteToronto + str(sitePageNum) + siteCategory
            response = session.get(siteURL, headers=headers)
        except:
            continue
        exact_url = response.url
        print(f'Exact URL: ' + response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f'Page url: ' + str(siteURL))
        if siteURL != exact_url and exact_url != site_first_page:
            is_last_page = False
        else:
            print(f'Flag: ' + str(is_last_page))

            # extract price
            allPriceItems = soup.find_all('div', attrs={"class": "price"})
            clearPriceItems = extractTextFromTags(allPriceItems)

            # extract description
            allDescriptionItems = soup.find_all('div', attrs={"class": "description"})
            clearDescriptionItems = extractTextFromTags(allDescriptionItems)

            # extract title
            allTitleItems = soup.find_all('div', attrs={"class": "title"})
            clearTitleItems = extractTextFromTags(allTitleItems)

            # extract number of bedrooms
            allBedsNumItems = soup.find_all('span', attrs={"class": "bedrooms"})
            clearBedsNumItemsTemp = extractTextFromTags(allBedsNumItems)
            clearBedsNumItems = []
            for item in clearBedsNumItemsTemp:
                clearItemTemp = (item[5:])
                clearItem = ''
                for item in range(len(clearItemTemp)):
                    if clearItemTemp[item].isdigit():
                        clearItem = ''
                        clearItem += str(clearItemTemp[item])
                clearBedsNumItems.append(clearItem)

            # extract location
            allLocationItems = soup.find_all('div', attrs={"class": "location"})
            clearLocationItemsTemp = extractTextFromTags(allLocationItems)
            clearLocationItems = []
            for item in clearLocationItemsTemp:
                if item.endswith('Yesterday'):
                    clearLocationItem = (item[:-9])
                elif item.endswith('hours ago'):
                    clearLocationItem = (item[:-12])
                elif item.endswith('minutes ago'):
                    clearLocationItem = (item[:-14])
                else:
                    clearLocationItem = (item[:-10])
                clearLocationItems.append(clearLocationItem)

            # alternate extract date
            clearDateItems = []
            for item in clearLocationItemsTemp:
                clearItem = (item[-10:])
                yesterday = 'y'
                today = 't'
                if clearItem.endswith('Yesterday'):
                    clearItem = get_dates(yesterday)
                elif clearItem.endswith(' ago'):
                    clearItem = get_dates(today)
                else:
                    clearItem = clearItem.replace('/', '-')
                clearDateItems.append(clearItem)

            # extract image URL
            allImageURLItems = soup.find_all('div', attrs={"class": "image"})
            clearImageURLItems = []
            for i in allImageURLItems:
                i = str(i)
                soup = BeautifulSoup(i, 'html.parser')
                images = soup.find_all('img')
                for image in images:
                    try:
                        imageURL = image['data-src']
                    except:
                        imageURL = image['src']
                    clearImageURLItems.append(imageURL)

            print(f'Items on page: ' + str(len(clearBedsNumItems)))

            # get elements from pages and add into common list
            print(f'Image URL: ' + str(clearImageURLItems[elementId]))
            for i in clearImageURLItems:
                image_url_items.append(i)
            print(f'Price: ' + clearPriceItems[elementId])
            for i in clearPriceItems:
                price_items.append(i)
            print(f'Description: ' + clearDescriptionItems[elementId])
            for i in clearDescriptionItems:
                description_items.append(i)
            print(f'Title: ' + clearTitleItems[elementId])
            for i in clearTitleItems:
                title_items.append(i)
            print(f'Date: ' + clearDateItems[elementId])
            for i in clearDateItems:
                date_items.append(i)
            print(f'Bedrooms: ' + clearBedsNumItems[elementId])
            for i in clearBedsNumItems:
                bedrooms_items.append(i)
            print(f'Location: ' + clearLocationItems[elementId])
            for i in clearLocationItems:
                location_items.append(i)

    elif page.status_code == 500:
        print(f'Server Error!')
    else:
        print('Some Connection Error!')
    time.sleep(3)
print(f'Images num: ' + str(len(image_url_items)))
print(f'Price num: ' + str(len(price_items)))
print(f'Description num: ' + str(len(description_items)))
print(f'Beds num: ' + str(len(bedrooms_items)))
print(f'Title num: ' + str(len(title_items)))
print(f'Location num: ' + str(len(location_items)))
print(f'Date num: ' + str(len(date_items)))

# add items to Postgres--------------------------------------------------

#new_apartment = Apartment(imageURL='imageURL',
#                            title='Title',
#                            date='09-10-2022',
#                            location='LA',
#                            bedrooms='4',
#                            description='Some text',
#                            price='500')

while True:
    session = Session()
    for image_url, title, date, location, bedrooms, description, price in zip(image_url_items,
                                                                              title_items,
                                                                              date_items,
                                                                              location_items,
                                                                              bedrooms_items,
                                                                              description_items,
                                                                              price_items):
        new_apartment = Apartment(imageURL=image_url,
                                  title=title,
                                  date=date,
                                  location=location,
                                  bedrooms=bedrooms,
                                  description=description,
                                  price=price)
        session.add(new_apartment)
        session.commit()
    break
    for i in image_url_items:
        #session = Session()
        new_apartment = Apartment(imageURL=i)
        session.add(new_apartment)
        #session.commit()
    for i in title_items:
        #session = Session()
        new_apartment = Apartment(title=i)
        session.add(new_apartment)
        #session.commit()
    #session.add(new_apartment)
    session.commit()
    for i in date_items:
        session = Session()
        new_apartment = Apartment(date=i)
        session.add(new_apartment)
        session.commit()
    for i in location_items:
        session = Session()
        new_apartment = Apartment(location=i)
        session.add(new_apartment)
        session.commit()
    for i in bedrooms_items:
        session = Session()
        new_apartment = Apartment(bedrooms=i)
        session.add(new_apartment)
        session.commit()
    for i in description_items:
        session = Session()
        new_apartment = Apartment(description=i)
        session.add(new_apartment)
        session.commit()
    for i in price_items:
        session = Session()
        new_apartment = Apartment(price=i)
        session.add(new_apartment)
        session.commit()

print(f'----------------Completed----------------')
