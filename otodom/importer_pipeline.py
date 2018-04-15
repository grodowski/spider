# coding: utf8
import redis
import os
from scrapy.exceptions import DropItem

from otodom import notifier

class ImporterPipeline(object):
    def __init__(self):
        self.rc = redis.from_url(os.getenv('REDIS_URL'))
        self.new_items = []

    def process_item(self, item, spider):
        if self.rc.exists(item['oid']):
            raise DropItem("Duplicate item found: %s" % item)
        self.rc.set(item['oid'], {k:v for k, v in item.items() if k != 'oid'})
        self.new_items.append(item)
        return item

    def close_spider(self, spider):
        notifier.deliver_now(self.new_items)
