#04.pyat key event.py
#pyqt 키 이벤트
import sys
from PyQt5.QtWidgets import QApplication, QWidget

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle('MyApp')
        self.show()

    #키를 누를 때
    def keyPressEvent(self, event):
        key = event.key()
        print(str(key) + 'press')

    #키를 뗄 때
    def keyReleaseEvent(self, event):
        key = event.key()
        print(str(key) + 'release')


if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = MyApp()
   sys.exit(app.exec_())