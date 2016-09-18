from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from binaryninja import *
from defunct.widgets import BinjaWidget

class TestWidget(BinjaWidget):
    def __init__(self, *__args):
        super(TestWidget, self).__init__('Entropy')
        self.setLayout(QtWidgets.QStackedLayout())
        self.layout().addWidget(QtWidgets.QPushButton())
        self.show()

TestWidget()
