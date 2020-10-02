# Libraries

# Python
import os
import datetime
import json
# WebScraping
import requests
import lxml.html as html

"""This scraper extract data about rental departments in bogota from www.fincaraiz.com.co, then
it creates txt files with each place extracted in a JSON format"""


HOME_URL = 'https://www.fincaraiz.com.co/apartamentos/arriendo/bogota/'

XPATH_LINK_TO_ARTICLE = '//div[@class="span-title"]/a/@href'

XPATH_TITLE = '//div[@class="title"]/div[@class="box"]/h1/text()'
XPATH_SUMMARY = '//div[@class="description"]/div[@class="boxcube"]/p/text()'
XPATH_ADDRESS = '//div[@class="title"]/div[@class="box"]/h1/span/text()'
XPATH_PRICE = '//div[@class="price"]/h2/text()'
XPATH_AREA = '//div[@class="features clearfix"]/span[@class="advertSurface"]/text()'
XPATH_ROOMS = '//div[@class="features clearfix"]/span[@class="advertRooms"]/text()'
XPATH_BATHS = '//div[@class="features clearfix"]/span[@class="advertBaths"]/text()'
XPATH_GARAGES = '//div[@class="features clearfix"]/span[@class="advertGarages"]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:

            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:

                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                summary = summary.replace('\"', '')
                price = parsed.xpath(XPATH_PRICE)[0]
                price = price.replace('\"', '')
                price = price.replace('.', '')
                address = parsed.xpath(XPATH_ADDRESS)[0]
                address = address.replace('\"', '')
                area = parsed.xpath(XPATH_AREA)[1]
                area = area.replace('\"', '')
                area = area.replace(' ', '')
                area = area.replace(',', '.')
                area = area.replace('\r\n', '')
                rooms = parsed.xpath(XPATH_ROOMS)[1]
                rooms = rooms.replace('\"', '')
                rooms = rooms.replace(' ', '')
                rooms = rooms.replace('\r\n', '')
                rooms = rooms.replace('Habitaciones:', '')
                bathrooms = parsed.xpath(XPATH_BATHS)[1]
                bathrooms = bathrooms.replace('\"', '')
                bathrooms = bathrooms.replace(' ', '')
                bathrooms = bathrooms.replace('\r\n', '')
                bathrooms = bathrooms.replace('Baños:', '')

            except IndexError:

                return

            with open(f'{today}/{address}.txt', 'w', encoding='utf-8') as f:
                f.write('{\"namePlace\": \"')
                f.write(address + '\"' + ',')
                f.write('\"location\": \"')
                f.write(address + '\"' + ',')
                f.write('\"images\": \"')
                f.write('' + '\"' + ',')
                f.write('\"price\": \"')
                f.write(price + '\"' + ',')
                f.write('\"avalaible\": \"')
                f.write('true' + '\"' + ',')
                f.write('\"furniture\": \"')
                f.write('true' + '\"' + ',')
                f.write('\"wifi\": \"')
                f.write('true' + '\"' + ',')
                f.write('\"bath\": \"')
                f.write(bathrooms + '\"' + ',')
                f.write('\"parking\": \"')
                f.write('true' + '\"' + ',')
                f.write('\"tv\": \"')
                f.write('true' + '\"' + ',')
                f.write('\"cleaning\": \"')
                f.write('false' + '\"' + ',')
                f.write('\"closet\": \"')
                f.write('false' + '\"' + ',')
                f.write('\"size\": \"')
                f.write(area + '\"' + ',')
                f.write('\"description\": \"')
                f.write(summary + '\"' + ',')
                f.write('\"profile_id\": \"')
                f.write('5f6d399b223f25242cf09644' + '\"' + ',')
                f.write('\"__v\": \"')
                f.write('0' + '\"' + '}')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)




def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            links_to_notices_complete = ['https://www.fincaraiz.com.co'
                                        + item for item in links_to_notices]
            print(links_to_notices_complete)

            today = datetime.date.today().strftime('%d-%m-%Y')

            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links_to_notices_complete:
                parse_notice(link, today)


        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        pass


def run():
    parse_home()



if __name__ == '__main__':
    run()