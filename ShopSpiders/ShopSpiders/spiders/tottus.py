# -*- coding: utf-8 -*-
import scrapy
from ShopSpiders.loaders.shop_loaders import ShopItemLoader
import re

class TottusSpider(scrapy.Spider):
    name = 'tottus'
    allowed_domains = ['www.tottus.com.pe']
    start_urls = ['http://www.tottus.com.pe/tottus/home/']

    def parse(self, response):
        categories = response.xpath(
            '//*[@class="nav navbar-nav navbar-categories"]//a[not(@href="#")]/@href').extract()
        assert categories, "Categories not found"
        url = 'http://www.tottus.com.pe/tottus/productListFragment'
        for category in categories:
            categorie_url = category.replace('/tottus/browse', '')
            yield response.follow(url+categorie_url, callback=self.parse_category_items)

    def parse_category_items(self, response):
        items = response.xpath('//*[contains(@class," item-product-caption")]')
        for item in items:
            shop_loader = ShopItemLoader(item={}, selector=items)
            price = item.xpath('//*[@class="prices"]/span[@class="active-price"]/span/text()').extract_first()
            shop_loader.add_value('regular_price',re.findall(r'(\d+\.\d+)',price)[0] )
            shop_loader.add_xpath('name', '//div[@class="title"]//h5/div-1.0/text()')
            shop_loader.add_value(
                'stock',"true" if item.xpath(
                '//*[contains(@class,"out-of-stock")]') else "false"
            )
            shop_loader.add_xpath('img_url', '//span[@class="thumbnail"]/img/@src')
            shop_loader.add_xpath('url', '//div[@class="title"]/a/@href')
            shop_loader.add_value('stars', 'Not Found')
            price_red = item.xpath(
                './/*[@class="prices"]/span[@class="red"]/text()').extract_first()
            if price_red == None:
                price_red = item.xpath(
                    './/*[@class="prices"]/span[@class="active-price"]/span[@class="red"]/text()').extract_first()
            shop_loader.add_value('online_price',  re.findall(r'\d+\.\d+|\d+',price_red) if price_red else 0.00)
            offer = item.xpath('.//*[@class="active-offer"]/span/text()').extract_first()
            shop_loader.add_value('card_price', re.findall(r'\d+\.\d+|\d+',offer) if offer else 0.00)
            yield shop_loader.load_item()
        next_url = response.xpath('//a[@id="next"]/@href').extract_first()
        absolute_next_page = response.urljoin(next_url)
        yield response.follow(absolute_next_page, callback=self.parse_category_items)
