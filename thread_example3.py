from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QVBoxLayout

class Thread1(QThread) :
    s1= pyqtSignal(int)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.count = 0
    def run(self):
        self.exec_()
    def on_start(self):    
            self.count +=1
            self.s1.emit(self.count)

class Thread2(QThread) :
    s2 = pyqtSignal(str)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    def run(self):
        self.exec_()
    def on_change(self, i):
        i += 10
        self.s2.emit("%d" % i)
        
class MyWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.label = QLabel("отжимайся")
        self.label.setAlignment(Qt.AlignHCenter)
        self.button = QPushButton("приступай")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.button)
        self.setLayout(self.vbox)
        self.thread1 = Thread1()
        self.thread2 = Thread2()
        self.thread1.start()
        self.thread2.start()
        self.button.clicked.connect(self.thread1.on_start)
        self.thread1.s1.connect(self.thread2.on_change)
        self.thread2.s2.connect(self.on_thread2_s2)
    def on_thread2_s2(self, s):
        self.label.setText(s)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("оприходуем QThread")
    window.resize(300, 70)
    window.show()
    sys.exit(app.exec_())
        
    
                        
            
