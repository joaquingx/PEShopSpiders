# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote_plus
import json
from scrapy import Request

class FalabellaSpider(scrapy.Spider):
    name = 'falabella'
    allowed_domains = ['falabella.com.pe/falabella-pe']
    start_urls = ['http://falabella.com.pe/falabella-pe']

    def parse(self, response):
        # we are not interested in some anchors give us url to all categories
        categories = response.xpath(
            '//ul[@class="fb-masthead__grandchild-links"]/li/a[not(contains(text(),"Ver todo"))]/@href').extract()
        for categorie in categories[0:1]:
            categorie_url = response.urljoin(categorie)
            yield Request(categorie_url, callback=self.parse_categorie, dont_filter=True)

    def parse_categorie(self, response):
        
        if len(response.xpath('//head/link[@rel="next"]/@href').extract()):
            nav_state = response.url.replace(
                'https://www.falabella.com.pe/falabella-pe', '')
            url_tab = '{"currentPage":2,"navState":"%s"}' % nav_state
            url_encode = quote_plus(url_tab)
            url_url_final='https://www.falabella.com.pe/rest/model/falabella/rest/browse/BrowseActor/get-product-record-list?'+url_encode
            yield Request(url_url_final, callback=self.parse_categorie_json, meta={'categorie': nav_state}, dont_filter=True)

    def parse_categorie_json(self, response):
        self.logger.info ("MI URL"+response.url)
        json_response = json.loads(response.body.decode('utf-8'))
        nav_state = response.meta['categorie']



        if json_response['success']:
            json_response = json_response['state']
            for i in range(1, json_response['pagesTotal']+1):
                url_tab = '{"currentPage":%d,"navState":"%s"}' %(i, nav_state)
                url_encode = quote_plus(url_tab)
                url_url_final='https://www.falabella.com.pe/rest/model/falabella/rest/browse/BrowseActor/get-product-record-list?'+url_encode
                yield Request(url_url_final, callback=self.parse_categorie_item_list, meta={'categorie': nav_state,'page_number':i}, dont_filter=True)
        else:
            self.logger.info("HORROR EN URL  "+ response.url)

    def parse_categorie_item_list(self, response):
        json_response = json.loads(response.body.decode('utf-8'))
        
        if json_response['success']:
            json_response = json_response['state']
            for i in range(len(json_response['resultList'] ) ):
                print ("iterando item ",i)
                yield json_response['resultList'][i]
        else:
            print ("SUPER HORROR!!!!!",response.url,"pagina: ",response.meta['page_number'])