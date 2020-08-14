import json

from spiders.base.base_spiders import CustomSiteMapSpider
from loaders.shop_loaders import ShopItemLoader


class RipleySpider(CustomSiteMapSpider):

    name = "ripley"
    sitemap_urls = ['https://home.ripley.com.pe/products_sitemap.xml']
    allowed_domains = ['simple.ripley.com.pe']

    def parse(self, response):

        def get_value(text, tag):
            return f'//*[contains(@class,"{text}")]/{tag}/text()'

        loader = ShopItemLoader(item={}, selector=response)

        loader.add_xpath('price', get_value('product-internet-price', 'span[2]'))
        loader.add_xpath('price',  get_value('product-normal-price', 'span[2]'))
        loader.add_xpath('price', get_value('product-ripley-price', 'span[2]'))
        loader.add_xpath('brand', '//td[contains(text(),"Marca")]/following-sibling::td/text()')
        loader.add_xpath('description', get_value('product-short-description', ''))
        loader.add_xpath('name', get_value('product-header hidden-xs', 'h1'))
        loader.add_xpath('img_url', '//meta[contains(@property, "og:image")]/@content', re="(home.*|http.*)")
        loader.add_value('url', response.url)
        currency_dictionary = response.xpath("//script[contains(@type, 'application/ld+json')]/text()").extract_first()
        loader.add_value('currency', json.loads(currency_dictionary)['offers']['priceCurrency'])

        yield loader.load_item()
