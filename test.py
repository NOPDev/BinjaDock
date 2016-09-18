from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from binaryninja import *
from defunct.widgets import BinjaDockWidget

class TestWidget(QtWidgets.QWidget):
    def __init__(self, *__args):
        super(TestWidget, self).__init__(*__args)
        self.setLayout(QtWidgets.QStackedLayout())
        self.layout().addWidget(QtWidgets.QPushButton())
        self.show()

dock = BinjaDockWidget()
dock.addTabWidget(TestWidget(dock), "derp")
