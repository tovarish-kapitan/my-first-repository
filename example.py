#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import sys
from PyQt5.QtWidgets import (QWidget, QLineEdit, QHBoxLayout, QFrame, QSplitter, QStyleFactory, QApplication)
from PyQt5.QtCore import Qt, QRectF, QTimer
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import complex_matrix_generator2
 
class MatrixWindow(QWidget):
    
    def __init__(self, mywid):
        super().__init__()
        self.initUI(mywid)
        
    def initUI(self, mywid):      
        hbox = QHBoxLayout(self)

        textbox = QLineEdit(self)  #здесь будет доделана область с настройками
        textbox.move(20, 20)
        textbox.resize(280, 40)
        
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(textbox)
        splitter.addWidget(mywid)
        hbox.addWidget(splitter)
        self.setLayout(hbox)
        self.setGeometry(300, 50, 800, 600)
        self.setWindowTitle('QSplitter')
        
        
    def updateData(self):
        global i, fps, updateTime  #пока не избавились от глобальных переменных 
        img.setImage(abs(Source.Data[:, :, i % 61]))# циклично выводим модуль iй матрицы
        QTimer.singleShot(1, self.updateData)
        now = ptime.time()
        fps=1/(now-updateTime)
        print("fps =", fps)
        updateTime = now
        i = i + 1     
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    matrix = pg.GraphicsLayoutWidget()
    mw = MatrixWindow(matrix)
    
    view = matrix.addViewBox()
    view.setAspectLocked(True)
    img = pg.ImageItem()
    view.addItem(img)
    view.setRange(QRectF(0, 0, 600, 600))
    mw.show()
    Source=complex_matrix_generator2.OurMatrix(600,600,62,50)#создаем массив из 62 комплексных матриц 600х600
    updateTime = ptime.time()
    i = 0
    fps=0
    mw.updateData()
    
    
    sys.exit(app.exec_())
