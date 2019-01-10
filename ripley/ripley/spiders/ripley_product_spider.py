from scrapy.spiders import SitemapSpider

class RipleySpider(SitemapSpider):

    name = "ripley"
    sitemap_urls = ['https://home.ripley.com.pe/products_sitemap.xml']
    allowed_domains = ['simple.ripley.com.pe']
    
    def parse(self, response):
        
        brand = response.xpath('//*[contains(@class,"brand-logo")]/span/text()').extract_first()        
        iPrice = response.xpath('//*[contains(@itemprop,"lowPrice")]/text()').extract_first()
        nPrice = response.xpath('//*[contains(@itemprop,"price")]/text()').extract()[0]
        
        yield{
            'Code':  response.xpath('//*[contains(@itemprop,"sku")]/text()').extract_first(),
            'Brand': brand if brand else "Not found",
            'Description': response.xpath('//*[contains(@class,"product-short-description")]/text()').extract_first(), #exception
            'Internet_Price': iPrice if iPrice else "Not found",
            'Normal_Price': nPrice if nPrice else "Not found",
            'Product_Name': response.xpath('//*[contains(@class,"product-header hidden-xs")]/h1/text()').extract_first(),
        }

#Description is not always given :c It has not been considered
