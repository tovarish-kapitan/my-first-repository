import sys
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QPushButton, QWidget
from PyQt5.QtCore import pyqtSlot

class MyWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle("хорошая история просто")
        self.resize(300, 150)
        self.button1 = QPushButton("отжимайся")
        self.button2 = QPushButton("обманка")
        self.button3 = QPushButton("залезай")
        self.button4 = QPushButton("уничтожить")
        self.button3.setEnabled(False)
        vbox = QVBoxLayout()
        vbox.addWidget(self.button1)
        vbox.addWidget(self.button2)
        vbox.addWidget(self.button3)
        vbox.addWidget(self.button4)
        self.setLayout(vbox)
        self.button1.clicked.connect(self.on_clicked_button1)
        self.button2.clicked.connect(self.on_clicked_button2)
        self.button3.clicked.connect(self.on_clicked_button3)
        self.button4.clicked.connect(self.on_clicked_button4)
    @pyqtSlot()
    def on_clicked_button1(self):
        print("раз раз")
    @pyqtSlot()
    def on_clicked_button2(self):    
        self.button1.blockSignals(True)
        self.button2.setEnabled(False)
        self.button3.setEnabled(True)
    @pyqtSlot()
    def on_clicked_button3(self):
        self.button1.blockSignals(False)
        self.button2.setEnabled(True)
        self.button3.setEnabled(False)
    @pyqtSlot()
    def on_clicked_button4(self):
        self.button1.clicked.disconnect(self.on_clicked_button1)
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
