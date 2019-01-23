# -*- coding: utf-8 -*-
"""
Simple example of subclassing GraphItem.
"""

#import initExample  ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np


class CustomGraph(pg.GraphItem):
    def __init__(self):
        self.textItems = []
        self.ind = 0
        pg.GraphItem.__init__(self)

    def setData(self, **kwds):
        self.text = kwds.pop('text', [])
        self.sizes = kwds.get('size')
        self.dat = kwds
        if 'pos' in self.dat:
            npts = self.dat['pos'].shape[0]
            self.dat['dat'] = np.empty(npts, dtype=[('index', int)])
            self.dat['dat']['index'] = np.arange(npts)
        self.setTexts(self.text)
        self.ind = self.ind + 1
        self.updateGraph()

    def setTexts(self, text):
        for i in self.textItems:
            i.scene().removeItem(i)
        self.textItems = []
        for t in text:
            item = pg.TextItem(t)
            self.textItems.append(item)
            item.setParentItem(self)

    def updateGraph(self):
        pg.GraphItem.setData(self, **self.dat)
        for i, item in enumerate(self.textItems):
            item.setPos(*self.dat['pos'][i] + (0,-0.5*self.sizes[i]))




## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    # Enable antialiasing for prettier plots
    pg.setConfigOptions(antialias=True)

    w = pg.GraphicsWindow()
    w.setWindowTitle('pyqtgraph example: CustomGraphItem')
    v = w.addViewBox()
    v.setAspectLocked()

    g = CustomGraph()
    v.addItem(g)

    ## Define positions of nodes
    pos =np.array([[0, 0],
        [10, 0],
        [0, 10],
        [10, 10],
        [5, 5],
        [15, 5]])

    ## Define the set of connections in the graph
    adj = np.array([
        [0, 1],
        [1, 3],
        [3, 2],
        [2, 0],
        [1, 5],
        [3, 5],
    ])

    ## Define the symbol to use for each node (this is optional)
    symbols = ['o', 'o', 'o', 'o', 't', '+']
    sizes = [1, 2, 3, 4, 1, 1]

    ## Define the line style for each connection (this is optional)
    lines = np.array([
        (255, 0, 0, 255, 1),
        (255, 0, 255, 255, 2),
        (255, 0, 255, 255, 3),
        (255, 255, 0, 255, 2),
        (255, 0, 0, 255, 1),
        (255, 255, 255, 255, 4),
    ], dtype=[('red', np.ubyte), ('green', np.ubyte), ('blue', np.ubyte), ('alpha', np.ubyte), ('width', float)])

    ## Define text to show next to each symbol
    texts = ["Point %d" % i for i in range(6)]

    ## Update the graph
    g.setData(pos=pos, adj=adj, pen=lines, size=sizes, symbol=symbols, pxMode=False, text=texts)


    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()