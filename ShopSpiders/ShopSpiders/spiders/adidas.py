# -*- coding: utf-8 -*-	
import scrapy	
import re	

from ShopSpiders.loaders.shop_loaders import ShopItemLoader	


class AdidasSpider(scrapy.Spider):	
    name = 'adidas'	
    allowed_domains = ['adidas.pe']	
    start_urls = ['https://m.adidas.pe/on/demandware.store/Sites-adidas-PE-Site/es_PE/Search-BrowseCatalog']	

    def parse(self, response):	
        adidas_items = response.xpath('//*[contains(@class, "innercard")]')	
        for adidas_item in adidas_items:	
            shop_loader = ShopItemLoader(item={}, selector=adidas_item)	
            shop_loader.add_value('regular_price', re.findall(r'\d+\.\d+|\d+', adidas_item.xpath(	
                './/*[@class="new-plp-layout-enabled"]/div/*[contains(@class, "salesprice")]/text()').extract_first())[0])	
            shop_loader.add_xpath('name', './/*[@class="title"]/text()')	
            shop_loader.add_xpath('url', './/*[@class="image plp-image-bg"]/a/@href')	
            shop_loader.add_xpath('img_url', './/*[@class="image plp-image-bg"]/a/@href')	
            item_width = adidas_item.xpath('.//*[@class="rating-stars rating-stars-filled"]/@style').extract_first()	
            item_stars = str(int(re.findall(r'\d+', item_width)[0]) / 20) if item_width else 'Not Ranked'	

            shop_loader.add_value('stars', item_stars)	

            item_stock = 'true' if response.xpath('.//*[@class="badge soldout"]/*[@class="badge-text"]/text()').extract_first() else 'false'	

            shop_loader.add_value('stock', item_stock)	

            yield shop_loader.load_item()	

        next_page_url = self.start_urls[0] + response.xpath(	
            '//*[contains(@class, "next-page pagging-cta")]/@href').extract_first()	
        if next_page_url:	
            yield response.follow(url=next_page_url, callback=self.parse)
