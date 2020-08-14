# -*- coding: utf-8 -*-
from spiders.base.base_spiders import CustomSiteMapSpider
from loaders.shop_loaders import ShopItemLoader


class LinioSpider(CustomSiteMapSpider):
    sitemap_rules = [
        ('/p', 'parse_item'),
    ]
    sitemap_follow = ["sitemap.*"]
    sitemap_urls = [
        'http://sitemap.linio.com/pe/sitemap.xml'
    ]
    name = 'linio'
    allowed_domains = [
        'linio.com.pe',
        'sitemap.linio.com',
    ]

    def parse_item(self, response):
        css_path = "meta[{key}='{value}']::attr({content})"
        result = ShopItemLoader(item={}, selector=response)
        result.add_css('price', 'span[class="original-price"]::text')
        result.add_css('price', 'span[class="price-main-md"]::text')
        result.add_css('price', 'span[class="price-promotional"]::text')
        result.add_css('name', css_path.format(key="itemprop", value="name", content="content"))
        result.add_css('currency', css_path.format(key="itemprop", value="priceCurrency", content="content"))
        result.add_css('description', css_path.format(key="name", value="Description", content="content"))
        result.add_css('img_url', css_path.format(key="property", value="og:image", content="content"))
        result.add_value('url', response.url)
        yield result.load_item()
