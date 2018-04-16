# coding: utf8
from scrapy.crawler import CrawlerProcess
from otodom.oto_dom_spider import OtoDomSpider

if __name__ == "__main__":
    process = CrawlerProcess({
        'ITEM_PIPELINES': {'otodom.importer_pipeline.ImporterPipeline': 0},
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64, x64; Trident/7.0; rv:11.0) like Gecko)',
    })
    process.crawl(OtoDomSpider)
    print("Crawler ready 🚚")
    process.start()
