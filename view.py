from PyQt4 import QtGui, QtCore
import style as style
import math

class Graphic(QtGui.QGraphicsView):
  textList = []
  pointsList = []
  circlesList = []
  linesList = []
  pointPrev = 0;
  graphPoint = False;
  margin = 0
  def __init__(self, width, height,window, parent = None):
    QtGui.QWidget.__init__(self, parent)
    self.window = window
    self.W = width
    self.H = height
    self.graphPoint = QtCore.QPointF(0, 0)
    self.graphScene = QtGui.QGraphicsScene()
    self.setScene(self.graphScene)

    self.circlePen = QtGui.QPen(QtGui.QColor(style.circleOutline), style.circleOutlineW)
    self.selectedCirclePen = QtGui.QPen(QtGui.QColor(style.circleSelectedOutline), 3)

    self.axisPen = QtGui.QPen(QtGui.QColor(style.axis))

    self.gPathPen = QtGui.QPen(QtGui.QColor(style.gPathLine), style.gPathLineW)
    self.gLinePen = QtGui.QPen(QtGui.QColor(style.gLine))
    self.pointBrush = QtGui.QBrush(QtGui.QColor(style.pointFill));
    self.pointPen = QtGui.QPen(QtGui.QColor(style.pointOutline))
    self.selectedCircle = self.graphScene.addEllipse(0, 0, 0, 0, pen = self.selectedCirclePen)
    self.lineGroup = self.graphScene.createItemGroup([])

    self.xPath = self.graphScene.addLine(-self.margin, 0.0, self.rect().right(), 0.0, pen = self.axisPen)
    self.yPath = self.graphScene.addLine(0.0, -self.rect().height() / 2, 0.0, self.rect().height() / 2, pen = self.axisPen)
    self.graphScene.setSceneRect(-self.margin, -self.rect().height() / 2, self.rect().width(), self.rect().height())

    self.gLine = self.graphScene.addLine(0, 0, 0, 0, pen = self.gLinePen)
    self.oLine = self.graphScene.addLine(0, 0, 0, 0, pen = self.gLinePen)
    self.fText = self.graphScene.addSimpleText('');
  def setSelected(self, index):
    self.selected = index

  def drawCircles(self, newCirclesList):
      ncl = len(newCirclesList)

      #circles
      dcl = self.circlesList[ncl:] #deleted circle list
      dpl = self.pointsList[ncl:] #deleted point list
      self.circlesList = self.circlesList[0:ncl]
      self.pointsList = self.pointsList[0:ncl]


      for circle in newCirclesList:
        circle.scaleY([0, 2], [0, 1])
        circle.scaleX([0, 2], [0, 1])

      self.drawPoints(newCirclesList, self.pointsList)
      self.drawOutline(newCirclesList, self.circlesList)
      self.drawSelected()

      #removing
      if(len(dcl) > 0 or len(dpl) > 0):
        self.removeItems(dcl)
        self.removeItems(dpl)

  def drawStaticObject(self):
    self.xPath.setLine(-self.margin, 0.0, self.rect().right(), 0.0)
    if(self.rect().height() / 2 > self.margin):
      self.graphScene.setSceneRect(-self.margin, -self.rect().height() / 2, self.rect().width(), self.rect().height())
      self.yPath.setLine(0.0, - self.rect().height() / 2, 0.0, self.rect().height() / 2)
    else:
      self.graphScene.setSceneRect(-self.margin, -self.margin, self.rect().width(), self.margin * 2)
      self.yPath.setLine(0.0, -self.margin, 0.0, self.margin * 2)
  def drawGPath(self, gPath, gPoint):
    rate = 1000
    gPath.scaleY([0, 2], [0, 1])
    gPath.scaleX([0, 2], [0, 1000])
    nextPoint = QtCore.QPointF(gPath.x, gPath.y)
    line = self.graphScene.addLine(QtCore.QLineF(self.graphPoint, nextPoint), pen = self.gPathPen)
    line.setLine(0.0, line.line().y1(), line.line().dx(), line.line().y2())
    self.lineGroup.moveBy(-line.line().dx(), 0)
    self.lineGroup.addToGroup(line)
    self.graphPoint = nextPoint


    self.linesList.append(line)

    self.linesList = self.removeLine(self.linesList)

    gPoint.scaleY([0, 2], [0, 1])
    gPoint.scaleX([0, 2], [0, 1])

    self.gLine.setLine(0, gPoint.y, gPoint.x, gPoint.y)
    self.oLine.setLine(0, 0, gPoint.x, gPoint.y)
    self.fText.setText(str(gPoint))

  def removeLine(self, lineArr):
    if(len(lineArr) == 0): 
      return lineArr
    line = lineArr[0]
    r = QtCore.QRectF(self.window.rect())

    if(not r.contains(line.scenePos().x(), line.scenePos().y())):
      self.lineGroup.removeFromGroup(line)
      self.graphScene.removeItem(line)
      return self.removeLine(lineArr[1:])
    return lineArr

  def drawSelected(self):
    self.selectedCircle.setRect(self.circlesList[self.selected].rect())
  # newCirclesList, self.textList
  def drawOutline(self, newList, oldList):
    nl = len(newList) #newList length
    ol = len(oldList) #oldList length
    self.margin = 0
    for i in range(nl):
      c = newList[i]; #circle
      x = c.x - c.r / 2
      y = -c.y - c.r / 2 # - c.y because canvas reverse y
      self.margin += c.r / 2
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
      y = -c.y - style.pointW / 2 # - c.y because canvas reverse y
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
