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
  def drawValue(self, circlesList):
      cl = len(circlesList)
      dtl = self.textList[cl:]
      self.textList = self.textList[0:cl]
      tl = len(self.textList)
      for i in range(cl):
        print(i, cl, len(self.textList))
        circle = circlesList[i]
        values = 'f{0} r{1} p{2}'.format(circle.frequency, circle.radius, circle.phase)
        if(i >= tl):
            t = self.graphScene.addSimpleText(values)
            t.setY(i * 10)
            self.textList.append(t)
        else:
            print (i, cl, len(self.textList))
            self.textList[i].setText(values)

      #removing
      self.removeItems(dtl)

  # circlesList, self.textList
  def drawText(self, newList, oldList):
    nl = len(newList)
    ol = len(oldList)
    for i in range(nl):
      circle = newList[i]
      values = '{0} r{1} p{2}'.format(circle.frequency, circle.radius, circle.phase)
      if(i > ol):
        t = self.graphScene.addSimpleText(values)
        t.setY(i + 15)
        oldList.append(t)
      else:
        oldList[i].setText(values)

  def removeItems(self, circlesList):
    for item in circlesList:
      self.graphScene.removeItem(item)
