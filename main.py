import sys
from PyQt5 import QtWidgets
from windows_app.main import Window


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
