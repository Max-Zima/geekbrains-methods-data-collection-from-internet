# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import hashlib
from scrapy.utils.python import to_bytes
from pymongo import MongoClient


class InstagramPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client['Instagram']

    def process_item(self, item, spider):
        collections = self.mongobase[spider.name]
        collections.update_one({'_id': {'$eq': item['_id']}}, {'$set': item}, upsert=True)
        return item


class InstagramlinImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['pic_url']:
            for img in item['pic_url']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
        return item

    def item_completed(self, results, item, info):
        if results:
            item['pic_url'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_name = hashlib.sha1(to_bytes(request.url)).hexdigest()
        if item:
            return f'{item["_id"]}/{image_name}.jpg'
        else:
            return f'full/{image_name}.jpg'