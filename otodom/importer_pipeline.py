# coding: utf8
import os
from datetime import datetime
from scrapy.exceptions import DropItem

from constants import REDIS, TIME_FORMAT
from otodom import notifier

class ImporterPipeline(object):
    def __init__(self):
        self.rc = REDIS
        self.new_items = []

    def process_item(self, item, spider):
        # store new_items for notifier
        if self.rc.exists(item['oid']):
            self.new_items.append(item)

        self.rc.hmset(
            item['oid'],
            {
                'url': item['url'],
                'title': item['title'],
                'img_url': item['img_url'],
                'query_url': item['query_url'],
            }
        )
        self.rc.rpush(f"{item['oid']}.seen_at", item['last_seen'])
        self.rc.rpush(f"{item['oid']}.price", item['price'])
        return item

    def close_spider(self, spider):
        notifier.deliver_now(self.new_items)
