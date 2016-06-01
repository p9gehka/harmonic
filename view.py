from PyQt4 import QtGui, QtCore

class Graphic(QtGui.QGraphicsView):
  def __init__(self, parent = None):
    QtGui.QWidget.__init__(self, parent)

    self.line = QtCore.QLineF(0, 0, 400, 400)
    self.graphScene = QtGui.QGraphicsScene()
    self.graphScene.addLine(self.line)
    self.setScene(self.graphScene)
    self.textList = []
  def drawValue(self, circlesList):
      print('emit')
      print(circlesList)
