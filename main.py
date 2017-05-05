# coding: utf8
import os
import schedule
import time
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from oto_dom_spider import OtoDomSpider

def crawl():
    def _crawl_forked():
        process = CrawlerProcess({
            'ITEM_PIPELINES': {'importer_pipeline.ImporterPipeline': 0},
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        })
        process.crawl(OtoDomSpider)
        process.start()
    p = Process(target=_crawl_forked)
    p.start()
    p.join()

if __name__ == "__main__":
    print('Crawler ready 🚀')
    schedule.every(int(os.getenv('CRAWL_INTERVAL'))).minutes.do(crawl)
    while True:
        schedule.run_pending()
        time.sleep(1)
