from PyQt4 import QtGui, QtCore

class Graphic(QtGui.QGraphicsView):
  def __init__(self, width, height, parent = None):
    QtGui.QWidget.__init__(self, parent)
    self.W = width
    self.H = height
    self.line = QtCore.QLineF(0, 0, width, height)
    self.graphScene = QtGui.QGraphicsScene()
    self.graphScene.addLine(self.line)
    self.setScene(self.graphScene)

    self.textList = []
    self.circlesList = []

  def drawValue(self, newCirclesList):
      ncl = len(newCirclesList)
      dtl = self.textList[ncl:]
      self.textList = self.textList[0:ncl]
      self.drawText(newCirclesList, self.textList)
      self.drawCircles(newCirclesList, self.circlesList)

      #removing
      self.removeItems(dtl)

  def drawCircles(self, newList, oldList):

  # newCirclesList, self.textList
  def drawText(self, newList, oldList):
    nl = len(newList)
    ol = len(oldList)
    for i in range(nl):
      circle = newList[i]
      values = '{0} r{1} p{2}'.format(circle.frequency, circle.radius, circle.phase)
      if(i >= ol):
        t = self.graphScene.addSimpleText(values)
        t.setY(i * 15)
        oldList.append(t)
      else:
        oldList[i].setText(values)

  def removeItems(self, circlesList):
    for item in circlesList:
      self.graphScene.removeItem(item)
