import requests
from bs4 import BeautifulSoup

SHOP_MODES_MAX_COUNT = 10
SEVEN_DAYS_A_WEEK = {
    'Без выходных:': 'пн - вс'
}

html_doc = requests.get('https://www.mebelshara.ru/contacts')
soup = BeautifulSoup(html_doc.content, 'html.parser')

def get_mebelshara_offices():
    offices = []
    city_items = soup.select('.city-item')
    phone_items = soup.select('.phone-num.zphone')
    phones = [item.get_text() for item in phone_items]
    for item in city_items:
        cities = item.select('.js-city-name')
        city_name = cities[0].get_text() if cities else ''
        shop_list = item.select('.shop-list-item')
        for shop in shop_list:
            shop_name = shop.get('data-shop-name')
            shop_address = shop.get('data-shop-address')
            latitude = shop.get('data-shop-latitude')
            longitude = shop.get('data-shop-longitude')
            working_hours = []
            for i in range(SHOP_MODES_MAX_COUNT):
                shop_mode = shop.get('data-shop-mode%i' % (i))
                if SEVEN_DAYS_A_WEEK.get(shop_mode):
                    working_hours = ['%s %s' % (SEVEN_DAYS_A_WEEK[shop_mode], shop.get('data-shop-mode%i' % (i+1)))]
                    break
                if shop_mode:
                    working_hours.append(shop_mode)

            data = {
                'address': '%s, %s' % (city_name, shop_address),
                'latlon': [float(latitude), float(longitude)],
                'name': shop_name,
                'phones': phones,
                'working_hours': working_hours
            }
            offices.append(data)
    return offices
