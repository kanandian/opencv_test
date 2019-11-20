import component
import sys
from PyQt5.QtWidgets import QApplication

def main():
    app = 0
    app = QApplication(sys.argv)
    application = component.ApplicationByPyqt()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



# import sys
# import time
# from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel
# from PyQt5.QtGui import QPalette, QBrush, QPixmap
# import _thread
#
# app = QApplication(sys.argv)
#
#
#
# class MWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.label = QLabel(self)
#         self.initUI()
#
#     def initUI(self):
#         pix = QPixmap('images/yezi.png')
#         self.label.setGeometry(0,0,300,200)
#         self.label.setPixmap(pix)
#
#     def move_leaf(self):
#         i = 0
#         while True:
#             self.label.move(0, i)
#             i += 10
#             time.sleep(1)
#
#
#
#
#
#
# w = MWidget()
# w.resize(1920, 1080)
# w.move(0, 0)
# w.setWindowTitle('Simple')
# w.show()
#
#
#
# sys.exit(app.exec_())
#
#
#
