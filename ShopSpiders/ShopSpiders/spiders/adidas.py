# -*- coding: utf-8 -*-
import scrapy
import re


class AdidasSpider(scrapy.Spider):
    adidas_products = ["calzado-hombre","ropa-hombre","accesorios-hombre","performance-hombre"
    ,"calzado-mujer","ropa-mujer","accesorios-mujer","performance-mujer"
    ,"ninos?prefn1=age&prefv1=8-16%20A%C3%B1os&srule=newest-to-oldest"
    ,"ninos?prefn1=age&prefv1=4-8%20A%C3%B1os"
    ,"bebe-ninos"
    ,"performance-ninos"]
    name = 'adidas'
    allowed_domains = ['adidas.pe']
    start_urls = ['https://adidas.pe/{}'.format(i) for i in adidas_products]
    def parse(self, response):
        adidas_items = response.xpath('//div[@class="hockeycard originals " or @class="hockeycard performance "]')
        print(len(adidas_items))
        for adidas_item in adidas_items:
            item_name = adidas_item.xpath('.//*[@class="title"]/text()').extract()
            item_price = re.findall(r'\d+', adidas_item.xpath('.//*[contains(@class, "salesprice")]/text()').extract_first())[0]   
            item_image = adidas_item.xpath('.//*[@class="show lazyload"]/@data-original').extract_first()
            item_url = adidas_item.xpath('.//*[@class="image plp-image-bg"]/a/@href').extract_first()
            item_star = adidas_item.xpath('.//*[@class="rating-stars rating-stars-filled"]/@style').extract_first()
            # item_star = int(re.findall(r'\d+',adidas_item.xpath('.//*[@class="rating-stars rating-stars-filled"]/@style').extract_first())[0])    
            yield{  'Name' : item_name,
                    'Prices' : item_price,
                    'Image' : item_image,
                    'URL' : "adidas.pe"+item_url,
                    'Stars' : item_star
                  }
        next_page_url = response.xpath('//*[@class="paging-arrow pagging-next-page"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url)
