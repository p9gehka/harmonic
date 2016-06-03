import math
PI = math.pi


def getScale(sD, sR):
    return (sR[1] -sR[0]) / (sD[1] - sD[0])

class Circle:
    def __init__(self, r, i, theta, FList):
        self.theta = theta
        self.FList = FList
        self.fX = self.FT(r, i, PI / 2)
        self.fY = self.FT(r, i, 0)
        self.r = abs(r[i])
        print(theta)
    # public
    def scaleX(self, scaleDomain, scaleRange):
        self.x = self.fX(self.theta) * getScale(scaleDomain, scaleRange)
    def scaleY(self, scaleDomain, scaleRange):
        self.y = self.fY(self.theta) * getScale(scaleDomain, scaleRange)

    # private
    def FT(self, A, N, f):
        def inner(x):
            n = 0
            y = 0
            while n < N:
                y += A[n] * math.sin(PI * 2 * self.FList[n] * (n + 1) * x + f)
                n += 1
            return y
        return inner

class MathLogic():
    @staticmethod
    def getCoords(theta, circlesList):
        circlesList
        r = [circle.getFRadius() for circle in circlesList]
        f = [circle.getFFrequency() for circle in circlesList]
        return [Circle(r, i, theta, f) for i in range(len(r))]

