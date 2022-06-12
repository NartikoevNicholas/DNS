class Product:
    name: str
    old_price: int or str
    new_price: int or str
    price_difference: int or str
    color: str
    date: str
    warranty_expire_date: str
    url: str
    count: str or int
    image: bytes

    def __init__(self, name="Неопределено", old_price="-", new_price="-", count=1, url="-", date="-", warranty_expire_date="-", image=None):
        self.name = name
        self.old_price = old_price
        self.new_price = new_price
        self.count = count
        self.url = url
        self.date = date
        self.warranty_expire_date = warranty_expire_date
        self.get_price_difference()
        self.image = image

    def get_price_difference(self):
        if type(self.new_price) == int and type(self.old_price) == int:
            temp = self.new_price - self.old_price
            if temp < 0:
                self.color = "red"
            elif temp == 0:
                self.color = "black"
            else:
                self.color = "green"
            self.price_difference = abs(temp)
        else:
            self.color = "black"
            self.price_difference = "-"
