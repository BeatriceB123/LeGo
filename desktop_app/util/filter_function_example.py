import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainGui(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(218, 379)
        self.centralwidget = QWidget(MainWindow)
        self.layout = QVBoxLayout(self.centralwidget)
        self.p_text = QLineEdit(self.centralwidget)
        self.layout.addWidget(self.p_text)
        MainWindow.setCentralWidget(self.centralwidget)

        # iti apeleaza functia la fiecare keypress
        self.p_text.keyPressEvent = self.keyPressEvent

    def keyPressEvent(self, e):
        print(e.text())
        if e.key() == Qt.Key_Backspace:
            self.p_text.setText(self.p_text.text()[:-1])
        else:
            self.p_text.setText(self.p_text.text() + e.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = MainGui()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())