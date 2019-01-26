from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import replace_entities, replace_tags, strip_html5_whitespace


def replace_decimals(value: str) -> str:
    try:
        f_value = float(value)
        return '%.2f' % f_value
    except ValueError:  # if it's not float-value
        return f_value


class ShopItemLoader(ItemLoader):
    """Loader for every shop item."""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(
        replace_entities,  # Convert to unicode character when necessary
        replace_tags,  # Deletes html/xml tags
    )
    regular_price_in = online_price_in = card_price_in = MapCompose(
        replace_decimals,
    )
