from PyQt4 import QtGui, QtCore

class Buttons(QtGui.QWidget):
  def __init__(self, circleSync, countSync, globalSync, reset, parent = None):
    QtGui.QWidget.__init__(self, parent)

    self.circleSync = circleSync
    self.countSync = countSync
    self.globalSync = globalSync
    self.reset = reset

    self.circlePlus = QtGui.QPushButton('+')
    self.circleMinus = QtGui.QPushButton('-')
    self.resetView = QtGui.QPushButton('reset view')
    self.circleSelect = QtGui.QComboBox()
    self.showCheckbox = QtGui.QCheckBox()
    self.radiusLine = QtGui.QLineEdit()
    self.frequencyLine = QtGui.QLineEdit()
    self.phaseLine = QtGui.QLineEdit()
    self.animationSpeedSlowLine = QtGui.QLineEdit()

    self.hbox = QtGui.QHBoxLayout()

    #add widget
    self.hbox.addWidget(self.circlePlus)
    self.hbox.addWidget(self.circleMinus)
    self.hbox.addWidget(self.resetView)
    self.hbox.addWidget(self.circleSelect)
    self.hbox.addWidget(self.showCheckbox)
    self.hbox.addWidget(self.radiusLine)
    self.hbox.addWidget(self.frequencyLine)
    self.hbox.addWidget(self.phaseLine)
    self.hbox.addWidget(self.animationSpeedSlowLine)

    #events
    self.connect(self.circlePlus, QtCore.SIGNAL('clicked()'), self.on_circlePlus)
    self.connect(self.circleMinus, QtCore.SIGNAL('clicked()'), self.on_circleMinus)
    self.connect(self.resetView, QtCore.SIGNAL('clicked()'), self.on_resetView)
    self.connect(self.circleSelect, QtCore.SIGNAL('currentIndexChanged(int)'), self.on_circleSelectChanged)
    self.connect(self.showCheckbox, QtCore.SIGNAL('toggled(bool)'), self.on_showCheckboxChanged)
    self.connect(self.radiusLine, QtCore.SIGNAL('textChanged(const QString&)'), self.on_radiusLineChanged)
    self.connect(self.frequencyLine, QtCore.SIGNAL('textChanged(const QString&)'), self.on_frequencyLineChanged)
    self.connect(self.phaseLine, QtCore.SIGNAL('textChanged(const QString&)'), self.on_phaseLineChanged)
    self.connect(self.animationSpeedSlowLine, QtCore.SIGNAL('textChanged(const QString&)'), self.on_animationSpeedSlowLineChanged)

    #defalut
    #radius validation
    self.radiusLine.setValidator(QtGui.QDoubleValidator())
    #frequency validation
    self.frequencyLine.setValidator(QtGui.QDoubleValidator())
    #phase validation
    self.phaseLine.setValidator(QtGui.QDoubleValidator())
    #speed animation validation
    self.animationSpeedSlowLine.setValidator(QtGui.QDoubleValidator())

    #layout
    self.setLayout(self.hbox)

  def isFieldCorrect(self, value):
    try:
        float(value)
    except ValueError as err:
        print("error:", err)
        return False
    else:
        return True

  def circleValueChanged(self):
    if not self.isFieldCorrect(self.radiusLine.text()):
      return
    if not self.isFieldCorrect(self.frequencyLine.text()):
      return
    if not self.isFieldCorrect(self.phaseLine.text()):
      return

    self.circleSync(self.circleSelect.currentIndex(), self.radiusLine.text(), self.frequencyLine.text(), self.phaseLine.text())
  def countValueChanged(self):
      self.countSync(self.circleSelect.count())
  def globalValueChanged(self):
      if not self.isFieldCorrect(self.animationSpeedSlowLine.text()) or int(self.animationSpeedSlowLine.text()) is 0:
        return
      self.globalSync(self.circleSelect.currentIndex(), self.showCheckbox.isChecked(), self.animationSpeedSlowLine.text())
  def setGlobalValue(self, index, show, animationSpeedSlow):
    while(self.circleSelect.count() <= index):
      self.circleSelect.addItem(str(self.circleSelect.count()))

    self.circleSelect.setCurrentIndex(index)
    self.showCheckbox.setChecked(show)
    self.animationSpeedSlowLine.setText(str(animationSpeedSlow))


  #circle change
  def on_radiusLineChanged(self, string):
      if(len(string) == 0):
        return
      self.circleValueChanged()
  def on_frequencyLineChanged(self, string):
      self.circleValueChanged()
  def on_phaseLineChanged(self, string):
      self.circleValueChanged()

  def setCircleData(self, radius, frequency, phase = 0):
      self.radiusLine.setText(str(radius))
      self.frequencyLine.setText(str(frequency))
      self.phaseLine.setText(str(phase))

  #count change
  def on_circlePlus(self):
    self.circleSelect.addItem(str(self.circleSelect.count()))
    self.countValueChanged()
  def on_circleMinus(self):
    if(self.circleSelect.count() == 1):
      print('value must be less then one')
    else:
      self.circleSelect.removeItem(self.circleSelect.count() - 1)
      self.countValueChanged()

  #global change
  def on_circleSelectChanged(self):
      self.globalValueChanged()
  def on_showCheckboxChanged(self, b):
      self.globalValueChanged()
  def on_animationSpeedSlowLineChanged(self, string):
      self.globalValueChanged()
  #reset
  def on_resetView(self):
      self.reset()
