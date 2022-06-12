from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GroupBox(QGroupBox):
    def __init__(self, main_window, name: str, data: dict, highlight=None, color="black", image=None):
        super().__init__()
        self.setTitle(self._get_name(name))
        self.resize(main_window.width() - 30, 100)
        self.adjustSize()
        self.setStyleSheet("QGroupBox:title {"
                           "subcontrol-origin: margin;"
                           "subcontrol-position: top center;"
                           "padding-left: 10px;"
                           "padding-right: 10px; }")

        self.layout_1 = QGridLayout()
        self.data = data
        self._initialize_element(highlight, color, image)
        self.setLayout(self.layout_1)

    def _initialize_element(self, highlight, color, img):
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.setFont(font)

        if img is not None:
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(img))

            image = QLabel()
            image.setScaledContents(True)
            image.setStyleSheet("border: 1px solid black;")
            image.setPixmap(pixmap)
            self.layout_1.addWidget(image, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        p = self.layout_1.count()
        for i, el in enumerate(self.data):
            font.setBold(False)
            label_left = self.get_label(el, font)
            self.layout_1.addWidget(label_left, i + p, 0)

            label_right = self.get_label(str(self.data[el]), font)
            if highlight is not None and highlight.__contains__(i):
                label_right.setStyleSheet(f"color: {color}")
            if el.__contains__("URL"):
                label_right.setOpenExternalLinks(True)
            self.layout_1.addWidget(label_right, i + p, 1, alignment=Qt.AlignmentFlag.AlignRight)

    @staticmethod
    def _get_name(name):
        result = ""
        check = True
        for i in range(len(name)):

            if name[i] == "[":
                check = False
            elif name[i] == "]":
                check = True
                i += 1
                continue

            if check:
                result += name[i]
        return result

    @staticmethod
    def get_label(text, font):
        label = QLabel(text)
        label.setFont(font)
        label.adjustSize()
        return label
