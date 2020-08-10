from typing import List


def exist_exact_item_in_product_list_object(product_list: List[dict], product_to_evaluate: dict):
    try:
        return True if [ product for product in product_list if
                        product_to_evaluate['spider'] == product['provider']] else False
    except:
        return False


def exist_item_in_different_date(product_list: List[dict], product_to_evaluate: dict):
    try:
        return True if [product for product in product_list if product_to_evaluate['name'] == product['real_name']
                    and product_to_evaluate['price'] != product['prices'][-1]['price']
                    and product_to_evaluate['spider'] == product['provider']
                    and product_to_evaluate['url'] == product["url"]] else False
    except:
        return False


def create_new_product_object(product: dict):
    try:
        return {
            'provider': product['spider'],
            "real_name": product['name'],
            'url': product['url'],
            'location': {
                "lat": "",
                "lng": "",
            },
            'prices': [{
                'price': product['price'],
                'date': product['timestamp'],
            }],
        }
    except KeyError as e:
        return {
            'provider': product.get('spider'),
            "real_name": product.get('name'),
            'url': product.get('url'),
            'location': {
                "lat": "",
                "lng": "",
            },
            'prices': [{
                'price': product.get('price'),
                'date': product.get('timestamp'),
            }],
        }


def add_price_to_product_object(product_list_object: List[dict], product_to_add: dict):
    for product in product_list_object:
        if product['provider'] == product_to_add['spider']:
            product['prices'].append({
                "price": product_to_add['price'],
                "date": product_to_add['timestamp'],
            })
            break


def get_product_objects(product_list: List[dict]) -> dict:  #TODO: sort by price.
    product_list_object = []
    product_list = sorted(product_list, key=(lambda x: x['timestamp']))
    for product in product_list:
        if not exist_exact_item_in_product_list_object(product_list_object, product):
            product_list_object.append(create_new_product_object(product))
        elif exist_item_in_different_date(product_list_object, product):
            add_price_to_product_object(product_list_object, product)
    if len(product_list) > 0:
        return {
            "id": str(product_list[0]['_id']), # TODO: puede ser que necesito cambiarlo
            "name": product_list[0]['name'],
            "imgUrl": product_list[0]['img_url'],
            "description": "",
            'providersSimple': product_list_object,
        }
