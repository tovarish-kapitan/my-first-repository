from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QVBoxLayout
import queue

class MyThread(QThread) :
    task_done = pyqtSignal(int, int, name = 'tastDone')
    def __init__(self, id, queue, parent=None):
        QThread.__init__(self, parent)
        self.id = id
        self.queue = queue
    def run(self):
        while True:
            task = self.queue.get()
            self.sleep(1)
            self.task_done.emit(task, self.id)
            self.queue.task_done()

class MyWindow(QPushButton):
    def __init__(self):
        QPushButton.__init__(self)
        self.setText("приступай")
        self.queue = queue.Queue()
        self.threads = []
        for i in range(1, 3):
            thread = MyThread(i, self.queue)
            self.threads.append(thread)
            thread.task_done.connect(self.on_task_done, Qt.QueuedConnection)
            thread.start()
        self.clicked.connect(self.on_add_task)
    def on_add_task(self):
        for i in range(0, 11):
            self.queue.put(i)
    def on_task_done(self, data, id):
        print(data, "- id =", id)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("оприходуем QThread")
    window.resize(300, 70)
    window.show()
    sys.exit(app.exec_())        
        
        
        


        
