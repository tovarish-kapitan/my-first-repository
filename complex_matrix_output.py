from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import complex_matrix_generator #будет сгенерирован массив комплексных матриц, модули которых 
# будут использованы как данные для выводимых изображений

app = QtGui.QApplication([])

## Create window with GraphicsView widget
win = pg.GraphicsLayoutWidget()
win.show()  ## show widget alone in its own window
win.setWindowTitle('Ждем, пока генерируются наши матрицы')
view = win.addViewBox()

## lock the aspect ratio so pixels are always square
view.setAspectLocked(True)

## Create image item
img = pg.ImageItem(border='w')
view.addItem(img)

## Set initial view bounds
view.setRange(QtCore.QRectF(0, 0, 600, 600))
i = 0
updateTime = ptime.time()
Source=complex_matrix_generator.OurMatrix(600,600,62)#создаем массив из 62 комплексных матриц 600х600
fps=0

def updateData():
    global img, i, updateTime, fps

    ## Display the data
    img.setImage(abs(Source.Data[:,:,i%61]))# циклично выводим модуль iй матрицы
    QtCore.QTimer.singleShot(1, updateData)
    now = ptime.time()
    fps=1/(now-updateTime)
    print("fps =",fps)
    updateTime = now
    i = i+1

updateData()
win.setWindowTitle('Дождались')

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

