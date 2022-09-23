from datetime import datetime, timedelta
import requests
import time
from bs4 import BeautifulSoup

# imports for db
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

site_address = "https://www.kijiji.ca"
site_toronto = "/b-apartments-condos/city-of-toronto/page-"
site_category = "/c37l1700273?ad=offering"
site_page_num = 84  # AFTER TESTS CHANGE TO ZERO!!!
site_first_page = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273?ad=offering'
is_last_page = True

# lists for data from all pages
image_url_items = []
title_items = []
date_items = []
location_items = []
bedrooms_items = []
description_items = []
price_items = []

print(f'App is RUN')

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
def extract_text_from_tags(all_items_with_tag):
    all_items_clear_text = []
    for i in all_items_with_tag:
        clear_item = i.get_text(strip=True)
        all_items_clear_text.append(clear_item)
    return all_items_clear_text


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

page = requests.get(site_address + site_toronto + str(site_page_num) + site_category)

# main function for data scraping
while is_last_page == True:
    site_page_num += 1

    if page.status_code == 200:
        try:
            session = requests.session()
            site_url = site_address + site_toronto + str(site_page_num) + site_category
            response = session.get(site_url, headers=headers)
        except requests.exceptions.ChunkedEncodingError:
            print(f'Exception!')
            continue
        exact_url = response.url
        # print(f'Exact URL: ' + response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(f'Page url: ' + str(siteURL))
        if site_url != exact_url and exact_url != site_first_page:
            is_last_page = False
        else:
            print(f'Flag: ' + str(is_last_page))

            # extract price
            all_price_items = soup.find_all('div', attrs={"class": "price"})
            clear_price_items = extract_text_from_tags(all_price_items)

            # extract description
            all_description_items = soup.find_all('div', attrs={"class": "description"})
            clear_description_items = extract_text_from_tags(all_description_items)

            # extract title
            all_title_items = soup.find_all('div', attrs={"class": "title"})
            clear_title_items = extract_text_from_tags(all_title_items)

            # extract number of bedrooms
            all_beds_num_items = soup.find_all('span', attrs={"class": "bedrooms"})
            clear_beds_num_items_temp = extract_text_from_tags(all_beds_num_items)
            clear_beds_num_items = []
            for item in clear_beds_num_items_temp:
                clear_item_temp = (item[5:])
                clear_item = ''
                for item in range(len(clear_item_temp)):
                    if clear_item_temp[item].isdigit():
                        clear_item = ''
                        clear_item += str(clear_item_temp[item])
                clear_beds_num_items.append(clear_item)

            # extract location
            all_location_items = soup.find_all('div', attrs={"class": "location"})
            clear_location_items_temp = extract_text_from_tags(all_location_items)
            clear_location_items = []
            for item in clear_location_items_temp:
                if item.endswith('Yesterday'):
                    clear_location_item = (item[:-9])
                elif item.endswith('hours ago'):
                    clear_location_item = (item[:-12])
                elif item.endswith('minutes ago'):
                    clear_location_item = (item[:-14])
                else:
                    clear_location_item = (item[:-10])
                clear_location_items.append(clear_location_item)

            # alternate extract date
            clear_date_items = []
            for item in clear_location_items_temp:
                clear_item = (item[-10:])
                yesterday = 'y'
                today = 't'
                if clear_item.endswith('Yesterday'):
                    clear_item = get_dates(yesterday)
                elif clear_item.endswith(' ago'):
                    clear_item = get_dates(today)
                else:
                    clear_item = clear_item.replace('/', '-')
                clear_date_items.append(clear_item)

            # extract image URL
            all_image_url_items = soup.find_all('div', attrs={"class": "image"})
            clear_image_url_items = []
            for i in all_image_url_items:
                i = str(i)
                soup = BeautifulSoup(i, 'html.parser')
                images = soup.find_all('img')
                for image in images:
                    try:
                        image_url = image['data-src']
                    except:
                        image_url = image['src']
                    clear_image_url_items.append(image_url)

            print(f'Items on page: ' + str(len(clear_beds_num_items)))

            # get elements from pages and add into common list
            for i in clear_image_url_items:
                image_url_items.append(i)
            for i in clear_price_items:
                price_items.append(i)
            for i in clear_description_items:
                description_items.append(i)
            for i in clear_title_items:
                title_items.append(i)
            for i in clear_date_items:
                date_items.append(i)
            for i in clear_beds_num_items:
                bedrooms_items.append(i)
            for i in clear_location_items:
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

session = Session()
# with loop add data to Postgres
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

print(f'----------------END----------------')
