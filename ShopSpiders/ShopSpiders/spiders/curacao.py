from spiders.base.base_spiders import CustomSiteMapSpider
from loaders.shop_loaders import ShopItemLoader


class CuracaoSpider(CustomSiteMapSpider):
    sitemap_urls = [
        "https://www.lacuracao.pe/sitemap.xml",
    ]
    sitemap_rules = [
        (r"-p$", "parse_item")
    ]
    name = "curacao"

    def parse_item(self, response):
        result = ShopItemLoader(item={}, selector=response)
        error = response.css("div[id='errorPage']")
        if not error:
            img_url = response.urljoin(response.css("img[id='productMainImage']::attr(src)").get())
            stock = True if response.css("p[class='subtitle-despacho']::text").get() == 'Disponible' else False
            result.add_css("price", "div[id*='productSlot'] span[id='offerPriceValue']::text")
            result.add_css("price", "div[id*='productSlot'] span[id='old_price']::text")
            result.add_css("price", "div[id*='productSlot'] span[class='price']::text")
            result.add_css("name", "h1[class='main_header']")
            result.add_value("stock", stock)
            result.add_value("img_url", img_url)
            result.add_value("url", response.url)
            result.add_css("currency", "span[id='offerPriceValue']")
            result.add_css("currency", "span[id='old_price']")
            result.add_css("currency", "span[class='price']")
            return result.load_item()
