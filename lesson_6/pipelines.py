# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from itemadapter import ItemAdapter
import hashlib
from random import getrandbits
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client['vacansy_hhry']

    def process_item(self, item, spider):
        vacancy_info = dict()
        vacancy_info['name'] = item['name']
        vacancy_info['link'] = item['link']
        vacancy_info['pay_min'] = 0
        vacancy_info['pay_max'] = 0
        vacancy_info['pay_valuta'] = ''
        vacancy_info['site'] = item['site']

        vacancy_pay = item['pay'].split()
        if vacancy_pay[0] == 'от':
            vacancy_info['pay_min'] = int(f'{vacancy_pay[1]}{vacancy_pay[2]}')
        elif vacancy_pay[0] == 'до':
            vacancy_info['pay_max'] = int(f'{vacancy_pay[1]}{vacancy_pay[2]}')
        else:
            vacancy_info['pay_min'] = int(f'{vacancy_pay[0]}{vacancy_pay[1]}')
            vacancy_info['pay_max'] = int(f'{vacancy_pay[3]}{vacancy_pay[4]}')

        vacancy_info['pay_valuta'] = vacancy_pay[-1]
        vacancy_info['_id'] = hashlib.sha1(str(vacancy_info).encode()).hexdigest()

        collections = self.mongobase[spider.name]
        collections.update_one({'_id': {'$eq': vacancy_info['_id']}}, {'$set': vacancy_info}, upsert=True)
        return vacancy_info
