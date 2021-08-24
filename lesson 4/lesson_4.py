from lxml import html
import requests
from datetime import datetime
from pymongo import MongoClient
from pprint import pprint


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 '
                  'YaBrowser/21.6.3.757 Yowser/2.5 Safari/537.36'}

news_list = []

def get_news_lenta_ru():
    link_lenta = 'https://lenta.ru/'
    response = requests.get(link_lenta, headers=header)
    dom = html.fromstring(response.text)

    news_list = []

    xpath_1 = dom.xpath('//div[@class="span8 js-main__content"]//div[@class="item"]')
    xpath_2 = dom.xpath('//div[@class="item news b-tabloid__topic_news"]')

    for new in xpath_1:
        news_data = {}
        news_data['source'] = link_lenta
        news_data['name'] = new.xpath('.//a/text()')[0]
        news_data['link'] = f"{link_lenta}{new.xpath('.//a/@href')[0]}"
        news_data['time'] = new.xpath('.//a/time/@datetime')
        news_list.append(news_data)

    for new in xpath_2:
        news_data = {}
        news_data['source'] = link_lenta
        news_data['name'] = new.xpath('.//h3/text()')
        news_data['link'] = f"{link_lenta}{new.xpath('.//a/@href')}"
        news_data['time'] = new.xpath('.//span[@class="g-date item__date"]/text()')
        news_list.append(news_data)

    return(news_list)



def save_to_db():
    client = MongoClient('localhost', 27017)
    db = client['news_database']
    collections = db['news_list']
    for item in news_list:
        query = {
            'link': item['link']
        }

        update = {
            '$set': item
        }
        collections.update_one(query, update, upsert=True)


news_list.append(get_news_lenta_ru())