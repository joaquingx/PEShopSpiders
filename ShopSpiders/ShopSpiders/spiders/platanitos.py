from scrapy.spiders import Spider
from loaders.shop_loaders import ShopItemLoader


class PlatanitosSpider(Spider):
    start_urls = ["https://platanitos.com/catalogo"]
    allowed_domains = [
        "platanitos.com",
    ]
    name = "platanitos"

    def parse(self, response):
        item_selector_list = response.css("div[id='catalogo-box2'] a[class='items']")
        for item_selector in item_selector_list:
            result = ShopItemLoader(item={}, selector=item_selector)
            href = item_selector.css('a::attr(href)').get()
            img_url = item_selector.css("img[src*='mister']::attr(src)").get()
            name = item_selector.css("div[id='product_brand']").get()
            name = ''.join([name, item_selector.css("div[id='product_model']").get()])
            result.add_css("price", "span[class='price']")
            result.add_value("name", name)
            result.add_value("url", response.urljoin(href))
            result.add_value("img_url", img_url.replace("160x240", "1500x1500"))
            result.add_css("currency", "span[class='price']")
            result.add_value("referer", response.url)
            yield result.load_item()

        next_url = response.css('div[class="pagination-box2"] a::attr(href)')[-1]
        if "sin-resultados" not in next_url.get():
            yield response.follow(next_url)
