from PyQt4 import QtCore
import math

PI = math.pi

def getScale(sD, sR):
    return (sR[1] -sR[0]) / (sD[1] - sD[0])

class Circle:
    def __init__(self, i, theta, RList, FList, PList):

        self.theta = theta

        self.FList = FList
        self.PList = PList
        self.RList = RList
        self.fX = self.FT(RList, i, PI / 2)
        self.fY = self.FT(RList, i, PI * 2)
        self.r = RList[i]
        self.phase = PList[i]
    def __str__(self):
        string = ''
        result = []
        for i in range(len(self.RList)):
          string = "{0} * sin({1} * n + {2})".format(int(self.RList[i]),int(self.FList[i]), self.PList[i])
          if(i >= 3 and i % 3 == 0):
            string  += '\n'
          result.append(string)
        return 'y = ' + ' + '.join(result)
    # public
    def scaleX(self, scaleDomain, scaleRange, start = 0):
        self.x = self.fX(self.theta) * getScale(scaleDomain, scaleRange) + start

    def scaleY(self, scaleDomain, scaleRange, start = 0):
        self.y = self.fY(self.theta) * getScale(scaleDomain, scaleRange) - start
    # private
    def FT(self, A, N, f):
        def inner(x):
            n = 0
            y = 0
            while n < N:
                y += A[n] * math.sin(self.FList[n] * x + (f + self.PList[n]))
                n += 1
            return y
        return inner

class GPath(Circle):
    def __init__(self, i, theta, RList, FList, PList):
        Circle.__init__(self, i, theta, RList, FList, PList)
        self.fX = self.zero()
    # public
    def zero(self):
        def inner(x):
            return x;
        return inner
    def getRange(self, r):
        result = []
        for i in range(r):
            result.append( QtCore.QPointF(self.x, -self.y))
        return result
    # private


class MathLogic():
    @staticmethod
    def getCoords(theta, circlesList):
        r = [circle.getFRadius() for circle in circlesList]
        f = [circle.getAngularFrequency() for circle in circlesList]
        p = [circle.getRadianPhase() for circle in circlesList]

        return [Circle(i, theta, r,f, p) for i in range(len(r))]
    @staticmethod
    def getGPath(theta, circlesList):
        r = [circle.getFRadius() for circle in circlesList]
        f = [circle.getAngularFrequency() for circle in circlesList]
        p = [circle.getRadianPhase() for circle in circlesList]
        return GPath(len(r) - 1, theta, r, f, p)
    @staticmethod
    def getGPoint(theta, circlesList):
        r = [circle.getFRadius() for circle in circlesList]
        f = [circle.getAngularFrequency() for circle in circlesList]
        p = [circle.getRadianPhase() for circle in circlesList]
        return Circle(len(r) - 1, theta, r, f, p)

