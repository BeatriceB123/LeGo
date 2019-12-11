from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import json
import PIL.Image as Image
from util import drawImage


def populate_table_from_file(path, table, width):
    with open(path) as f:
        data = json.load(f)
    table.setRowCount(len(data))
    for i in range(0, len(data)):
        path = drawImage.imagePath
        drawImage.imagePath = drawImage.imagePath + data[i].get("Id")
        print(drawImage.imagePath)
        table.setCellWidget(i, 0, drawImage.ImgWidget())
        table.setItem(i, 1, QTableWidgetItem(data[i].get("Id")))
        table.setItem(i, 2, QTableWidgetItem(data[i].get("Number")))
        table.setItem(i, 3, QTableWidgetItem(data[i].get("Color")))
        print(drawImage.imagePath)
        image = Image.open(drawImage.imagePath + ".png")
        width2, height = image.size
        print(height)
        table.setRowHeight(i, height)

        drawImage.imagePath = path
    table.setColumnWidth(0, width)