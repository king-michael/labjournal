import sys
import time

from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton
# usefull links:
# https://stackoverflow.com/questions/6783194/background-thread-with-qthread-in-pyqt


class SimpleThread(QThread):

    send_data = pyqtSignal('int')

    def run(self):
        count = 0
        while count < 5:
            time.sleep(1)
            print("A Increasing")
            count += 1
            self.send_data.emit(count)
        print('finished')

    def __del__(self):
        self.exiting = True
        self.wait()

class test_main_thread(QWidget):
    def __init__(self):
        super(self.__class__, self).__init__()

        layout = QtWidgets.QHBoxLayout()

        btn = QtWidgets.QPushButton("Start counter")
        btn.clicked.connect(self.do_counting)
        layout.addWidget(btn)

        self.setLayout(layout)

    def do_counting(self):
        thread = SimpleThread()
        thread.send_data.connect(self.report_work)
        thread.finished.connect(self.finished_tread)
        thread.start()

    def report_work(self, count):
        print(count)

    def finished_tread(self):
        print('Thread finished')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = test_main_thread()
    window.show()
    sys.exit(app.exec_())