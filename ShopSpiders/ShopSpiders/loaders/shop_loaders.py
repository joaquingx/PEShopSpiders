from typing import Union

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Identity, Join, Compose
from w3lib.html import replace_entities, replace_tags
import re


def replace_decimals(value: str) -> str:
    try:
        f_value = float(re.search('\d+\.?\d*', value).group(0))
        return '%.2f' % f_value
    except (ValueError, AttributeError):  # if it's not float-value
        return value


def get_only_numbers(value: str) -> str:
    f_value = re.sub(r'[A-Za-z/ \s,]', '', value)
    return f_value


def replace_not_found(value: Union[str, float]) -> str:
    """If there's no value for field then replace it with Not Found"""
    if not value or float(value) == 0:
        return 'Not Found'
    else:
        return value


class GetCheaper(object):
    def __call__(self, values):
        mock_min_value = 1000000000000
        for value in values:
            if value != "Not Found":
                value_number = float(value)
                mock_min_value = min(mock_min_value, value_number)
        # not handle case when all prices are 'NOT FOUND'
        return replace_decimals(str(mock_min_value))


# Note: This loader function just receive ONE ITEM, seems that is not the usual way.
class AddHttp(object):
    def __call__(self, value):
        if not re.search('^(http|https)', value):
            return f'http://{value}'
        return value


class GetCurrency(object):
    def __call__(self, values):
        pen_currency = ['S/', 'PEN', 'SOL', 'NUEVO SOL']
        usd_currency = ['USD', '$', 'DOLLAR']
        for value in values:
            if value in pen_currency:
                return 'PEN'
            if value in usd_currency:
                return 'USD'
        return 'PEN'


class ShopItemLoader(ItemLoader):
    """Loader for every shop item."""
    url_out = img_url_out = Compose(
        lambda v: Join('')(v),
        lambda v: AddHttp()(v),
    )
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(
        replace_entities,  # Convert to unicode character when necessary
        replace_tags,  # Deletes html/xml tags
    )
    price_in = MapCompose(
        get_only_numbers,
        replace_decimals,
        replace_not_found,
    )
    stock_in = Identity()
    price_out = GetCheaper()
    currency_out = GetCurrency()
