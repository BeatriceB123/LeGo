import PIL.Image as Image
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

imagePath = "../desktop_app/lego_pictures/"


class ImgWidget(QWidget):

    def __init__(self, parent=None):
        super(ImgWidget, self).__init__(parent)
        self.pic = QPixmap(imagePath)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pic)