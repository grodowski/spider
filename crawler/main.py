import os
import requests
from scrapy.crawler import CrawlerProcess
from oto_dom_spider import OtoDomSpider

results_hook_url = os.getenv(
    'RESULTS_HOOK_URL',
    'http://localhost:3000/results', # dev
)

if __name__ == "__main__":
    output_csv = 'results.csv'
    process = CrawlerProcess({
        'FEED_FORMAT': 'csv',
        'FEED_URI': output_csv,
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })
    process.crawl(OtoDomSpider)
    process.start()
    try:
        response = requests.request(
            'POST',
            results_hook_url,
            files={'results': open(output_csv, 'rb')},
        )
        print('Status: ', response)
    except Exception as ex:
        print('Exception: ', ex)
