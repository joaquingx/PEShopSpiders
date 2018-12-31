# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.selector import HtmlXPathSelector


class PlazaveaSpider(scrapy.Spider):
    name = 'plazavea'
    allowed_domains = ['plazavea.com.pe']
    start_urls = ['http://plazavea.com.pe/sitemap-departments.xml']
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.xpath('//loc/text()').extract()
        for next_page_url in urls:
            if next_page_url:
                yield response.follow(url=next_page_url, callback=self.parseUrl)
    def parseUrl(self,response):
        URL =  response.xpath('//div[@class="vitrine resultItemsWrapper"]/script[@type="text/javascript"]').extract_first()
        if URL is not None:
            LoadProduct = re.findall(r"/buscapagina(.*?)'",URL)[0]
            LoadProduct = "http://www.plazavea.com.pe/buscapagina"+LoadProduct
            yield response.follow(url=LoadProduct+'50',callback=self.parseLoadProduct)
    def parseLoadProduct(self, response):
        products = response.xpath('//*[@class="g-inner-prod"]')
        number = response.url[response.url.find("Number=")+7:]
        Next_load = str(response.url[:-len(number)])+str(int(number)+1)
        if(len(products)):
            for product in products:
                normal_price = product.xpath('.//*[@class="g-block g-pnormal"]/span/text()').extract_first()
                discount_price =  product.xpath('.//*[@class="g-block g-pmejor"]/p[@itemprop="lowprice"]/text()').extract_first()
                name = product.xpath('.//*[@class="g-nombre-complete"]/text()').extract_first()
                image = product.xpath('.//*[@class="g-img-prod "]/figure/img/@src').extract_first()
                url = product.xpath('.//*[@class="g-img-prod "]/@href').extract_first()
                if discount_price is None:
                    discount_price = "No disponible"
                if normal_price is None:
                    normal_price = "No disponible"
                if image is None:
                    image = "No disponible"
                if url is None:
                    url = "No disponible"
                yield {'name':name,
                    'normal_price':normal_price,
                    'discount_price': discount_price,
                    'image': image,
                    'URL': url
                }
            yield response.follow(url=Next_load,callback=self.parseLoadProduct)