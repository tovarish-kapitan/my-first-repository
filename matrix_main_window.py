from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication


import qt_matrix
import matrix_output_widget
import sys


class MatrixMainWindow(QtWidgets.QMainWindow, qt_matrix.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.sigma = 50
        self.intensity = 10
        self.nx = 1
        self.ny = 1
        self.frames = 50
        self.xdim = 500
        self.ydim = 500
        self.nx_box.valueChanged.connect(self.change_nx)
        self.ny_box.valueChanged.connect(self.change_ny)
        self.frames_slider.valueChanged.connect(self.set_frames)
        self.xdim_box.valueChanged.connect(self.set_xdim)
        self.ydim_box.valueChanged.connect(self.set_ydim)
        self.sigma_slider.valueChanged.connect(self.change_sigma)
        self.intense_slider.valueChanged.connect(self.change_intensity)
        self.run_btn.clicked.connect(self.run_matrix)

    def change_nx(self):
        self.nx = self.nx_box.value()

    def change_ny(self):
        self.ny = self.ny_box.value()

    def change_sigma(self):
        self.sigma = self.sigma_slider.value()

    def change_intensity(self):
        self.intensity = self.intense_slider.value()

    def set_frames(self):
        self.frames = self.frames_slider.value()

    def set_xdim(self):
        self.xdim = self.xdim_box.value()

    def set_ydim(self):
        self.ydim = self.ydim_box.value()

    def run_matrix(self):
        self.matrix_widget.complex_matrix_out2(self.xdim, self.ydim, self.nx, self.ny, self.sigma, self.intensity, self.frames)


if __name__ == '__main__':


    ###################################
    sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook
    ######################################


    app = QApplication(sys.argv)
    mmw = MatrixMainWindow()
    mmw.show()
    #print(mmw.nxbox.value)

    #mmw.matrix_widget.complex_matrix_out(3,2,50,5)

    app.exec_()