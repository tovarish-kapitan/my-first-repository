#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import sys
from PyQt5.QtWidgets import (QWidget, QLineEdit, QHBoxLayout, QFrame, QSplitter, QStyleFactory, QApplication)
from PyQt5.QtCore import Qt, QRectF, QTimer
import pyqtgraph as pg
import pyqtgraph.ptime as ptime
import complex_matrix_output
import complex_matrix_generator2
 
class Window(QWidget):
    
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
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    matrix = complex_matrix_output.MatrixWidget()
    mw = Window(matrix)
    mw.show()
    matrix.frames = complex_matrix_generator2.OurMatrix(600,600,62,50).Data
    matrix.updateTime = ptime.time()
    matrix.i = 0
    matrix.fps = 0
    matrix.updateData()
    
    
    sys.exit(app.exec_())
