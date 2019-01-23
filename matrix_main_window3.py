from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import numpy as np


import multy_matrix_window2
import matrix_logic
#import matrix_output_widget
import sys


class MatrixMainWindow(QtWidgets.QMainWindow, multy_matrix_window2.Ui_matrix_main_window3 ):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.noize_ = 1
        self.x_dim = 400
        self.y_dim = 400
        self.frames = 200
        self.vel = np.ones(shape=(4))
        self.nx = np.ones(shape=(4))
        self.ny = np.ones(shape=(4))
        self.sigma = 20 * np.ones(shape=(4))
        self.intensity = 5 * np.ones(shape=(4))
        self.matr_log = matrix_logic.MatrixLogic()


    def set_v1(self):
        self.vel[0] = self.v1.value()

    def set_v2(self):
        self.vel[1] = self.v2.value()

    def set_v3(self):
        self.vel[2] = self.v3.value()

    def set_v4(self):
        self.vel[3] = self.v4.value()

    def set_nx1(self):
        self.nx[0] = self.nx1.value()

    def set_nx2(self):
        self.nx[1] = self.nx2.value()

    def set_nx3(self):
        self.nx[2] = self.nx3.value()

    def set_nx4(self):
        self.nx[0] = self.nx4.value()

    def set_ny1(self):
        self.ny[0] = self.ny1.value()

    def set_ny2(self):
        self.ny[1] = self.ny2.value()

    def set_ny3(self):
        self.ny[2] = self.ny3.value()

    def set_ny4(self):
        self.ny[0] = self.ny4.value()

    def set_sigma1(self):
        self.sigma[0] = self.sigma1.value()

    def set_sigma2(self):
        self.sigma[1] = self.sigma2.value()

    def set_sigma3(self):
        self.sigma[2] = self.sigma3.value()

    def set_sigma4(self):
        self.sigma[3] = self.sigma4.value()

    def set_intens1(self):
        self.intensity[0] = self.intens1.value()

    def set_intens2(self):
        self.intensity[1] = self.intens2.value()

    def set_intens3(self):
        self.intensity[2] = self.intens3.value()

    def set_intens4(self):
        self.intensity[3] = self.intens4.value()

    def set_frms(self):
        self.frames = self.frms.value()

    def set_xdim(self):
        self.x_dim = self.xdim.value()

    def set_ydim(self):
        self.y_dim = self.ydim.value()

    def set_noize(self):
        self.noize_ = self.noize.value()

    def run_button(self):
        self.matr_log.play = True
        self.matr_log.complex_matrix_out2(self.x_dim, self.y_dim, self.vel, self.nx, self.ny, self.sigma, self.intensity, self.frames, self.noize_, self .matrix_widget)

    def pause(self):
        self.matr_log.play = not self.matr_log.play

    def next(self):
        self.matr_log.i += 1

    def prev(self):
        self.matr_log.i -= 1


if __name__ == '__main__':


    ###################################
    #sys._excepthook = sys.excepthook
    #def exception_hook(exctype, value, traceback):
        #sys._excepthook(exctype, value, traceback)
        #sys.exit(1)
    #sys.excepthook = exception_hook
    ######################################
    app = QApplication(sys.argv)
    mmw = MatrixMainWindow()
    mmw.show()
    #mmw.matrix_widget.complex_matrix_out(3,2,50,5)

    app.exec_()