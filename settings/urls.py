class Urls:
    MAIN = "https://www.dns-shop.ru"
    API = "https://restapi.dns-shop.ru/v1/cart/"
    AUTHORIZATIONS = "https://www.dns-shop.ru/auth/auth/login-password-authorization/"
    LIST_ORDER = "https://restapi.dns-shop.ru/v1/profile-orders-get-list?page=&tab=all"
    ORDER = "https://www.dns-shop.ru/profile/order/all/"
    MICRODATA = "https://www.dns-shop.ru/product/microdata/"
    PRODUCT = "https://www.dns-shop.ru/product/"
    PROFILE = "https://restapi.dns-shop.ru/v1/get-menu-profile"
    CART = "https://www.dns-shop.ru/cart-service/get-data/"

    @classmethod
    def get_product(cls, product_id: str):
        return cls.PRODUCT + product_id

    @classmethod
    def get_microdata(cls, product_id: str):
        return cls.MICRODATA + product_id

    @classmethod
    def get_list_order(cls, page: int):
        return cls.LIST_ORDER.replace("page=", "page=" + str(page))
