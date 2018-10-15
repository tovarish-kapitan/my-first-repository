from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QVBoxLayout

class MyThread(QThread) :
    mysignal = pyqtSignal(str)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.running = False
        self.count = 0
    def run(self):
        self.running = True
        while self.running:
            self.count +=1
            self.mysignal.emit("count = %s" % self.count)
            self.sleep(1)

class MyWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.label = QLabel("отжимайся")
        self.label.setAlignment(Qt.AlignHCenter)
        self.btnStart = QPushButton("приступай")
        self.btnStop = QPushButton("стоять")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.btnStart)
        self.vbox.addWidget(self.btnStop)
        self.setLayout(self.vbox)
        self.mythread = MyThread()
        self.btnStart.clicked.connect(self.on_start)
        self.btnStop.clicked.connect(self.on_stop)
        self.mythread.mysignal.connect(self.on_change, Qt.QueuedConnection)
    def on_start(self):
        if not self.mythread.isRunning():
            self.mythread.start()
    def on_stop(self):
        self.mythread.running = False
    def on_change(self, s):
        self.label.setText(s)
    def closeEvent(self, event):
        self.hide()
        self.mythread.running = False
        self.mythead.wait(5000)
        event.accept()
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("оприходуем QThread")
    window.resize(300, 70)
    window.show()
    sys.exit(app.exec_())

        
