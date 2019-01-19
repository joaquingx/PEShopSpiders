# -*- coding: utf-8 -*-
import scrapy


class TottusSpiderSpider(scrapy.Spider):
    name = 'tottus_spider'
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
            out_stock = True if item.xpath(
                '//*[contains(@class,"out-of-stock")]') else 0
            url = response.urljoin(item.xpath(
                './/a[@href!=""]/@href').extract_first())
            title = item.xpath(
                './/div[@class="title"]//h5/div/text()').extract_first().replace('\n', '')
            title = title.replace(' ', '')
            brand = item.xpath(
                './/div[@class="title"]//h5/span/text()').extract_first()
            characteristics = item.xpath(
                './/*[@class="statement"]/text()').extract_first()
            price = item.xpath(
                './/*[@class="prices"]/span[@class="nule-price"]/text()').extract_first()
            if price == None:
                price = item.xpath(
                    './/*[@class="prices"]/span[@class="active-price"]/span/text()').extract_first()
            if price:
                price = price.replace('\n', '')
                price = price.replace(' ', '')

            price_red = item.xpath(
                './/*[@class="prices"]/span[@class="red"]/text()').extract_first()
            if price_red == None:
                price_red = item.xpath(
                    './/*[@class="prices"]/span[@class="active-price"]/span[@class="red"]/text()').extract_first()
            if price_red:
                price_red = price_red.replace('\n', '')
                price_red = price_red.replace(' ', '')

            offer = item.xpath(
                './/*[@class="active-offer"]/span/text()').extract_first()

            yield{
                'out_stock': out_stock,
                'url': url,
                'title': title,
                'brand': brand,
                'characteristics': characteristics,
                'price': price,
                'price_red': price_red,
                'offer': offer,
            }
        next_url = response.xpath('//a[@id="next"]/@href').extract_first()
        absolute_next_page = response.urljoin(next_url)
        self.logger.info("===> NEXT_PAGE: "+absolute_next_page)
        yield response.follow(absolute_next_page, callback=self.parse_category_items)
