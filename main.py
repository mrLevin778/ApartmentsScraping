from datetime import datetime, timedelta
import requests
import urllib3.exceptions
from bs4 import BeautifulSoup

siteAddress = "https://www.kijiji.ca"
siteToronto = "/b-apartments-condos/city-of-toronto/page-"
siteCategory = "/c37l1700273?ad=offering"
sitePageNum = 83
site_first_page = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273?ad=offering'
allPages = []  # list of all pages
elementId = 0  # test element


# lists for data from all pages
image_url_items = []
title_items = []
date_items = []
location_items = []
bedrooms_items = []
description_items = []
price_items = []


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
while True:
    is_last_page = False
    sitePageNum += 1
    #allPages.append(siteAddress + siteToronto + str(sitePageNum) + siteCategory)
    #if siteURL == exact_url:
    #    break
    #print(allPages)
    #print(len(allPages))

    if page.status_code == 200:
        print(f'Connection Open! Status Code: ' + str(page.status_code))
        session = requests.session()
        siteURL = siteAddress + siteToronto + str(sitePageNum) + siteCategory

        response = session.get(siteURL, headers=headers)
        exact_url = response.url
        print(f'Exact URL: ' + response.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f'Page url: ' + str(siteURL))
        if siteURL != exact_url and exact_url != site_first_page:
            is_last_page = True
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

        print(f'Image URL: ' + str(clearImageURLItems[elementId]))
        print(f'Price: ' + clearPriceItems[elementId])
        print(f'Description: ' + clearDescriptionItems[elementId])
        print(f'Title: ' + clearTitleItems[elementId])
        print(f'Date: ' + clearDateItems[elementId])
        print(f'Bedrooms: ' + clearBedsNumItems[elementId])
        print(f'Location: ' + clearLocationItems[elementId])

        # for element in soup.find_all('div', class_='clearfix'):

        # apart = Apartment(imageurl, price, description, title, date, bedsnum, location)

        # print(apart.__repr__())
    else:
        print('Connection Error or end of pages!')
