from typing import List, Any
import datetime
import requests
from bs4 import BeautifulSoup

siteAddress = "https://www.kijiji.ca"
siteToronto = "/b-apartments-condos/city-of-toronto/page-"
siteCategory = "/c37l1700273"
sitePageNum = 0
allPages = []  # list of all pages
lastPage = 94  # temporary variable
dt = datetime.datetime.today()
today = dt.strftime("%d-%m-%Y")
elementId = 0

# now this class don't use
class Apartment:
    imageURL = str
    price = str
    description = str
    title = str
    date = str
    bedsNum = str
    location = str

    def __init__(self, imageurl, price, description, title,
                 date, bedsnum, location):
        self.imageURL = imageurl
        self.price = price
        self.description = description
        self.title = title
        self.date = date
        self.bedsNum = bedsnum
        self.location = location

    def __repr__(self):
        return str(self.__dict__)


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

# extract number of pages, now it's don't work :(
while True:
    sitePageNum += 1
    allPages.append(siteAddress + siteToronto + str(sitePageNum) + siteCategory)
    if page.status_code != 200 or sitePageNum >= lastPage:
        break
print(allPages[lastPage - 1])
print(len(allPages))

# function for extracting text from text
def extractTextFromTags(allItemsWithTag):
    allItemsClearText = []
    for item in allItemsWithTag:
        clearItem = item.get_text(strip=True)
        allItemsClearText.append(clearItem)
    return allItemsClearText


if page.status_code == 200:
    print(f'Connection Open! Status Code: ' + str(page.status_code))
    session = requests.session()
    siteURL = siteAddress + siteToronto + str(sitePageNum) + siteCategory
    response = session.get(siteURL, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    allImageURLItems = soup.find_all('div', attrs={"class": "image"})

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
        clearItem = (item[:-10])
        clearLocationItems.append(clearItem)

    # alternate extract date
    clearDateItems = []
    for item in clearLocationItemsTemp:
        clearItem = (item[-10:])
        if clearItem == 'oYesterday':
            clearItem = today
        else:
            clearItem = clearItem.replace('/', '-')
        clearDateItems.append(clearItem)

    # print(allImageURLItems[5])
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

# temp area!!!!!!!