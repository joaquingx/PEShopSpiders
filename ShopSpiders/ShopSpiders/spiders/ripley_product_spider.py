from scrapy.spiders import SitemapSpider


class RipleySpider(SitemapSpider):

    name = "ripley"
    sitemap_urls = ['https://home.ripley.com.pe/products_sitemap.xml']
    allowed_domains = ['simple.ripley.com.pe']
    
    def parse(self, response):

        def getValue(text,tag):
            return response.xpath('//*[contains(@class,"'+text+'")]/'+tag+'/text()').extract_first()

        brand = response.xpath('//td[contains(text(),"Marca")]/following-sibling::td/text()').extract_first()
        iPrice = getValue('product-internet-price','span[2]')
        nPrice = getValue('product-normal-price','span[2]')
        rPrice = getValue('product-ripley-price','span[2]')
        description = getValue('product-short-description','')
        discount = getValue('discount-percentage','')
        
        yield{
            'Code':  response.xpath('//*[contains(@itemprop,"sku")]/text()').extract_first(),
            'Brand': brand if brand else "Not found",
            'Description': description if description else "Not found",
            'Internet_Price': iPrice if iPrice else "Not found",
            'Normal_Price': nPrice if nPrice else "Not found",
            'Ripley_Price': rPrice if rPrice else "Not found",
            'Product_Name': getValue('product-header hidden-xs','h1'),
            'Url': response.url,
            'Discount': discount if discount else "Not found",
        }
