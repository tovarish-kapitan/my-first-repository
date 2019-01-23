from PyQt5.QtWidgets import QWidget
from pyqtgraph.Qt import QtCore, QtGui
from PyQt5.QtCore import QRectF
import numpy as np
from matplotlib import cm
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
from scipy import ndimage, misc
import pathlib
import complex_matrix_generator2
import custom_graph


class MatrixWidget(pg.GraphicsLayoutWidget):

    def __init__(self, parent=None):
        self.Rmin = 0
        self.Rmax = 1500
        self.Vmin = -750
        self.Vmax = 750
        self.RRange = self.Rmax - self.Rmin
        self.VRange = self.Vmax - self.Vmin
        self.xdim = 0
        self.ydim = 0
        self.noize = 0
        self.data = None
        self.texts = custom_graph.CustomGraph()
        self.item = pg.ImageItem()
        self.i = None
        self.mass_centers = pg.GraphItem()
        self.fps = None
        self.updateTime = None
        colormap = cm.get_cmap("plasma")
        colormap._init()
        self.lut = (colormap._lut * 255).view(np.ndarray)
        super().__init__(parent)
        self.initUI()


    def initUI(self):

        view = self.addViewBox(0, 1)
        view.setAspectLocked(True)
        view.addItem(self.item)
        xAxis = pg.AxisItem(orientation='bottom', linkView=view)
        xAxis.setLabel('V, m/s', color='#2E2EFE')
        self.addItem(xAxis, 1, 1)
        yAxis = pg.AxisItem(orientation='left', linkView=view)
        yAxis.setLabel('R, m', color='#2E2EFE')
        self.addItem(yAxis, 0,0)
        view.addItem(self.texts)
        self.item.setLookupTable(self.lut)
        view.setRange(QRectF(self.Vmin, self.Rmin, self.VRange , self.RRange))


    def set_data(self, in_array_data):
        frame = abs(in_array_data)
        self.item.setImage(frame)
        self.item.setRect(QRectF(self.Vmin, self.Rmin, self.VRange , self.RRange))
        frame = (abs(in_array_data) - 2*self.noize) * np.heaviside((abs(in_array_data) - 2*self.noize),0)
        #frame = frame.astype(int)
        frame = ndimage.binary_opening(frame, structure=np.ones((3, 3))).astype(int)
        labeled_array, lab_num = ndimage.label(frame)
        pos = []
        symbols = []
        sizes = []
        texts = []
        for i in range(lab_num):
            (xcm, ycm) = (ndimage.measurements.center_of_mass(labeled_array == i + 1))
            xcm = xcm * (self.VRange / self.xdim) + self.Vmin
            ycm = ycm * (self.RRange / self.ydim) + self.Rmin
            slices =  ndimage.find_objects(labeled_array == i + 1)
            pos.append([xcm, ycm])
            symbols.append('s')
            sizes.append(self.val_from_slice(slices[0]))
            texts.append('target %s\n V=%3d R=%3d' % (i, xcm, ycm))
        pos = np.asarray(pos)
        self.mass_centers.setData(pos=pos, symbolPen=(255,0,0,255), symbolBrush=(255,0,0,255), size=10, symbol='+')
        self.texts.setData(pos=pos, symbolPen='g', symbolBrush=None, size=sizes, symbol=symbols, text=texts, pxMode=False)


    def set_param(self, xdim, ydim, noize):
        self.xdim = xdim
        self.ydim = ydim
        self.noize = noize


    def val_from_slice(self, tup):
        return (self.slice_bouds(tup[0]) * (self.VRange / self.xdim) +
                self.slice_bouds(tup[1]) * (self.RRange / self.ydim)) / 2


    def slice_bouds(self, slice_):
        return slice_.stop - slice_.start


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