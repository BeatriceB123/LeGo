import sys
import os, os.path
import PIL.Image as Image
from util import export, importFile, drawImage
from interface import add_config_screen as config
from interface import last_screen
import main_function

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

list_of_images_id = []
dictionary_of_images_size = {}
current_piece = ""
current_row = 0


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


class AddItemWindow(QWidget):

    def __init__(self, parent=None):
        super(AddItemWindow, self).__init__(parent)
        self.setFixedWidth(400)
        self.setFixedHeight(250)
        self.setWindowTitle("Add piece")
        self.move(700, 300)
        self.init_UI()

    def init_UI(self):
        self.tab_layout = QVBoxLayout()
        self.amount_layout = QHBoxLayout()
        self.color_layout = QHBoxLayout()
        self.setLayout(self.tab_layout)

        self.add_title_label()
        self.add_error_label()
        self.add_id_line()
        self.add_amount_line()
        self.tab_layout.addLayout(self.amount_layout)
        self.add_color_line()
        self.tab_layout.addLayout(self.color_layout)
        self.add_confirm_button()

        quit = QAction("Quit", self)
        quit.triggered.connect(self.close)

        self.show()

    def add_title_label(self):
        self.label = QLabel()
        self.label.setText("Add a brick type")
        self.label.setStyleSheet("font-weight: bold; font-size: 20px;")

        self.tab_layout.addWidget(self.label, alignment=Qt.AlignCenter)

    def add_error_label(self):
        self.error_label = QLabel()
        self.error_label.setText("Give a valid amount of bricks")
        self.error_label.setStyleSheet("color:red; font-weight: bold; font-size: 15px;")
        self.error_label.setVisible(False)

        self.tab_layout.addWidget(self.error_label, alignment=Qt.AlignCenter)

    def add_id_line(self):
        global current_piece
        self.id_label = QLabel()
        self.id_label.setText("ID piesa: " + current_piece)

        self.tab_layout.addWidget(self.id_label, alignment=Qt.AlignCenter)

    def add_amount_line(self):
        self.amount_label = QLabel()
        self.amount_label.setText("Number of bricks: ")

        self.amount_layout.addWidget(self.amount_label)

        self.amount_line_edit = QLineEdit()
        self.amount_line_edit.setValidator(QIntValidator())

        self.amount_layout.addWidget(self.amount_line_edit)

    def add_color_line(self):
        self.color_label = QLabel()
        self.color_label.setText("Choose color")

        self.color_layout.addWidget(self.color_label)

        self.color_box = QComboBox()
        self.color_box.addItem("Blue")
        self.color_box.addItem("Red")
        self.color_box.addItem("Green")
        self.color_box.addItem("Yellow")
        self.color_box.addItem("Lime-Green")
        self.color_box.addItem("Black")
        self.color_box.addItem("Gray")
        self.color_box.addItem("Light-Gray")
        self.color_box.addItem("Brown")
        self.color_box.addItem("Purple")

        self.color_layout.addWidget(self.color_box)

    def add_confirm_button(self):
        self.confirm_button = QPushButton()
        self.confirm_button.setText("Confirm")
        self.confirm_button.clicked.connect(self.confirm_functionality)

        self.tab_layout.addWidget(self.confirm_button, alignment=Qt.AlignCenter)

    def confirm_functionality(self):

        if self.amount_line_edit.text() == '' or self.amount_line_edit.text() == '0' or self.amount_line_edit.text() == '-':
            self.error_label.setVisible(True)
        else:
            path = drawImage.imagePath
            drawImage.imagePath = drawImage.imagePath + current_piece + ".png"

            row_position = mainWin.tableWidgetRight.rowCount()
            mainWin.tableWidgetRight.insertRow(row_position)

            mainWin.tableWidgetRight.setCellWidget(mainWin.tableWidgetRight.rowCount() - 1, 0,
                                                   drawImage.ImgWidget(self))
            mainWin.tableWidgetRight.setItem(mainWin.tableWidgetRight.rowCount() - 1, 1,
                                             QTableWidgetItem(current_piece))
            mainWin.tableWidgetRight.setItem(mainWin.tableWidgetRight.rowCount() - 1, 2,
                                             QTableWidgetItem(self.amount_line_edit.text()))
            mainWin.tableWidgetRight.setItem(mainWin.tableWidgetRight.rowCount() - 1, 3,
                                             QTableWidgetItem(self.color_box.currentText()))

            image = Image.open(drawImage.imagePath)
            width, height = image.size
            mainWin.tableWidgetRight.setRowHeight(mainWin.tableWidgetRight.rowCount() - 1, height)

            drawImage.imagePath = path
            mainWin.setEnabled(True)

            self.close()

    def closeEvent(self, event):
        mainWin.setEnabled(True)
        event.accept()


