# coding: utf8
import os
import schedule
import time
import redis

from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from otodom.oto_dom_spider import OtoDomSpider
from server.server import listen_and_serve

from constants import CRAWL_INTERVAL

def crawl():
    def _crawl_forked():
        process = CrawlerProcess({
            'ITEM_PIPELINES': {'otodom.importer_pipeline.ImporterPipeline': 0},
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        })
        process.crawl(OtoDomSpider)
        process.start()
    p = Process(target=_crawl_forked)
    p.start()
    p.join()

def start_web():
    def _http_server():
        print("Server ready 🌍")
        listen_and_serve()
    p = Process(target=_http_server)
    p.start()

if __name__ == "__main__":
    start_web()
    schedule.every(CRAWL_INTERVAL).minutes.do(crawl)
    print('Crawler ready 🚀')
    while True:
        schedule.run_pending()
        time.sleep(1)
