# -*- coding: utf-8 -*-
import json

from scrapy.spiders import SitemapSpider
from scrapy import Request
from inline_requests import inline_requests
from ShopSpiders.loaders.shop_loaders import ShopItemLoader


# TODO: Handle completely card_price
class SuperMarketBase(SitemapSpider):
    sitemap_rules = [
        ('/p', 'parse_item'),  # Parse products(/p) with parse_item
    ]
    sitemap_follow = ['sitemap-products.*']  # Go for all products without specific order/category
    card_url = None  # Check existence of Credit Card Offer(OH!)

    @inline_requests
    def parse_item(self, response):
        card_price = 'Not Found'
        if self.card_url:  # It's possible to exist offers
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
                    card_price = card_price[:-2] + ".00"
                except (KeyError, IndexError) as e:
                    card_price = 'Not Found'

        css_st = '.{}::text'
        result = ShopItemLoader(item={}, selector=response)
        result.add_css('regular_price', css_st.format('skuListPrice'))
        result.add_css('online_price', css_st.format('skuBestPrice'))
        result.add_value('card_price', card_price)
        result.add_css('description', '.productDescription')
        result.add_css('name', '.productName::text')
        result.add_css('img_url', '.image-zoom::attr(href)')
        result.add_value('url', response.url)
        result.add_css('stock', 'script', re='"skuStocks"\:\{.*?\:(\d+)\}')
        result.add_value('stars', '0')  # Apparently stars doesn't work for now

        yield result.load_item()


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