class UpdateItemWindow(QWidget):
    def __init__(self, parent=None):
        super(UpdateItemWindow, self).__init__(parent)
        self.setFixedWidth(400)
        self.setFixedHeight(250)
        self.setWindowTitle("Update piece")
        self.move(700, 300)
        self.init_UI()

    def init_UI(self):
        self.tab_layout = QVBoxLayout()
        self.amount_layout = QHBoxLayout()
        self.color_layout = QHBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.setLayout(self.tab_layout)

        self.add_title_label()
        self.add_error_label()
        self.add_id_line()
        self.add_amount_line()
        self.tab_layout.addLayout(self.amount_layout)
        self.add_color_line()
        self.tab_layout.addLayout(self.color_layout)
        self.add_buttons()
        self.tab_layout.addLayout(self.buttons_layout)

    def add_title_label(self):
        self.label = QLabel()
        self.label.setText("Update or delete a brick")
        self.label.setStyleSheet("font-weight: bold; font-size: 20px;")

        self.tab_layout.addWidget(self.label, alignment=Qt.AlignCenter)

    def add_error_label(self):
        self.error_label = QLabel()
        self.error_label.setText("Give a valid amount of bricks")
        self.error_label.setStyleSheet("color:red; font-weight: bold; font-size: 15px;")
        self.error_label.setVisible(False)

        self.tab_layout.addWidget(self.error_label, alignment=Qt.AlignCenter)

    def add_id_line(self):
        self.id_line = QLabel()
        self.id_line.setText("ID piesa: " + current_piece)
        self.tab_layout.addWidget(self.id_line, alignment=Qt.AlignCenter)

    def add_amount_line(self):
        self.amount_label = QLabel()
        self.amount_label.setText("Number of bricks: ")

        self.amount_layout.addWidget(self.amount_label)

        self.amount_line_edit = QLineEdit()
        self.amount_line_edit.setValidator(QIntValidator())

        self.amount_layout.addWidget(self.amount_line_edit)

    def add_color_line(self):
        self.color_label = QLabel()
        self.color_label.setText("Choose color")

        self.color_layout.addWidget(self.color_label)

        self.color_box = QComboBox()
        self.color_box.addItem("Blue")
        self.color_box.addItem("Red")
        self.color_box.addItem("Green")
        self.color_box.addItem("Yellow")
        self.color_box.addItem("Lime-Green")
        self.color_box.addItem("Black")
        self.color_box.addItem("Gray")
        self.color_box.addItem("Light-Gray")
        self.color_box.addItem("Brown")
        self.color_box.addItem("Purple")

        self.color_layout.addWidget(self.color_box)

    def add_buttons(self):
        self.delete_button = QPushButton()
        self.delete_button.setText("Delete")
        self.delete_button.clicked.connect(self.delete_functionality)
        self.buttons_layout.addWidget(self.delete_button)

        self.update_button = QPushButton()
        self.update_button.setText("Update")
        self.update_button.clicked.connect(self.update_functionality)
        self.buttons_layout.addWidget(self.update_button)

    def update_functionality(self):
        global current_row
        if self.amount_line_edit.text() == '' or self.amount_line_edit.text() == '0' or self.amount_line_edit.text() == '-':
            self.error_label.setVisible(True)
        else:
            mainWin.tableWidgetRight.setItem(current_row, 2, QTableWidgetItem(self.amount_line_edit.text()))
            mainWin.tableWidgetRight.setItem(current_row, 3, QTableWidgetItem(self.color_box.currentText()))
            mainWin.setEnabled(True)

            self.close()


    def delete_functionality(self):
        global current_row
        mainWin.tableWidgetRight.removeRow(current_row)
        mainWin.setEnabled(True)
        self.close()

    def closeEvent(self, event):
        mainWin.setEnabled(True)
        event.accept()


