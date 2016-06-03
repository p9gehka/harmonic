from PyQt4 import QtGui, QtCore
import style as style

class Graphic(QtGui.QGraphicsView):
  def __init__(self, width, height, parent = None):
    QtGui.QWidget.__init__(self, parent)
    self.W = width
    self.H = height
    self.graphScene = QtGui.QGraphicsScene()
    self.setScene(self.graphScene)

    self.textList = []
    self.pointsList = []
    self.circlesList = []
    self.circlePen = QtGui.QPen(QtGui.QColor(style.circleOutline), style.circleOutlineW)
    self.pointBrush = QtGui.QBrush(QtGui.QColor(style.pointFill));
    self.pointPen = QtGui.QPen(QtGui.QColor(style.pointOutline))

  def drawValue(self, newCirclesList):
      ncl = len(newCirclesList)

      #circles
      dcl = self.circlesList[ncl:] #deleted circle list
      dpl = self.pointsList[ncl:] #deleted point list
      self.circlesList = self.circlesList[0:ncl]

      for circle in newCirclesList:
        circle.scaleY([0, 2], [0, 1])
        circle.scaleX([0, 2], [0, 1])

      self.drawPoints(newCirclesList, self.pointsList)
      self.drawCircles(newCirclesList, self.circlesList)

      #removing
      self.removeItems(dpl)
      self.removeItems(dcl)

  # newCirclesList, self.textList
  def drawCircles(self, newList, oldList):
    nl = len(newList) #newList length
    ol = len(oldList) #oldList length
    for i in range(nl):
      c = newList[i]; #circle
      x = c.x - c.r / 2
      y = c.y - c.r / 2
      if(i >= ol):
        t = self.graphScene.addEllipse(x, y, c.r, c.r, pen = self.circlePen)
        oldList.append(t)
      else:
        oldList[i].setRect(x, y, c.r, c.r)

  def drawPoints(self, newList, oldList):
    nl = len(newList)
    ol = len(oldList)
    for i in range(nl):
      c = newList[i]
      x = c.x - style.pointW / 2
      y = c.y - style.pointW / 2
      if(i >= ol):
        p = self.graphScene.addEllipse(x, y, style.pointW, style.pointW, pen = self.pointPen,  brush = self.pointBrush)
        oldList.append(p)
      else:
        oldList[i].setRect(x, y, style.pointW, style.pointW)

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
