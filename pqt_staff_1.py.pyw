import sys
from PyQt5.QtWidgets import qApp, QWidget, QPushButton, QApplication, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
class MyWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.label = QLabel("Здравствуйте")
        self.label.setAlignment(Qt.AlignHCenter)
        self.btnQuit = QPushButton("&Закрой окно")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.btnQuit)
        self.setLayout(self.vbox)
        self.btnQuit.clicked.connect(qApp.quit)#кнопка, которая должна закрывать окно, но неделает этого#

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("название")
    window.resize(300,100)
    window.show()
    sys.exit(app.exec_())

