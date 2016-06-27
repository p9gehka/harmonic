from PyQt4 import QtGui, QtCore
from view import Graphic
from controllers import Buttons
from controllersDataService import ControllersData
from furieService import MathLogic

import AppConfig
import sys
import time


class Thread(QtCore.QThread):
    def __init__(self, cb, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.cb = cb
    def run(self):
        self.cb(self)

class MainWindow(QtGui.QWidget):
    theta = 0
    speedSlow = 1
    showAnimation = True

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.controllersData = ControllersData()

        self.vbox = QtGui.QVBoxLayout()
        self.graphView = Graphic(400, 400, self)
        self.buttons = Buttons(self.circleSync, self.countSync, self.globalSync, self.reset)
        self.buttons.setGlobalValue(0, True, self.speedSlow)

        self.vbox.addWidget(self.graphView)
        self.vbox.addWidget(self.buttons)
        self.setLayout(self.vbox)

        self.cycle = Thread(self.drawCicle);
        self.connect(self.cycle, QtCore.SIGNAL('drawCircle(QVariant)'), self.on_drawCircles, QtCore.Qt.QueuedConnection)
        self.connect(self.cycle, QtCore.SIGNAL('drawGPath(QVariant, QVariant)'), self.on_drawGPath, QtCore.Qt.QueuedConnection)
        self.connect(self.cycle, QtCore.SIGNAL('drawStatic()'), self.on_drawStatic, QtCore.Qt.QueuedConnection)

    def circleSync(self, index, radius, frequency, phase):
        self.controllersData.setData(index, radius, frequency, phase)

    def countSync(self, count):
        self.controllersData.setCirclesCount(count)

    def globalSync(self, index, show, speedSlow):
        self.showAnimation = show;
        data = self.controllersData.getDataIndex(index)
        self.buttons.setCircleData(data[0], data[1], data[2])
        self.speedSlow = speedSlow
        self.graphView.setSelected(index)


    def reset(self):
      self.theta = 0

    def drawCicle(self, thread):
        rate = 1 / 60;
        while True:
            if(self.showAnimation):
              self.theta += rate / float(self.speedSlow)
            circlesList = self.controllersData.getCirclesList()
            fxList = MathLogic.getCoords(self.theta, circlesList)
            gPath = MathLogic.getGPath(-self.theta, circlesList)
            gPoint = MathLogic.getGPoint(-self.theta, circlesList)
            thread.emit(QtCore.SIGNAL('drawCircle(QVariant)'), fxList)
            thread.emit(QtCore.SIGNAL('drawGPath(QVariant, QVariant)'), gPath, gPoint)
            thread.emit(QtCore.SIGNAL('drawStatic()'))
            time.sleep(rate)

    def on_drawCircles(self, valuesList):
        self.graphView.drawCircles(valuesList)
    def on_drawGPath(self, gPath, gPoint):
        self.graphView.drawGPath(gPath, gPoint)
    def on_drawStatic(self):
        self.graphView.drawStaticObject()
    def runAnimation(self):
        self.cycle.start()

app = QtGui.QApplication(sys.argv)
window = MainWindow()
window.resize(AppConfig.WinH, AppConfig.WinW)
window.show()
window.runAnimation()
sys.exit(app.exec())
