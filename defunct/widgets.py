"""
Defunct <defunct<at>defunct.io> - NOP Developments LLC. 2016

The MIT License (MIT)
Copyright (c) <2016> <NOP Developments LLC>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""


from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt


class DefunctCore(QtCore.QObject):
    def __init__(self):
        super(DefunctCore, self).__init__()
        self._app = QtWidgets.QApplication.instance()
        self._main_window = [x for x in self._app.allWidgets() if x.__class__ is QtWidgets.QMainWindow][0]
        self._tool_menu = [x for x in self._main_window.menuWidget().children() if x.__class__ is QtWidgets.QMenu and x.title() == u'&Tools'][0]

class BinjaDockWidget(QtWidgets.QDockWidget):
    """Binja Dockable Widget
        A widget that uses PyQt5 to locate Binja window instances and inject them as parents to allow docking

    .. note::
        This is meant to be a PoC, the binja team is developing UI API for use in the long run.
    """
    def __init__(self, *__args):
        super(BinjaDockWidget, self).__init__(*__args)
        self._app = QtWidgets.QApplication.instance()
        self._main_window = [x for x in self._app.allWidgets() if x.__class__ is QtWidgets.QMainWindow][0]
        self._tool_menu = [x for x in self._main_window.menuWidget().children() if x.__class__ is QtWidgets.QMenu and x.title() == u'&Tools'][0]
        self._tabs = QtWidgets.QTabWidget()
        self.setWidget(self._tabs)
        self._main_window.addDockWidget(Qt.RightDockWidgetArea, self)
        self.addToolMenuAction('Toggle plugin dock', lambda: self.hide() if self.isVisible() else self.show())
        self.hide()

    def addToolMenuAction(self, name, function):
        self._tool_menu.addAction(name, function)

    def addTabWidget(self, widget, name):
        self._tabs.addTab(widget, name)
