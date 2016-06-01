class Circle():
  def __init__(self, radius = 1, frequency = 440, phase = 0):
    self.radius = radius
    self.frequency = frequency
    self.phase = phase
  def setData(self, radius, frequency, phase):
    self.radius = radius
    self.frequency = frequency
    self.phase = phase
  def getData(self):
    return self.radius, self.frequency, self.phase

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
    print(count, len(self.circlesList))
    if(count >= len(self.circlesList)):
      self.circlesList.append(Circle())
    else:
      self.circlesList = self.circlesList[0:len(self.circlesList) - 1]

