from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import replace_entities, replace_tags
import re


def replace_decimals(value: str) -> str:
    try:
        f_value = float(re.search('\d+\.?\d*', value).group(0))
        return '%.2f' % f_value
    except (ValueError, AttributeError):  # if it's not float-value
        return value


def replace_not_found(value) -> str:
    """If there's no value for field then replace it with Not Found"""
    if not value:
        return 'Not Found'
    else:
        return value


class ShopItemLoader(ItemLoader):
    """Loader for every shop item."""
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(
        replace_entities,  # Convert to unicode character when necessary
        replace_tags,  # Deletes html/xml tags
        replace_not_found,
    )
    regular_price_in = online_price_in = card_price_in = MapCompose(
        replace_decimals,
    )
