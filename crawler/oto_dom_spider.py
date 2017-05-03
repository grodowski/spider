import scrapy
import re

class OtoDomSpider(scrapy.Spider):
    name = 'otodom'
    # TODO: build a way to customize the url query :) env var?
    start_urls = [('https://www.otodom.pl/wynajem/mieszkanie/warszawa/?search'
                   '%5Bfilter_float_price%3Ato%5D=2500&search%5Bfilter_float_'
                   'm%3Afrom%5D=40&search%5Bfilter_float_m%3Ato%5D=60&search%'
                   '5Bdescription%5D=1&search%5Bdist%5D=0&search%5Bdistrict_i'
                   'd%5D=39')]
    img_url_re = '(https:\/\/.+)\)$'

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
            }
        next_page = response.css('ul.pager a[data-dir="next"]::attr(href)') \
                            .extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
