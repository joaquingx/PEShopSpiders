from spiders.base.base_spiders import CustomSiteMapSpider
from loaders.shop_loaders import ShopItemLoader


class XiaomiSpider(CustomSiteMapSpider):
    sitemap_urls = [
        "https://xiaomiperu.pe/product-sitemap.xml",
    ]
    name = "xiaomi"
    sitemap_rules = [
        ('/producto', 'parse_item'),
    ]
    allowed_domains = [
        "xiaomiperu.pe",
    ]

    def parse_item(self, response):
        css_path = "meta[{key}='{value}']::attr({content})"
        result = ShopItemLoader(item={}, selector=response)
        result.add_css("price", "p[class='price'] span[class='woocommerce-Price-amount amount']::text")
        result.add_css("currency", "span[class='woocommerce-Price-currencySymbol']")
        result.add_css("description", css_path.format(key="property", value="og:description", content="content"))
        result.add_css("img_url", css_path.format(key="property", value="og:image", content="content"))
        result.add_css("name", "h1[itemprop='name']::text")
        result.add_value("url", response.url)
        yield result.load_item()
