import math
PI = math.pi

class Circle():
  def __init__(self, radius = 100, frequency = 2, phase = 0):
    self.radius = radius
    self.frequency = frequency
    self.phase = phase

  def setData(self, radius, frequency, phase):
    self.radius = radius
    self.frequency = frequency
    self.phase = phase
    self.selected = True

  def getData(self):
    return self.radius, self.frequency, self.phase
  def getFRadius(self):
    return float(self.radius)
  def getFFrequency(self):
    return float(self.frequency)
  def getAngularFrequency(self):
      return PI * 2 * float(self.frequency)
  def getFPhase(self):
    return float(self.phase)
  def getRadianPhase(self):
    if (float(self.phase) == 0.0):
      return 0.0
    else:
      return (float(self.phase) / 180) * PI

class ControllersData():
  def __init__(self):
    self.circlesList = [Circle()]
  def setData(self, index, radius, frequency, phase):
    self.circlesList[index].setData(radius, frequency, phase)
  def getDataIndex(self, index):
    return self.circlesList[index].getData()
  def getCirclesList(self):
    return self.circlesList
  def setCirclesCount(self, count):
    if(count >= len(self.circlesList)):
      self.circlesList.append(Circle())
    else:
      self.circlesList = self.circlesList[0:len(self.circlesList) - 1]

