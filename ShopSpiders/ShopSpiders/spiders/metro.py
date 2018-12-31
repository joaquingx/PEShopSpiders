# -*- coding: utf-8 -*-
from scrapy.spiders import SitemapSpider


class SuperMarketBase(SitemapSpider):
    sitemap_rules = [
        ('/p', 'parse_item'),  # Parse products(/p) with parse_item
    ]
    sitemap_follow = ['sitemap-products.*']  # Go for all products without specific order/category

    def parse_item(self, response):
        def get_price(name_class):
            return response.css(f'.{name_class}::text').re_first('\d+\.\d+')

        def is_available():
            qty = response.css('script').re_first('"skuStocks"\:\{.*?\:(\d+)\}')
            return int(qty) if qty else False

        result = {
            'regular_price': get_price('skuListPrice'),
            'online_price': get_price('skuBestPrice') if get_price('skuBestPrice') else 'Not Found',
            'description': response.css('.productDescription').xpath('string()').get(),
            'name': response.css('.productName::text').get(),
            'url': response.url,
            'stock': True if is_available() else False,
            'stars': '0',  # I don't found any product with stars
        }
        return result


class MetroSpider(SuperMarketBase):
    name = 'metro'
    sitemap_urls = [
        'https://www.metro.pe/sitemap.xml'
    ]
    allowed_domains = ['www.metro.pe']


class PlazaVeaSpider(SuperMarketBase):
    name = 'plaza_vea'
    sitemap_urls = [
        'https://www.plazavea.com.pe/sitemap.xml'
    ]
    allowed_domains = ['www.plazavea.com.pe']


class WongSpider(SuperMarketBase):
    name = 'wong'
    sitemap_urls = [
        'https://www.wong.pe/sitemap.xml'
    ]
    allowed_domains = ['www.wong.pe']
