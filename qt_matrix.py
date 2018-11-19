# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_matrix.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(662, 456)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(0, 10, 641, 401))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.nxbox = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.nxbox.setMinimum(1)
        self.nxbox.setMaximum(5)
        self.nxbox.setObjectName("nxbox")
        self.verticalLayout.addWidget(self.nxbox)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.nybox = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.nybox.setMinimum(1)
        self.nybox.setMaximum(5)
        self.nybox.setObjectName("nybox")
        self.verticalLayout.addWidget(self.nybox)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.sigmaslider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.sigmaslider.setMinimum(10)
        self.sigmaslider.setMaximum(1000)
        self.sigmaslider.setOrientation(QtCore.Qt.Horizontal)
        self.sigmaslider.setObjectName("sigmaslider")
        self.verticalLayout.addWidget(self.sigmaslider)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.intenseslider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.intenseslider.setMinimum(1)
        self.intenseslider.setOrientation(QtCore.Qt.Horizontal)
        self.intenseslider.setObjectName("intenseslider")
        self.verticalLayout.addWidget(self.intenseslider)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.runbtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.runbtn.setObjectName("runbtn")
        self.verticalLayout.addWidget(self.runbtn)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.matrix_widget = MatrixWidget(self.splitter)
        self.matrix_widget.setObjectName("matrix_widget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 662, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">nx</p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">ny</p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">sigma</p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">intensity</p></body></html>"))
        self.runbtn.setText(_translate("MainWindow", "generate and show"))

from matrix_output_widget import MatrixWidget
