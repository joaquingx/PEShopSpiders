# -*- coding: utf-8 -*-
import scrapy
import re


class AdidasSpider(scrapy.Spider):
    name = 'adidas'
    allowed_domains = ['adidas.pe']
    start_urls = ['https://m.adidas.pe/on/demandware.store/Sites-adidas-PE-Site/es_PE/Search-BrowseCatalog']
    def parse(self, response):
        adidas_items = response.xpath('//*[contains(@class, "innercard")]')
        for adidas_item in adidas_items:
            item_name = adidas_item.xpath('.//*[@class="title"]/text()').extract_first()
            item_price = re.findall(r'\d+\.\d+|\d+',adidas_item.xpath('.//*[@class="new-plp-layout-enabled"]/div/*[contains(@class, "salesprice")]/text()').extract_first())[0]
            item_image = adidas_item.xpath('.//*[@class="show lazyload"]/@data-original').extract_first()
            item_url = adidas_item.xpath('.//*[@class="image plp-image-bg"]/a/@href').extract_first()
            item_width = adidas_item.xpath('.//*[@class="rating-stars rating-stars-filled"]/@style').extract_first()
 
            if item_width is None:
                item_stars = 'Not Ranked'
            else:
                item_stars = int(re.findall(r'\d+', item_width)[0])/20
            
            item_stock = adidas_item.xpath('.//*[@class="badge soldout"]/*[@class="badge-text"]/text()').extract_first()

            if item_stock is None:
                stock = 'Yes'
            else:
                stock = 'No'

            yield{  'Name' : item_name,
                    'Prices' : item_price,
                    'Image' : item_image,
                    'URL' : item_url,
                    'Stars' : item_stars,
                    'Stock' : stock,
                  }
        next_page_url = self.start_urls[0] + response.xpath('//*[contains(@class, "next-page pagging-cta")]/@href').extract_first()
        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse)
