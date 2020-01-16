import copy
import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

count = 0
algorithm_solution = []
text_file = []
jpg_file = []


class EndScreen(QWidget):
    def __init__(self, algorithm_solution_arg=None, *args):
        QWidget.__init__(self, *args)
        self.setMinimumSize(QSize(600, 600))
        global algorithm_solution
        algorithm_solution = []
        for (key, value) in algorithm_solution_arg.items():
            if value == True:
                algorithm_solution.append((str(key), value))
        self.setMaximumSize(QSize(600, 600))
        self.setWindowTitle("Lego")
        QApplication.setStyle("fusion")
        self.setWindowIcon(QIcon("Icon.png"))
        self.move(400, 100)
        self.init_UI()
        self.show()

    def init_UI(self):
        self.previous_button = QPushButton("Previous", self)
        self.previous_button.move(10, 540)
        self.previous_button.setFixedHeight(50)
        self.previous_button.setFixedWidth(140)
        self.previous_button.clicked.connect(self.previous_button_clicked)

        self.next_button = QPushButton("Next", self)
        self.next_button.move(450, 540)
        self.next_button.setFixedHeight(50)
        self.next_button.setFixedWidth(140)
        self.next_button.clicked.connect(self.next_button_clicked)

        self.configuration_image = QLabel(self)
        self.configuration_image.move(10, 10)
        self.configuration_image.setFixedWidth(580)
        self.configuration_image.setFixedHeight(520)
        # self.configuration_image.setStyleSheet("background-color: #F93822")

        self.configuration_name = QLabel(self)
        self.configuration_name.move(160, 540)
        self.configuration_name.setFixedHeight(50)
        self.configuration_name.setFixedWidth(130)
        self.configuration_name.setAlignment(Qt.AlignCenter)

        self.configuration_status = QLabel(self)
        self.configuration_status.move(310, 540)
        self.configuration_status.setFixedHeight(50)
        self.configuration_status.setFixedWidth(130)
        self.configuration_status.setStyleSheet("background-color: green")

        global text_file
        global jpg_file
        global count
        global algorithm_solution
        count = 0
        text_file = []
        jpg_file = []
        for root, dirs, files in os.walk(".\\configurations\\"):
            for i in files:
                if i.endswith(".txt"):
                    text_file.append(os.path.join(root, i))
                elif i.endswith(".jpg"):
                    text_file.append(os.path.join(root, i))
        if len(algorithm_solution) > 0:
            pix_map = QPixmap(".\\configurations\\" + algorithm_solution[count][0] + '.jpg')
            pix_map.scaled(580, 520)
            self.configuration_image.setPixmap(pix_map)
            self.configuration_name.setText("Configuration_" + algorithm_solution[count][0])
            self.next_button.setEnabled(True)
            self.previous_button.setEnabled(True)
        else:
            self.next_button.setEnabled(False)
            self.previous_button.setEnabled(False)

    def next_button_clicked(self):
        global count
        global algorithm_solution
        count = (count + 1) % len(algorithm_solution)
        pix_map = QPixmap(".\\configurations\\" + algorithm_solution[count][0] + '.jpg')
        pix_map.scaled(580, 520)
        self.configuration_image.setPixmap(pix_map)
        self.configuration_name.setText("Configuration_" + algorithm_solution[count][0])

    def previous_button_clicked(self):
        global count
        global algorithm_solution
        count = (count - 1) % len(algorithm_solution)
        pix_map = QPixmap(".\\configurations\\" + algorithm_solution[count][0] + '.jpg')
        pix_map.scaled(580, 520)
        self.configuration_image.setPixmap(pix_map)
        self.configuration_name.setText("Configuration_" + algorithm_solution[count][0])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    d = dict()
    d = {0: False, 1: True, 2: False, 3: True, 4: True, 5: False, 6: True, 7: False, 8: False, 9: True}
    mainWin = EndScreen(d)
    sys.exit(app.exec_())