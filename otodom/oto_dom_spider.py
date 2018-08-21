# coding: utf8
import scrapy
import os
import re
from datetime import datetime

from constants import TIME_FORMAT

class OtoDomSpider(scrapy.Spider):
    name = 'otodom'
    start_urls = os.getenv('CRAWL_OTODOM_URL').split(',')
    img_url_re = '(https:\/\/.+)\)$'

    print(f"Spider crawling: {start_urls}")
    last_seen = datetime.now().strftime(TIME_FORMAT)

    def parse(self, response):
        for offer in response.css('article.offer-item'):
            oid = offer.css('::attr(data-item-id)').extract_first()
            offer_url = offer.css('::attr(data-url)').extract_first()
            title = offer.css('.offer-item-header .offer-item-title::text') \
                         .extract_first()
            price = offer.css('.offer-item-price::text') \
                         .extract_first()
            img_cover_style = offer.css('.img-cover::attr(style)') \
                                   .extract_first()
            img_url = re.findall(self.img_url_re, img_cover_style)[0]
            price_i = re.sub('\D+', '', price)
            yield {
                'oid': oid,
                'url': offer_url,
                'title': title,
                'img_url': img_url,
                'price': price_i,
                'query_url': response.url,
                'last_seen': self.last_seen,
            }
        next_page = response.css('ul.pager a[data-dir="next"]::attr(href)') \
                            .extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
