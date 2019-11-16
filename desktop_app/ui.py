import sys
from random import randint

from PyQt5 import QtWidgets, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(600, 500))
        self.setMaximumSize(QSize(600, 500))
        self.setWindowTitle("Demo app")
        QApplication.setStyle("fusion")
        self.move(1000, 200)

        self.button_start = QPushButton('Start', self)
        self.button_start.setFixedHeight(40)
        self.button_start.setFixedWidth(170)
        self.button_start.move(10, 215)
        self.button_start.clicked.connect(self.start_function)
        self.update()

        self.button_stop = QPushButton('Stop', self)
        self.button_stop.setFixedHeight(40)
        self.button_stop.setFixedWidth(170)
        self.button_stop.move(200, 215)
        self.button_stop.setDisabled(True)
        self.button_stop.clicked.connect(self.stop_function)
        self.update()

        self.label = QLineEdit(self)
        self.label.move(10, 170)
        self.label.resize(170, 40)
        self.label.setEnabled(False)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: red;")
        self.label.setText("Test")
        self.update()

    def start_function(self):
        self.button_start.setDisabled(True)
        self.button_stop.setDisabled(False)
        self.label.setText("Start Pres")
        self.move(randint(0, 700), randint(0, 700))

    def stop_function(self):
        self.label.setText("Stop Press")
        self.button_start.setDisabled(False)
        self.button_stop.setDisabled(True)
        self.move(randint(0, 700), randint(0, 700))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    mainWin.update()
    sys.exit(app.exec_())
