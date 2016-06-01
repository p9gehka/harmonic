from PyQt4 import QtGui, QtCore
from view import Graphic
from controllers import Buttons
from controllersDataService import ControllersData

import AppConfig
import sys
import time

class Thread(QtCore.QThread):
    def __init__(self, cb, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.cb = cb
    def run(self):
        self.cb()

class MainWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.controllersData = ControllersData()

        self.graphView = Graphic()
        self.buttons = Buttons(self.circleSync, self.countSync, self.globalSync)
        self.buttons.setGlobalValue(0, True, 100)

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addWidget(self.graphView)
        self.vbox.addWidget(self.buttons)
        self.setLayout(self.vbox)

        self.cycle = Thread(self.drawCicle);
        self.connect(self.cycle, QtCore.SIGNAL('draw(QVariant)'), self.graphView.drawValue, QtCore.Qt.QueuedConnection)

    def circleSync(self, index, radius, frequency, phase):
        self.controllersData.setData(index, radius, frequency, phase)

    def countSync(self, count):
        self.controllersData.setCirclesCount(count)

    def globalSync(self, index, show, speedSlow):
        data = self.controllersData.getDataIndex(index)
        self.buttons.setCircleData(data[0], data[1], data[2])

    def drawCicle(self):
        theta = 0
        F = 0.3
        rate = 1 / 60
        while True:
            theta += rate + F;
            circlesList = self.controllersData.getCirclesList()
            self.emit(QtCore.SIGNAL('draw(QVariant)'), circlesList)
            time.sleep(0.03)

    def runAnimation(self):
        self.cycle.start()

app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.resize(AppConfig.WinH, AppConfig.WinW)
window.show()
window.runAnimation()
sys.exit(app.exec())
