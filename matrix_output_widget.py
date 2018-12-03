from PyQt5.QtWidgets import QWidget
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtCore import Qt, QRectF, QTimer
import numpy as np
from matplotlib import cm
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
from scipy import ndimage, misc
import pathlib
#import complex_matrix_generator
import complex_matrix_generator2
import custom_graph


class MatrixWidget(pg.GraphicsLayoutWidget):

    def __init__(self, parent=None):
        self.play = True
        self.frames = 50
        self.xdim = 600
        self.ydim = 600
        self.noize = 1
        self.data = None
        self.text = custom_graph.CustomGraph()
        self.item = pg.ImageItem()
        self.i = None
        self.mass_centers = pg.GraphItem()
        self.fps = None
        self.updateTime = None
        #self.pos = np.linspace(0, 1, 256)
        #n = len(self.pos)
        #self.color = []
        #for i in range(n):
        #    self.color.append([((n-i)/n), (i/n), ((n-i)/n), 1])
        #self.colmap = pg.ColorMap(self.pos, self.color)
        #self.lut = self.colmap.getLookupTable(0, 1.0, 256)
        colormap = cm.get_cmap("plasma")  # cm.get_cmap("CMRmap")
        colormap._init()
        self.lut = (colormap._lut * 255).view(np.ndarray)
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        view = self.addViewBox()
        view.setAspectLocked(True)
        view.addItem(self.item)
        view.addItem(self.mass_centers)
        view.addItem(self.text)
        self.item.setLookupTable(self.lut)
        self.item.setLevels([0, 1])
        view.setRange(QRectF(0, 0, self.xdim, self.ydim))

    def updateData(self):
        self.set_data(self.data[:,:,self.i%(self.frames-1)])
        if self.play == True:
            self.i = self.i + 1
        QTimer.singleShot(1, self.updateData)
        now = ptime.time()
        self.fps = 1 / (now - self.updateTime)
        print("fps =", self.fps)
        self.updateTime = now

    def set_data(self, in_array_data):
        frame = abs(in_array_data)
        (self.item).setImage(frame)
        frame = (abs(in_array_data) - 2*self.noize) * np.heaviside((abs(in_array_data) - 2*self.noize),0)
        #frame = frame.astype(int)
        frame = ndimage.binary_opening(frame, structure=np.ones((2, 2))).astype(int)
        labeled_array, lab_num = ndimage.label(frame)
        pos = []
        symbols = []
        sizes = []
        texts = []
        for i in range(lab_num):
            (xcm, ycm) = ndimage.measurements.center_of_mass(labeled_array == i + 1)
            slices =  ndimage.find_objects(labeled_array == i + 1)
            pos.append([xcm, ycm])
            symbols.append('s')
            sizes.append(self.val_from_slice(slices[0]))
            texts.append('target %s\n %3d %3d' % (i, xcm, ycm))
        pos = np.asarray(pos)
        self.text.setData(pos=pos, symbolPen='g', symbolBrush=None, size=sizes, symbol=symbols, text=texts, pxMode=False)
        #self.text.setText('target')
        #self.text.setPos(xcm,ycm)

    def val_from_slice(self, tup):
        return (self.slice_bouds(tup[0]) + self.slice_bouds(tup[1])) / 2

    def slice_bouds(self, slice_):
        return slice_.stop - slice_.start

    #def complex_matrix_out(self, xdim, ydim, nx, ny, sigma, intensity, frames):
        #self.frames = complex_matrix_generator.OurMatrix(xdim,ydim, nx, ny, sigma, intensity, frames).data
        #self.frames = frames
        #self.xdim = xdim
        #self.ydim = ydim
        #self.updateTime = ptime.time()
        #self.i = 0
        #self.fps = 0
        #self.updateData()

    def complex_matrix_out2(self, xdim, ydim, vel, nx, ny, sigma, intensity, frames, noize):
        #self.frames = complex_matrix_generator2.OurMatrix2(xdim, ydim, vel, nx,ny, sigma, intensity,fr).data
        npzfile = self.np_ziping(xdim, ydim, vel, nx, ny, sigma, intensity, frames, noize)
        self.data = npzfile['arr_0']
        self.frames = frames
        self.xdim = xdim
        self.ydim = ydim
        self.updateTime = ptime.time()
        self.i = 0
        self.fps = 0
        self.noize = noize
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
    mw = MatrixWidget()
    #name = mw.generate_name(200, 200, 1 [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [10, 10, 10, 10], [10, 10, 10, 10], 50)
    #print(name)
    #mw.complex_matrix_out2(200, 200, [1,1,1,1], [1,1,1,1],[1,1,1,1],[10,10,10,10],[10,10,10,10], 50)
    #mw.show()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

