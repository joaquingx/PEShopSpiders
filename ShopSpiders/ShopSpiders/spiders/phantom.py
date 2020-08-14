from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
from loaders.shop_loaders import ShopItemLoader, get_only_numbers, replace_decimals, replace_not_found
from w3lib.html import replace_entities, replace_tags


def replace_comma(value: str) -> str:
    return value.replace(",", ".")


class PhantomLoader(ShopItemLoader):
    price_in = MapCompose(
        replace_entities,
        replace_tags,
        replace_comma,
        get_only_numbers,
        replace_decimals,
        replace_not_found,
    )


class PhantomSpider(CrawlSpider):
    name = "phantom"
    allowed_domains = [
        "phantom.pe"
    ]
    start_urls = [
        "https://phantom.pe/"
    ]

    rules = (
        Rule(LinkExtractor(restrict_css="a[class='em-menu-link']")),
        Rule(LinkExtractor(restrict_css="h2[class='product-name'] a"), callback="parse_item"),
        Rule(LinkExtractor(restrict_css="a[class='next i-next']"))
    )

    def parse_item(self, response):
        result = PhantomLoader(item={}, selector=response)
        stock = True if response.css("p[class='availability in-stock'] span::text").get() == "En existencia" else False
        result.add_css("price", "div[class='product-view-detail'] span[class='price']::text")
        result.add_css("name", "div[class='product-name'] h1")
        result.add_value("stock", stock)
        result.add_css("img_url", "p[class='product-image'] a[id='image_zoom'] img::attr(src)")
        result.add_value("url", response.url)
        result.add_css("currency", "div[class='product-view-detail'] span[id*='product-price']")
        return result.load_item()
