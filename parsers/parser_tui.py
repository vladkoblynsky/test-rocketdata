import requests

SHOP_MODES_MAX_COUNT = 10
SATURDAY = 'saturday'
SUNDAY = 'sunday'
DAYS = {
    'workdays': 'пн - пт',
    'saturday': 'сб',
    'sunday': 'вс',
    'weekends': 'cб - вс',
}

response = requests.get('https://www.tui.ru/api/office/list/?cityId=1&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false')

def get_tui_offices():
    offices = []
    items = response.json()
    for item in items:
        phones = item.get('phones')
        if phones:
            phones = [phone.get('phone', '').strip() for phone in phones]
        working_hours = []
        operation_hours = item.get('hoursOfOperation')
        for day, hours in item.get('hoursOfOperation').items():
            if not hours.get('isDayOff'):
                if day == SATURDAY and hours.get('startStr') == operation_hours[SUNDAY].get('startStr') and hours.get('endStr') == operation_hours[SUNDAY].get('endStr'):
                    working_hours.append('%s %s - %s' % (DAYS.get('weekends'), hours.get('startStr'), hours.get('endStr')))
                    break
                else:
                    working_hours.append('%s %s - %s' % (DAYS.get(day, ''), hours.get('startStr'), hours.get('endStr')))
        data = {
            'address': item.get('address'),
            'latlon': [item.get('latitude'), item.get('longitude')],
            'name': item.get('name'),
            'phones': phones,
            'working_hours': working_hours
        }
        offices.append(data)

    return offices