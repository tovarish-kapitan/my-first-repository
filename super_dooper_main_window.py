from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication


import qt_design_wind
import matrix_output_widget
import sys


class SuperDooperMainWindow(QtWidgets.QMainWindow, qt_design_wind.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':


    ###################################
    sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook
    ######################################


    app = QApplication(sys.argv)
    sdmw = SuperDooperMainWindow()
    mw = matrix_output_widget.MatrixWidget()
    sdmw.show()

    sdmw.matrix_widget.complex_matrix_out(2,3,50,10)

    # mw.show()
    # mw.complexMatrixOut()
    app.exec_()