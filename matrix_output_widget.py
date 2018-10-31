from PyQt5.QtWidgets import QWidget
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtCore import Qt, QRectF, QTimer
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import complex_matrix_generator

class MatrixWidget(pg.GraphicsLayoutWidget):

    def __init__(self):
        self.img = pg.ImageItem()
        self.i = None
        self.fps = None
        self.updateTime = None
        self.frames = []
        super().__init__()
        self.initUI()

    def initUI(self):
        view = self.addViewBox()
        view.setAspectLocked(True)
        view.addItem(self.img)
        view.setRange(QRectF(0, 0, 600, 600))

    def updateData(self): 
        (self.img).setImage(abs(self.frames[:, :, (self.i) % 61]))# циклично выводим модуль iй матрицы
        QTimer.singleShot(1, self.updateData)
        now = ptime.time()
        self.fps = 1 / (now - self.updateTime)
        print("fps =", self.fps)
        self.updateTime = now
        self.i = self.i + 1

    def complexMatrixOut(self):
        self.frames = complex_matrix_generator.OurMatrix(600,600,62,50).Data
        self.updateTime = ptime.time()
        self.i = 0
        self.fps = 0
        self.updateData()
        

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    mw = MatrixWidget()
    mw.show()
    mw.complexMatrixOut()
       
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

