# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import re
from scrapy.exceptions import DropItem
from pymongo.errors import DuplicateKeyError


class SzplGovCnPipeline(object):
    item_to_collection_name = {
        'ProjectItem': 'projects',
        'CertItem': 'certifications',
        'HouseItem': 'houses'
    }

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print('------------inside pipeline------------------------------------------------')
        item_type = type(item).__name__
        # index_of_dot = item_type.rfind('.')
        # if index_of_dot != -1:
        #     item_type = item_type[index_of_dot + 1:]
        # else:
        #     raise DropItem("")

        spider.logger.info('----inserting item type :' + item_type)
        collection_name = self.item_to_collection_name.get(item_type)
        if not collection_name:
            raise DropItem
        elif item_type == 'HouseItem':
            price = re.search('\d+', item.get('record_price', ''))
            if price:
                item['record_price'] = price.group()
        spider.logger.info(collection_name)
        try:
            insert_result = self.db[collection_name].insert_one(dict(item))
            if insert_result.inserted_id:
                spider.logger.info('---insert result :' + str(insert_result.inserted_id))
        except DuplicateKeyError:
            # todo duplicate project should append possible new buidlings to the buildings property
            spider.logger.info('---duplicate ' + item_type + 'key for item\n' + str(item))

        return item
