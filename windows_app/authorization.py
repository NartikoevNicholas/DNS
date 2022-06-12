from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from requests.utils import dict_from_cookiejar
from urllib.parse import unquote
from parse import *
from dns_api import get_user_name


class Authorization(QMainWindow):
    def __init__(self, main_window, x, y):
        super().__init__()
        self.main_window = main_window
        self.setMinimumSize(x, y)
        self.setMaximumSize(x, y)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowTitle("Авторизация")

        # user name elements
        self.label_login = QLabel(self)
        self.text_line_login = QLineEdit(self)

        # password elements
        self.label_password = QLabel(self)
        self.text_line_password = QLineEdit(self)

        # sing in button
        self.button = QPushButton(self)

        # remember check
        self.label_check = QLabel(self)
        self.check_remember = QCheckBox(self)

        # message about authorization

        self.message = QLabel(self)

        self.data = None
        self.cookies = None
        self.headers = None
        self.response = None

        self.__initialize_element()

    def __initialize_element(self):
        font = QtGui.QFont()
        font.setPointSize(11)

        # user name
        self.label_login.move(10, 10)
        self.label_login.setText("User name")
        self.label_login.setFont(font)
        self.label_login.adjustSize()

        self.text_line_login.move(self.label_login.x(), self.label_login.y() + 20)
        self.text_line_login.setPlaceholderText("Введите почту или номер телефона")
        self.text_line_login.setFixedWidth(self.width() - 20)
        self.text_line_login.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # password
        self.label_password.move(self.text_line_login.x(), self.text_line_login.y() + 50)
        self.label_password.setText("Password")
        self.label_password.setFont(font)
        self.label_password.adjustSize()

        self.text_line_password.move(self.text_line_login.x(), self.label_password.y() + 20)
        self.text_line_password.setPlaceholderText("Введите пароль")
        self.text_line_password.setFixedWidth(self.width() - 20)
        self.text_line_password.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # button
        self.button.setText("Войти")
        self.button.setFont(font)
        self.button.move(self.text_line_password.x(), self.text_line_password.y() + self.text_line_password.height() + 10)
        self.button.setStyleSheet("background-color: rgb(105,105,105);\n"
                                  "color: rgb(255, 255, 255);")
        self.button.clicked.connect(self.click_button)

        # checkbox
        self.label_check.setFont(font)
        self.label_check.setText("Запомнить меня")
        self.label_check.adjustSize()
        self.label_check.move(self.button.x() + self.button.width() + 40, self.button.y() + 5)

        self.check_remember.setGeometry(self.label_check.x() + self.label_check.width() + 10, self.label_check.y(),
                                        self.label_check.height(), self.label_check.height())
        self.check_remember.setChecked(False)

    def get_message(self, color="rgb(0, 0, 0)", text=""):
        self.message.setText(text)
        self.message.adjustSize()
        self.message.setStyleSheet("color:" + color)
        self.message.move(int(self.width() / 2) - int(self.message.width() / 2), self.button.y() + 40)
        self.message.repaint()

    def show_window(self):
        if self.check_remember.isChecked() is False:
            self.text_line_login.setText("")
            self.text_line_password.setText("")
        self.get_message()
        self.show()

    def click_button(self):
        if self.check_enter_login_password():
            self.get_message("rgb(255, 0, 0)", "Введите логин и пароль!")
            return
        self.get_message("rgb(0, 0, 0)", "Аутентификация...")

        driver = get_driver(2)

        self.data = get_data(self.text_line_login.text(), self.text_line_password.text())
        self.cookies = get_cookies(driver)
        self.headers = get_headers(self.data, driver)
        self.response = authentication(self.data, self.cookies, self.headers)
        if self.response.status_code == 200:
            if len(self.response.json()['errors']) == 0:

                # get new cookies after authentication
                cookies = dict_from_cookiejar(self.response.cookies)
                for el in cookies:
                    self.cookies[el] = cookies[el]

                # add new headers after authentication
                city_id = ""
                current_path = unquote(self.cookies["current_path"]).split('"city":"')[1]
                for char in current_path:
                    if char == '"':
                        break
                    city_id += char
                self.headers["cityid"] = city_id
                self.headers["authaccesstoken"] = self.cookies['auth_access_token']
                self.main_window.setWindowTitle(get_user_name(self.cookies, self.headers))
                # message authentication
                self.get_message("rgb(0, 255, 0)", "Вы авторизованны.")
                time.sleep(1)
                self.close()
            else:
                self.get_message("rgb(255, 0, 0)", self.response.json()['errors'][0])
        else:
            self.get_message("rgb(255, 0, 0)", " Не получаеться авторизоваться. Возможно, сайт не работает.")

    def check_enter_login_password(self):
        if self.text_line_login.text() == "" or self.text_line_password.text() == "":
            return True
        return False
