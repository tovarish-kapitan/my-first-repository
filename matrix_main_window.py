from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication


import qt_matrix
import matrix_output_widget
import sys


class MatrixMainWindow(QtWidgets.QMainWindow, qt_matrix.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.nx = 1
        self.ny = 1
        self.sigma = 50
        self.intensity = 10
        self.nxbox.valueChanged.connect(self.change_nx)
        self.nybox.valueChanged.connect(self.change_ny)
        self.sigmaslider.valueChanged.connect(self.change_sigma)
        self.intenseslider.valueChanged.connect(self.change_intensity)
        self.runbtn.clicked.connect(self.run_matrix)

    def change_nx(self):
        self.nx = self.nxbox.value()

    def change_ny(self):
        self.ny = self.nybox.value()

    def change_sigma(self):
        self.sigma = self.sigmaslider.value()

    def change_intensity(self):
        self.intensity = self.intenseslider.value()

    def run_matrix(self):
        self.matrix_widget.complex_matrix_out(self.nx,self.ny,self.sigma,self.intensity)


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