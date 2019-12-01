import sys
import os, os.path
import PIL.Image as Image

from random import randint

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic.properties import QtGui

imagePath = "../desktop_app/lego_pictures/"
list_of_images_id = []
dictionary_of_images_size = {}


class ImgWidget(QWidget):

    def __init__(self, parent=None):
        super(ImgWidget, self).__init__(parent)
        self.pic = QPixmap(imagePath)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pic)


class MainWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.setMinimumSize(QSize(1200, 800))
        self.setMaximumSize(QSize(1200, 800))
        self.setWindowTitle("Demo app")
        QApplication.setStyle("fusion")
        self.move(400, 100)
        self.init_UI()

    def init_UI(self):
        self.tab_layout = QHBoxLayout()
        self.setLayout(self.tab_layout)
        self.left_side_layout = QVBoxLayout()
        self.right_side_layout = QVBoxLayout()
        self.left_side_filter_layout = QHBoxLayout()
        self.import_export_layout = QHBoxLayout()
        self.first_condition_line = QHBoxLayout()
        self.second_condition_line = QHBoxLayout()

        self.creating_tables()
        self.add_filter_label()
        self.add_filter_line()
        self.left_side_layout.addLayout(self.left_side_filter_layout)
        # self.left_side_layout.setSizeConstraint(QLayout_SizeConstraint=s)
        self.tab_layout.addLayout(self.left_side_layout)


        self.create_second_table()
        self.tab_layout.addLayout(self.right_side_layout)
        self.creating_buttons()
        self.right_side_layout.addLayout(self.import_export_layout)
        self.add_label()
        self.add_first_condition_line()
        self.right_side_layout.addLayout(self.first_condition_line)
        self.add_second_condition_line()
        self.right_side_layout.addLayout(self.second_condition_line)
        self.add_generate_button()

        # self.left_side_layout.setGeometry(QRect(0, 0, 100, 900))
        # print(self.left_side_layout.direction())


        self.left_side_filter_layout.setSpacing(0)


        self.show()


    def add_filter_label(self):
        self.label = QLabel()
        self.label.setText("Filtrare optiuni: ")
        self.left_side_filter_layout.addWidget(self.label)

    def add_filter_line(self):
        self.input = QLineEdit()
        self.input.setFixedWidth(200)
        self.left_side_filter_layout.addWidget(self.input, alignment=Qt.AlignLeft)

    def add_generate_button(self):
        self.button_generate = QPushButton("Generate", self)
        self.button_generate.setFixedHeight(40)
        self.button_generate.setFixedWidth(170)
        self.button_generate.setStyleSheet("background-color:#6e6e6e")
        self.right_side_layout.addWidget(self.button_generate, alignment=Qt.AlignCenter)

    def add_second_condition_line(self):
        self.check_box = QCheckBox()
        self.text = QLabel()
        self.text.setText("Descompunere")
        self.second_condition_line.addWidget(self.check_box)
        self.second_condition_line.addWidget(self.text)

    def add_first_condition_line(self):
        self.check_box = QCheckBox()
        self.text = QLabel()
        self.text.setText("Aceeasi culoare")
        self.first_condition_line.addWidget(self.check_box)
        self.first_condition_line.addWidget(self.text)

    def add_label(self):
        self.name_filter_label = QLabel()
        self.name_filter_label.setText("Criterii de filtrare")
        self.name_filter_label.setStyleSheet("font-weight: bold; font-size: 15px; padding-top: 20px;")
        self.name_filter_label.setAlignment(Qt.AlignCenter)
        self.right_side_layout.addWidget(self.name_filter_label)

    def creating_buttons(self):
        self.button_import = QPushButton('Import', self)
        self.button_import.setFixedHeight(40)
        self.button_import.setFixedWidth(170)
        # self.button_start.move(500, 215)
        self.button_import.setStyleSheet("background-color:#6e6e6e")
        self.import_export_layout.addWidget(self.button_import)

        self.button_export = QPushButton('Export', self)
        self.button_export.setFixedHeight(40)
        self.button_export.setFixedWidth(170)
        # self.button_end.move(500, 115)
        self.button_export.setStyleSheet("background-color:#6e6e6e")
        self.import_export_layout.addWidget(self.button_export)

    def create_second_table(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Image"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("ID"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Number of pieces"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Color"))
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Name"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Email"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("Phone No"))
        # self.tableWidget.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        header = self.tableWidget.horizontalHeader()
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.right_side_layout.addWidget(self.tableWidget)

    def creating_tables(self):
        self.tableWidget = QTableWidget()
        self.row_count = self.get_number_of_lines()
        self.tableWidget.setRowCount(self.row_count)
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Imagine"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("ID"))

        global imagePath
        global list_of_images_id
        self.max_width = 0

        for i in range(0, self.row_count):
            path = imagePath
            imagePath = imagePath + list_of_images_id[i]

            self.tableWidget.setCellWidget(i, 0, ImgWidget(self))
            id_item = QTableWidgetItem(list_of_images_id[i])
            id_item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(i, 1, id_item)

            image = Image.open(imagePath + ".png")
            width, height = image.size
            self.tableWidget.setRowHeight(i, height)
            imagePath = path
            if width > self.max_width:
                self.max_width = width

        self.tableWidget.setColumnWidth(0, self.max_width)

        print(self.tableWidget.geometry())
        print(self.tableWidget.columnWidth(0))
        print(self.tableWidget.columnWidth(1))
        self.tableWidget.setFixedWidth(self.tableWidget.columnWidth(0) + self.tableWidget.columnWidth(1) + 41)
        print(self.tableWidget.width())
        self.left_side_layout.addWidget(self.tableWidget)

    def get_number_of_lines(self):
        global list_of_images_id
        count = 0
        for root, dirs, files in os.walk("../desktop_app/lego_pictures"):
            for i in files:
                if i.split(".")[1] == "png":
                    list_of_images_id.append(i.split(".")[0])
                    count += 1
        return count
