from PyQt5.QtWidgets import QWidget
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtCore import Qt, QRectF, QTimer
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import complex_matrix_generator
import complex_matrix_generator2

class MatrixWidget(pg.GraphicsLayoutWidget):

    def __init__(self, parent=None):
        self.fr = 50
        self.xdim = 600
        self.ydim = 600
        self.frames = None
        self.img = pg.ImageItem()
        self.i = None
        self.fps = None
        self.updateTime = None
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        view = self.addViewBox()
        view.setAspectLocked(True)
        view.addItem(self.img)
        view.setRange(QRectF(0, 0, self.xdim, self.ydim))

    def updateData(self):
        self.set_data(self.frames[:,:,self.i%(self.fr-1)])
        QTimer.singleShot(1, self.updateData)
        now = ptime.time()
        self.fps = 1 / (now - self.updateTime)
        print("fps =", self.fps)
        self.updateTime = now
        self.i = self.i + 1

    def set_data(self, in_array_data):
        (self.img).setImage(abs(in_array_data))


    def complex_matrix_out(self, xdim, ydim, nx, ny, sigma, intensity, fr):
        self.frames = complex_matrix_generator.OurMatrix(xdim,ydim, nx, ny, sigma, intensity, fr).data
        self.fr = fr
        self.xdim = xdim
        self.ydim = ydim
        self.updateTime = ptime.time()
        self.i = 0
        self.fps = 0
        self.updateData()

    def complex_matrix_out2(self, xdim, ydim, nx, ny, sigma, intensity, fr):
        self.frames = complex_matrix_generator2.OurMatrix2(xdim, ydim,nx,ny, sigma, intensity,fr).data
        self.fr = fr
        self.xdim = xdim
        self.ydim = ydim
        self.updateTime = ptime.time()
        self.i = 0
        self.fps = 0
        self.updateData()

if __name__ == '__main__':
    import sys


    ###################################
    sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook
    ######################################

    app = QtGui.QApplication([])
    mw = MatrixWidget()
    mw.show()
    mw.complex_matrix_out()
       
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

