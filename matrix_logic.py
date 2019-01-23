from PyQt5.QtWidgets import QWidget
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtCore import Qt, QRectF, QTimer
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import pathlib
import complex_matrix_generator2


class MatrixLogic:

    def __init__(self):
        self.play = True
        self.frames = 50
        self.xdim = 600
        self.ydim = 600
        self.noize = 1
        self.data = None
        self.i = None
        self.fps = None
        self.wid = None
        self.updateTime = None


    def updateData(self):
        self.wid.set_data(self.data[:,:,self.i%(self.frames-1)])
        if self.play == True:
            self.i = self.i + 1
        QTimer.singleShot(1, self.updateData)
        now = ptime.time()
        self.fps = 1 / (now - self.updateTime)
        print("fps =", self.fps)
        self.updateTime = now


    def complex_matrix_out2(self, xdim, ydim, vel, nx, ny, sigma, intensity, frames, noize, wid):
        #self.frames = complex_matrix_generator2.OurMatrix2(xdim, ydim, vel, nx,ny, sigma, intensity,fr).data
        npzfile = self.np_ziping(xdim, ydim, vel, nx, ny, sigma, intensity, frames, noize)
        self.data = npzfile['arr_0']
        self.frames = frames
        self.xdim = xdim
        self.ydim = ydim
        self.updateTime = ptime.time()
        self.wid = wid
        self.i = 0
        self.fps = 0
        self.noize = noize
        self.wid.set_param(self.xdim, self.ydim, self.noize)
        self.updateData()


    def generate_name(self, xdim, ydim, vel, nx, ny, sigma, intensity, frames, noize):
        infa = [xdim, ydim, frames, noize] + vel.astype(int).tolist() + nx.astype(int).tolist()+ ny.astype(int).tolist()\
               + sigma.astype(int).tolist() + intensity.astype(int).tolist()
        name = ''
        for i in range(len(infa)):
            name = name + str(infa[i]) + '_'
        return name


    def np_ziping(self, xdim, ydim, vel, nx, ny, sigma, intensity, frames, noize):
        pathlib.Path('matrix_saves').mkdir(parents=True, exist_ok=True)
        name = self.generate_name(xdim, ydim, vel, nx, ny, sigma, intensity, frames, noize)
        try:
            data = open('matrix_saves/%s' % name, 'br')
            npzfile = np.load(data)
        except FileNotFoundError:
            data = open('matrix_saves/%s' % name, 'bw')
            dat = complex_matrix_generator2.OurMatrix2(xdim, ydim, vel, nx,ny, sigma, intensity, frames, noize).data
            np.savez(data, dat)
            data.seek(0)  # Only needed here to simulate closing & reopening file
            data = open('matrix_saves/%s' % name, 'br')
            npzfile = np.load(data)
        return npzfile


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
    mw = MatrixLogic()
    print(mw.play)
    #name = mw.generate_name(200, 200, 1 [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [10, 10, 10, 10], [10, 10, 10, 10], 50)
    #print(name)
    #mw.complex_matrix_out2(200, 200, [1,1,1,1], [1,1,1,1],[1,1,1,1],[10,10,10,10],[10,10,10,10], 50)
    #mw.show()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()