def get_number_of_lines():
    global list_of_images_id
    count = 0
    for root, dirs, files in os.walk("..\\lego_pictures\\"):
        for i in files:
            if i.split(".")[1] == "png":
                list_of_images_id.append(i.split(".")[0])
                count += 1
    return count


class MainWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.setMinimumSize(QSize(1200, 800))
        self.setMaximumSize(QSize(1200, 800))
        self.setWindowTitle("Lego")
        QApplication.setStyle("fusion")
        self.setWindowIcon(QIcon("Icon.png"))
        # self.setStyleSheet("background-color: #F93822")
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
        self.configuration_generate_layout = QHBoxLayout()

        self.creating_tables()
        self.add_filter_label()
        self.add_filter_line()
        self.left_side_layout.addLayout(self.left_side_filter_layout)
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
        self.add_configurtion_generate_buttons()
        self.right_side_layout.addLayout(self.configuration_generate_layout)

        self.left_side_filter_layout.setSpacing(0)

        self.show()

    def add_filter_label(self):
        self.label = QLabel()
        self.label.setText("Filtrare optiuni: ")
        self.left_side_filter_layout.addWidget(self.label)

    def add_filter_line(self):
        self.input = QLineEdit()
        self.input.setStyleSheet("background-color:white")
        self.input.setFixedWidth(200)
        self.input.setValidator(QIntValidator())
        self.input.keyPressEvent = self.keyPressEvent
        self.left_side_filter_layout.addWidget(self.input, alignment=Qt.AlignLeft)

    def add_configurtion_generate_buttons(self):
        self.button_configuration = QPushButton("Add Configuration", self)
        self.button_configuration.setFixedHeight(40)
        self.button_configuration.setFixedWidth(170)
        self.button_configuration.setStyleSheet("background-color:#FDD20E")
        self.button_configuration.clicked.connect(self.configuration_button_clicked)

        self.configuration_generate_layout.addWidget(self.button_configuration)

        self.button_generate = QPushButton("Generate", self)
        self.button_generate.setFixedHeight(40)
        self.button_generate.setFixedWidth(170)
        self.button_generate.setStyleSheet("background-color:#FDD20E")
        self.button_generate.clicked.connect(self.generate_button_clicked)

        self.configuration_generate_layout.addWidget(self.button_generate)

    def add_second_condition_line(self):
        self.check_box = QCheckBox()
        self.check_box.setStyleSheet("background-color:white")
        self.text = QLabel()
        self.text.setText("Aceleasi piese")
        self.second_condition_line.addWidget(self.check_box)
        self.second_condition_line.addWidget(self.text)
        self.second_condition_line.insertStretch(-1, 1)

    def add_first_condition_line(self):
        self.color_check_box = QCheckBox()
        self.color_check_box.setStyleSheet("background-color:white")
        self.color_text = QLabel()
        self.color_text.setText("Aceleasi culori")
        self.first_condition_line.addWidget(self.color_check_box)
        self.first_condition_line.addWidget(self.color_text)
        self.first_condition_line.insertStretch(-1, 1)

    def add_label(self):
        self.name_filter_label = QLabel()
        self.name_filter_label.setText("Criterii de filtrare")
        self.name_filter_label.setStyleSheet("font-weight: bold; font-size: 15px; padding-top: 20px;")
        self.name_filter_label.setAlignment(Qt.AlignLeft)
        self.right_side_layout.addWidget(self.name_filter_label)

    def creating_buttons(self):
        self.button_import = QPushButton('Import', self)
        self.button_import.setFixedHeight(40)
        self.button_import.setFixedWidth(170)
        self.button_import.setStyleSheet("background-color:#FDD20E")
        self.button_import.clicked.connect(self.import_button_clicked)

        self.import_export_layout.addWidget(self.button_import)

        self.button_export = QPushButton('Export', self)
        self.button_export.setFixedHeight(40)
        self.button_export.setFixedWidth(170)
        self.button_export.setStyleSheet("background-color:#FDD20E")
        self.button_export.clicked.connect(self.export_button_clicked)

        self.import_export_layout.addWidget(self.button_export)

    def create_second_table(self):
        self.tableWidgetRight = QTableWidget()
        self.tableWidgetRight.setRowCount(0)
        self.tableWidgetRight.setColumnCount(4)
        self.tableWidgetRight.setColumnWidth(0, self.max_width)
        self.tableWidgetRight.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidgetRight.cellDoubleClicked.connect(self.cell_for_update_was_clicked)
        self.tableWidgetRight.setHorizontalHeaderItem(0, QTableWidgetItem("Image"))
        self.tableWidgetRight.setHorizontalHeaderItem(1, QTableWidgetItem("ID"))
        self.tableWidgetRight.setHorizontalHeaderItem(2, QTableWidgetItem("Number of pieces"))
        self.tableWidgetRight.setHorizontalHeaderItem(3, QTableWidgetItem("Color"))
        self.tableWidgetRight.rowCount()
        self.tableWidgetRight.setStyleSheet("background-color:white")

        delegate = AlignDelegate(self.tableWidgetRight)
        self.tableWidgetRight.setItemDelegateForColumn(1, delegate)
        self.tableWidgetRight.setItemDelegateForColumn(2, delegate)
        self.tableWidgetRight.setItemDelegateForColumn(3, delegate)

        self.right_side_layout.addWidget(self.tableWidgetRight)

    def creating_tables(self):
        self.tableWidget = QTableWidget()
        self.row_count = get_number_of_lines()
        self.tableWidget.setRowCount(self.row_count)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setStyleSheet("background-color:white")

        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Image"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("ID"))

        global list_of_images_id
        self.max_width = 0

        for i in range(0, self.row_count):
            path = drawImage.imagePath
            drawImage.imagePath = drawImage.imagePath + list_of_images_id[i]


            self.tableWidget.setCellWidget(i, 0, drawImage.ImgWidget(self))
            id_item = QTableWidgetItem(list_of_images_id[i])
            id_item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(i, 1, id_item)

            image = Image.open(drawImage.imagePath + ".png")
            width, height = image.size
            self.tableWidget.setRowHeight(i, height)
            drawImage.imagePath = path
            if width > self.max_width:
                self.max_width = width

        self.tableWidget.setColumnWidth(0, self.max_width)
        self.tableWidget.setFixedWidth(self.tableWidget.columnWidth(0) + self.tableWidget.columnWidth(1) + 41)

        self.tableWidget.cellClicked.connect(self.cell_was_clicked)

        self.left_side_layout.addWidget(self.tableWidget)

    def generate_button_clicked(self):
        where_are_we = os.getcwd()
        if where_are_we[-9:] != "interface":
            os.chdir(os.getcwd() + "\\interface")
        result = dict()
        list_of_data = []
        for row in range(0, self.tableWidgetRight.rowCount()):
            list_of_data.append((int(self.tableWidgetRight.item(row, 1).text()),
                                 int(self.tableWidgetRight.item(row, 2).text()),
                                 self.tableWidgetRight.item(row, 3).text()))
        result = main_function.main_function(list_of_data, self.check_box.isChecked(), self.color_check_box.isChecked(), flg=True)
        # os.chdir("..\\interface")
        self.end_tab = last_screen.EndScreen(result)

    def configuration_button_clicked(self):
        self.config_tab = config.AddConfigurationScreen()

    def import_button_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(filter='JSON(*.json)')
        if filename is not '':
            self.tableWidgetRight.setRowCount(0)
            importFile.populate_table_from_file(filename, self.tableWidgetRight, self.max_width)

    def export_button_clicked(self):
        filename, _ = QFileDialog.getSaveFileName(filter='JSON(*.json)')
        if filename is not '':
            export.write_to_json_file(filename, self.tableWidgetRight)

    def cell_was_clicked(self, row, column):
        global current_piece
        current_piece = self.tableWidget.item(row, 1).text()
        self.tab = AddItemWindow()
        self.setEnabled(False)

        self.tab.show()

    def cell_for_update_was_clicked(self, row, column):
        global current_piece
        global current_row
        current_piece = self.tableWidgetRight.item(row, 1).text()
        current_row = row
        self.tab = UpdateItemWindow()
        self.setEnabled(False)

        self.tab.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Backspace:
            self.input.setText(self.input.text()[:-1])
        else:
            self.input.setText(self.input.text() + e.text())
        for index in range(0, self.tableWidget.rowCount()):
            if self.tableWidget.item(index, 1).text().startswith(self.input.text()):
                self.tableWidget.setRowHidden(index, False)
            else:
                self.tableWidget.setRowHidden(index, True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())
