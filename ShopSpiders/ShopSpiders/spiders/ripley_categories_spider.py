from scrapy.spiders import SitemapSpider

class RipleySpider(SitemapSpider):

    name = "ripley_cat"
    sitemap_urls = ['https://home.ripley.com.pe/categories_sitemap.xml']
    allowed_domains = ['simple.ripley.com.pe']

    def parse(self, response):
        items = response.xpath('//*[@id="catalog-page"]/div/div[2]/div[3]/section/div/div/a')
        for item in items:
            brand = item.xpath('.//div[@class="brand-logo"]/span/text()').extract_first()
            name = item.xpath('.//div[@class="catalog-product-details__name"]/text()').extract_first()
            nPrice = item.xpath('.//li[@class="catalog-prices__list-price catalog-prices__lowest"]/text()').extract_first()
            iPrice = item.xpath('.//li[@class="catalog-prices__offer-price"]/text()').extract_first()
            discount = item.xpath('.//div[@class="catalog-product-details__discount-tag"]/text()').extract_first()
            yield{
                'Brand': brand if brand else "Not found",
                'Product_name': name,
                'Normal_price': nPrice if nPrice else "Not found",
                'Internet_price': iPrice if iPrice else "Not found",
                'Discount': discount if discount else "Not found",
            }
        mark = response.xpath('//*[@id="catalog-page"]/div/div[2]/div[4]/nav/ul/li[4]/a/@href').extract_first()
        if mark!='#':
            next_page = response.urljoin(mark)
            yield response.follow(next_page, callback=self.parse)
