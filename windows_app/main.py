from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tkinter import messagebox as mb
from dns_api import get_list_orders, get_list_cart
from models import user_agent, proxy
from windows_app.authorization import Authorization
from widget.group_box import GroupBox


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()

        self.setMinimumSize(700, 500)
        self.setWindowTitle("My DNS")

        # ScrollArea
        self.scroll_area = QScrollArea()
        self.v_box = QVBoxLayout()

        # Create user agent
        self.UA = user_agent.UserAgent()
        self.proxy = proxy.Proxy()

        # Actions
        self.authorization_action = QAction(self)
        self.proxy_action = QAction(self)
        self.user_agent_action = QAction(self)
        self.show_order = QAction(self)
        self.cart = QAction(self)
        self.button_application = QAction(self)

        # Authorization window
        self.authorization_window = Authorization(self, 300, 200)

        # About app window

        # initialize_method
        self._create_actions()
        self._initialize_element()

        # dict orders user
        self.list_GroupBox = []

    def _initialize_element(self):

        # Menu bar
        self.menuBar().addAction(self.authorization_action)
        tools = self.menuBar().addMenu("Инструменты")
        tools.addAction(self.proxy_action)
        tools.addAction(self.user_agent_action)

        dns = self.menuBar().addMenu("DNS")
        dns.addAction(self.show_order)
        dns.addAction(self.cart)

        self.menuBar().addAction(self.button_application)

        # Status bar
        self.statusBar().setFixedHeight(15)
        self.statusBar().showMessage("ready")

        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.central_widget)

        self.central_widget.setLayout(self.v_box)
        self.setCentralWidget(self.scroll_area)

    def _create_actions(self):
        self.authorization_action.setText("Авторизация")
        self.authorization_action.triggered.connect(self.authorization_window.show_window)

        self.proxy_action.setText("Обновить список прокси")
        self.proxy_action.triggered.connect(self.update_proxy)

        self.user_agent_action.setText("Обновить список юзер агентов")
        self.user_agent_action.triggered.connect(self.update_ua)

        self.show_order.setText("Получить список моих заказов")
        self.show_order.triggered.connect(self.order_dns)

        self.cart.setText("Корзина")
        self.cart.triggered.connect(self.cart_dns)

        self.button_application.setText("о программе")
        self.button_application.triggered.connect(self.about_application)

    def update_ua(self):
        self.statusBar().showMessage('Обновление списка "User agent", подождите.')
        self.statusBar().repaint()
        self.UA.parse()
        self.statusBar().showMessage('Обновление завершено!')

    def update_proxy(self):
        self.statusBar().showMessage('Обновление списка прокси, подождите.')
        self.statusBar().repaint()
        self.proxy.parse()
        self.statusBar().showMessage('Обновление завершено!')

    def action_dns(self, check: str):
        if self.authorization_window.response is None or len(self.authorization_window.response.json()['errors']) > 0:
            mb.showerror("Ошибка",
                         "Вы не авторизованны!")
        else:
            self.statusBar().showMessage('Сбор информации, подождите.')
            self.statusBar().repaint()

            for el in self.list_GroupBox:
                self.v_box.removeWidget(el)
                el.deleteLater()

            self.list_GroupBox = []
            if check == "ORDER":
                list_orders = get_list_orders(self.authorization_window.cookies, self.authorization_window.headers)
                for product in list_orders:
                    data = {"Цена покупки:": product.old_price,
                            "Актуальная цена:": product.new_price,
                            "Разница в цене:": product.price_difference,
                            "Количество:": product.count,
                            "Дата покупки:": product.date,
                            "Дата окончании гарантии:": product.warranty_expire_date,
                            "URL:": f"<a href='{product.url}'>{product.url}</a>"}
                    group_box = GroupBox(self, product.name, data, [2], product.color, image=product.image)
                    self.v_box.addWidget(group_box)
                    self.list_GroupBox.append(group_box)
            elif check == "CART":
                list_orders = get_list_cart(self.authorization_window.cookies, self.authorization_window.headers)
                for product in list_orders:
                    data = {"Цена:": product.new_price,
                            "Дата добавления в корзину:": product.date,
                            "Количество:": product.count,
                            "URL:": f"<a href='{product.url}'>{product.url}</a>"}
                    group_box = GroupBox(self, product.name, data, image=product.image)
                    self.v_box.addWidget(group_box)
                    self.list_GroupBox.append(group_box)

            self.statusBar().showMessage('Сбор информации завершен.')

    def order_dns(self):
        self.action_dns(check="ORDER")

    def cart_dns(self):
        self.action_dns(check="CART")

    def about_application(self):
        pass
