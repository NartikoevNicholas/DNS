import http.client
import requests
from models.products import Product
from settings.urls import Urls

http.client._MAXHEADERS = 1000


def get_list_cart(cookies, headers):
    list_orders = []
    response = requests.get(Urls.CART, cookies=cookies, headers=headers).json()
    for product in response:
        info = response[product]["products"][0]
        list_orders.append(Product(
            name=info["name"],
            old_price="-",
            new_price=info["price"],
            url=Urls.get_product(info['productUrl'].replace("/product/", "")),
            count=info["count"],
            image=load_img(info['imageUrl'])
        ))
    return list_orders


def get_list_orders(cookies, headers):
    list_product = []
    i = 1
    while True:
        try:
            url = Urls.get_list_order(i)
            response = requests.get(url, cookies=cookies, headers=headers)
            count_orders = response.json()["data"]["groups"]["Личные заказы"]
            for orders in count_orders:
                for product in orders["products"]:
                    new_price: int or str
                    try:
                        new_price = \
                            requests.get(Urls.get_microdata(product['id']), cookies=cookies, headers=headers).json()[
                                "data"]["offers"]["price"]
                    except:
                        new_price = "Нет в продаже"
                    list_product.append(Product(product['title'],
                                                product["price"],
                                                new_price,
                                                product["count"],
                                                Urls.get_product(product["searchUid"]),
                                                orders["date"].replace("T", " ") if orders["date"] is not None else "",
                                                product['warrantyExpireDate'].replace("T", " ") if product[
                                                                                                       'warrantyExpireDate'] is not None else "",
                                                load_img(product['urlImg'])
                                                ))
                    load_img(product['urlImg'])
            i += 1
        except Exception as ex:
            return list_product


def get_user_name(cookies, headers):
    response = requests.get(Urls.PROFILE, cookies=cookies, headers=headers).json()['data']["username"]
    return response


def load_img(url):
    image = requests.get(url)
    return image.content
