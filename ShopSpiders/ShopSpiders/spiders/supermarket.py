# -*- coding: utf-8 -*-
import json

from scrapy.spiders import SitemapSpider
from scrapy import Request
from inline_requests import inline_requests


class SuperMarketBase(SitemapSpider):
    sitemap_rules = [
        ('/p', 'parse_item'),  # Parse products(/p) with parse_item
    ]
    sitemap_follow = ['sitemap-products.*']  # Go for all products without specific order/category
    card_url = None  # Check existence of Credit Card Offer(OH!)

    @inline_requests
    def parse_item(self, response):
        def get_price(name_class):
            return response.css(f'.{name_class}::text').re_first('\d+\.\d+')

        def is_available():
            qty = response.css('script').re_first('"skuStocks"\:\{.*?\:(\d+)\}')
            return int(qty) if qty else False

        card_price = 'Not Found'
        if self.card_url:    # It's possible to exist offers
            sku_id = response.css('#___rc-p-sku-ids::attr(value)').get()
            assert sku_id, "sku_id not found"

            url = self.card_url.format(sku_id)
            card_response = yield Request(url)
            card_dict = json.loads(card_response.text)
            if card_dict:
                try:
                    card_price = \
                        card_dict[0]['items'][0]['sellers'][0]['commertialOffer']['Teasers'][0][
                            '<Effects>k__BackingField'][
                            '<Parameters>k__BackingField'][0]['<Value>k__BackingField']
                    if '.' in card_price:    # If obtains a discount instead final price
                        card_price = float(get_price('skuBestPrice')) * (1-(float(card_price)/100))    # TODO: This could be buggy
                    else:
                        card_price = card_price[:-2] + ".00"
                except (KeyError, IndexError) as e:
                    card_price = 'Not Found'

        result = {
            'regular_price': get_price('skuListPrice'),
            'online_price': get_price('skuBestPrice') if get_price('skuBestPrice') else 'Not Found',
            'card_price': card_price,
            'description': response.css('.productDescription').xpath('string()').get(),
            'name': response.css('.productName::text').get(),
            'img_url': response.css(".image-zoom::attr(href)").get(),
            'url': response.url,
            'stock': True if is_available() else False,
            'stars': '0',  # Apparently stars doesn't work for now
        }
        yield result


class MetroSpider(SuperMarketBase):
    name = 'metro'
    sitemap_urls = [
        'https://www.metro.pe/sitemap.xml'
    ]
    allowed_domains = ['www.metro.pe']


class WongSpider(SuperMarketBase):
    name = 'wong'
    sitemap_urls = [
        'https://www.wong.pe/sitemap.xml'
    ]
    allowed_domains = ['www.wong.pe']


class OechsleSpider(SuperMarketBase):
    name = 'oechsle'
    sitemap_urls = [
        'https://www.oechsle.pe/sitemap.xml'
    ]
    allowed_domains = ['oechsle.pe']

    card_url = 'https://www.oechsle.pe/api/catalog_system/pub/products/search/?fq=productId:{}'


class PlazaVeaSpider(SuperMarketBase):
    name = 'plaza_vea'
    sitemap_urls = [
        'https://www.plazavea.com.pe/sitemap.xml'
    ]
    allowed_domains = [
        'plazavea.com.pe',
        'tienda.plazavea.com.pe'
    ]

    card_url = 'https://tienda.plazavea.com.pe/api/catalog_system/pub/products/search?fq=skuId:{}'
