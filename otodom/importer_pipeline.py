# coding: utf8
import os
from datetime import datetime
from scrapy.exceptions import DropItem

from main import REDIS, TIME_FORMAT
from otodom import notifier

class ImporterPipeline(object):
    def __init__(self):
        self.rc = REDIS
        self.new_items = []

    def process_item(self, item, spider):
        if self.rc.exists(item['oid']):
            self.rc.hset(item['oid'], 'last_seen', item['last_seen'])
            self.rc.hincrby(item['oid'], 'seen_count', 1)
            raise DropItem('Duplicate item found: %s' % item)
        self.rc.hmset(item['oid'], {k:v for k, v in item.items() if k != 'oid'})
        self.rc.hset(item['oid'], 'created_at', datetime.now().strftime(TIME_FORMAT))
        self.new_items.append(item)
        return item

    def close_spider(self, spider):
        notifier.deliver_now(self.new_items)
