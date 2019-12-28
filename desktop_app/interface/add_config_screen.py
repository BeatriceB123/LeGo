import sys

import PIL.Image as Image
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
sys.path.append("..")
from configuration import *
from util import drawImage


list_of_images_id_add = []
add_draw_image = "..\\lego_pictures\\"


class AddConfigurationScreen(QWidget):
    configuration1 = Configuration(True)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add Configuration')
        self.setMinimumSize(QSize(900, 420))
        self.setMaximumSize(QSize(900, 420))
        QApplication.setStyle("fusion")
        self.move(400, 400)

        self.configuration_information = QPlainTextEdit(self)
        self.configuration_information.move(20, 10)
        self.configuration_information.resize(600, 200)
        self.configuration_information.setReadOnly(True)

        self.x_label = QLabel(self)
        self.x_label.setText("X")
        self.x_label.move(20, 230)
        self.x_label.resize(30, 30)

        self.x_line = QLineEdit(self)
        self.x_line.move(30, 230)
        self.x_line.resize(40, 30)

        self.y_label = QLabel(self)
        self.y_label.setText("Y")
        self.y_label.move(80, 230)
        self.y_label.resize(30, 30)

        self.y_line = QLineEdit(self)
        self.y_line.move(90, 230)
        self.y_line.resize(40, 30)

        self.z_label = QLabel(self)
        self.z_label.setText("Z")
        self.z_label.move(140, 230)
        self.z_label.resize(30, 30)

        self.z_line = QLineEdit(self)
        self.z_line.move(150, 230)
        self.z_line.resize(40, 30)

        self.id_db_label = QLabel(self)
        self.id_db_label.move(200, 230)
        self.id_db_label.resize(50, 30)
        self.id_db_label.setText("ID DB")

        self.id_db_line = QLineEdit(self)
        self.id_db_line.move(230, 230)
        self.id_db_line.resize(50, 30)

        self.color_dropdown = QComboBox(self)
        self.color_dropdown.move(290, 230)
        self.color_dropdown.resize(60, 30)
        self.color_dropdown.addItem("Blue")
        self.color_dropdown.addItem("Red")
        self.color_dropdown.addItem("Green")

        self.rotaton_label = QLabel(self)
        self.rotaton_label.move(354, 230)
        self.rotaton_label.resize(50, 30)
        self.rotaton_label.setText("Rotation")

        self.rotaton = QComboBox(self)
        self.rotaton.move(400, 230)
        self.rotaton.resize(60, 30)
        self.rotaton.addItem("0")
        self.rotaton.addItem("1")
        self.rotaton.addItem("2")
        self.rotaton.addItem("3")

        self.add_button_studs = QPushButton("Add in studs", self)
        self.add_button_studs.move(20, 270)
        self.add_button_studs.resize(130, 30)
        self.add_button_studs.clicked.connect(self.add_button_stubs_clicked)

        self.add_button_tbes = QPushButton("Add in tubes", self)
        self.add_button_tbes.move(160, 270)
        self.add_button_tbes.resize(130, 30)
        self.add_button_tbes.clicked.connect(self.add_button_tubes_clicked)

        self.add_status = QLabel(self)
        self.add_status.move(300, 270)
        self.add_status.resize(100, 30)
        self.add_status.setText("")

        self.id_config_label = QLabel(self)
        self.id_config_label.setText("ID config")
        self.id_config_label.move(50, 310)
        self.id_config_label.resize(50, 30)

        self.id_config_line = QLineEdit(self)
        self.id_config_line.move(100, 310)
        self.id_config_line.resize(40, 30)

        self.remove_button = QPushButton("Remove", self)
        self.remove_button.move(160, 310)
        self.remove_button.resize(100, 30)
        self.remove_button.clicked.connect(self.remove_button_clicked)

        self.remove_status = QLabel(self)
        self.remove_status.move(280, 310)
        self.remove_status.resize(100, 30)
        self.remove_status.setText("")

        self.select_path_label = QLabel(self)
        self.select_path_label.move(50, 370)
        self.select_path_label.resize(140, 30)
        self.select_path_label.setText("Name/path to file")

        self.select_path_line = QLineEdit(self)
        self.select_path_line.move(150, 370)
        self.select_path_line.resize(200, 30)

        self.select_path_button = QPushButton("Choose config image", self)
        self.select_path_button.move(360, 370)
        self.select_path_button.resize(120, 30)
        self.select_path_button.clicked.connect(self.select_path_button_clicked)

        self.creating_table()

        self.show()

    def creating_table(self):
        row_cnt = get_number_of_lines()
        self.help_table = QTableWidget(self)
        self.help_table.move(630, 10)
        self.help_table.setFixedHeight(400)
        self.help_table.setRowCount(row_cnt)
        self.help_table.setColumnCount(2)
        self.help_table.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.help_table.setHorizontalHeaderItem(1, QTableWidgetItem("Image"))

        for i in range(0, row_cnt):
            aux = add_draw_image + list_of_images_id_add[i]
            drawImage.imagePath = aux

            id_item = QTableWidgetItem(list_of_images_id_add[i])
            id_item.setTextAlignment(Qt.AlignCenter)
            self.help_table.setItem(i, 0, id_item)
            self.help_table.setCellWidget(i, 1, drawImage.ImgWidget(self))

            image = Image.open(aux + ".png")
            width, height = image.size
            self.help_table.setRowHeight(i, height)

    def select_path_button_clicked(self):
        filename, _ = QFileDialog.getOpenFileName(filter='PNG(*.png)')
        if filename is not '':
            self.select_path_line.setText(filename)

    def add_button_stubs_clicked(self):
        if self.x_line.text() == "" or \
                self.y_line.text() == "" or \
                self.z_line.text() == "":
            print("Ok")
        else:
            self.add_status.setText("Failled")

    def add_button_tubes_clicked(self):
        # global configuration1
        global list_of_images_id_add
        if self.x_line.text() is not '' and \
                self.y_line.text() is not '' and \
                self.z_line.text() is not '' and \
                self.id_db_line.text() is not '' and  \
                self.id_db_line.text() in list_of_images_id_add:
            print(int(self.id_db_line.text()), str(self.color_dropdown.currentText()), [int(self.x_line.text()), int(self.y_line.text()), int(self.z_line.text())], int(self.rotaton.currentText()))
            if self.configuration1.place_in_tubes(Brick(int(self.id_db_line.text()), str(self.color_dropdown.currentText()), self.configuration1), [int(self.x_line.text()), int(self.y_line.text()), int(self.z_line.text())], rotation=int(self.rotaton.currentText())):
                self.add_status.setText("Succes")
            else:
                self.add_status.setText("Failled")
        else:
            self.add_status.setText("Failled")

    def remove_button_clicked(self):
        print("Ceva again")


def get_number_of_lines():
    global list_of_images_id_add
    count = 0
    for root, dirs, files in os.walk("..\\lego_pictures\\"):
        for i in files:
            if i.split(".")[1] == "png":
                list_of_images_id_add.append(i.split(".")[0])
                count += 1
    return count


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = AddConfigurationScreen()
    sys.exit(app.exec_())
