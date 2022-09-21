import requests
from bs4 import BeautifulSoup

siteAddress = "https://www.kijiji.ca"
siteToronto = "/b-apartments-condos/city-of-toronto/page-"
siteCategory = "/c37l1700273"
sitePageNum = "1"
siteURL = siteAddress + siteToronto + sitePageNum + siteCategory
#<a href="/b-apartments-condos/city-of-toronto/page-2/c37l1700273">2</a> - pages


class Apartment:
    imageURL = str
    price = str
    description = str
    title = str
    date = str
    bedsNum = str
    location = str

    def __init__(self, imageURL, price, description, title,
                 date, bedsNum, location):
        self.imageURL = imageURL
        self.price = price
        self.description = description
        self.title = title
        self.date = date
        self.bedsNum = bedsNum
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

page = requests.get(siteAddress + siteToronto + sitePageNum + siteCategory)

if page.status_code == 200:
    print(page.status_code)
    print(f'Connection Open!')
    session = requests.session()
    allDateItems = []
    filteredItems = []
    response = session.get(siteURL, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    allDateItems = soup.find_all('span', attrs={"class":"date-posted"}) #it works!!!
    print(allDateItems)
    #for data in allItems:
    #    if data.find('div', class_='left-col') is not None:
    #        filteredItems.append(data.text)

    #for data in filteredItems:
    #    print(data)

    #for element in soup.find_all('div', class_='clearfix'):
        #imageURL = element.find('img').get('data-src')
        #price = element.find('div', class_='price').text.strip()
        #description = element.find('div', class_='description').text.strip()
        #title = element.find('div', class_='title').text.strip()
        #date = element.find('span', class_='date-posted').text.strip()
        #bedsNum = element.find('span', class_='bedrooms').text.strip()
        #location = element.find('div', class_='location').text.strip()

        #apart = Apartment(imageURL, price, description, title, date, bedsNum, location)

        #print(apart.__repr__())
else:
    print('Connection Error!')
