"""
Defunct <defunct<at>defunct.io> - NOP Developments LLC. 2016

    Yarascan - v0.1.0
        Binja plugin that implements Yara signature scanning and navigation in a dockable widget.

    Useful crypto / malware / anti-vm signatures used (https://github.com/Yara-Rules/rules.git)

MIT License

Copyright (c) <2016> <NOP Developments LLC>                                                                                         

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


"""

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from binaryninja import *
from defunct import BinjaWidget
import defunct.widgets

import yara

class YaraWidget(BinjaWidget):
    """Binja Yara plugin
        Identifies yara signatures and displays them in a BinjaDockWidget.
    """
    def __init__(self):

        super(YaraWidget, self).__init__('Yara')
        self._rules = yara.compile(filepath=core.BNGetUserPluginDirectory() + '/yara/crypto_signatures.yar')
        self._table = QtWidgets.QTableWidget()
        self._table.setColumnCount(2)
        self._table.setHorizontalHeaderLabels(['Offset', 'Signature'])
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.verticalHeader().setVisible(False)
        self.setLayout(QtWidgets.QStackedLayout())
        self.layout().addWidget(self._table)
        self.setObjectName('BNPlugin_Yara')
        # self.addToolMenuAction("&Yara about", lambda: log_info('Yara scan!'))

    class YaraThread(QtCore.QThread):
        finished = QtCore.pyqtSignal(list)

        def __init__(self, rules, file):
            super(YaraWidget.YaraThread, self).__init__()
            self._rules = rules
            self._file = file

        def run(self):
            self.finished.emit(self._rules.match(self._file))

    def scan(self, bv):
        """ Scans a binary view for with the compiled yara rules
        :param bv:  The BinaryView to use
        :type bv: binaryninja.BinaryView
        :return:
        """
        self._view = bv
        self._thread = YaraWidget.YaraThread(self._rules, bv.file.filename)
        self._thread.finished.connect(self.scan_finished)
        self._thread.start()

    @QtCore.pyqtSlot(list)
    def scan_finished(self, matches):
        records = [[x.rule, a[0]] for x in matches for a in x.strings]
        self._table.setRowCount(len(records))
        for i in range(0, len(records)):
            # TODO: Proper QTableView / model implementation instead of lazy use of QTableWidget
            desc = QtWidgets.QTableWidgetItem(records[i][0])
            desc.setFlags(Qt.ItemIsEnabled)
            # TODO: meta tooltip
            offset = QtWidgets.QTableWidgetItem('0x%.8x' % records[i][1])
            offset.setFlags(Qt.ItemIsEnabled)
            offset.setForeground(QtGui.QColor(162, 217, 175))
            self._table.setItem(i, 0, offset)
            self._table.setItem(i, 1, desc)

        self._table.cellDoubleClicked.connect(self.cell_action)
        self._thread.terminate()
        self._core.show()
        self._core.selectTab(self)
        self.show()

    def cell_action(self, row, column):
        # TODO: view highlighting
        self.navigate(self._view, int(self._table.item(row, 0).text(), 16))

    def navigate(self, bv, offset):
        bv.navigate('Hex:' + bv.view_type, offset)



d = YaraWidget()
def scan(bv, offset):
    d.scan(bv)

PluginCommand.register_for_address('Yara', 'Scan for yara signatures', scan)
