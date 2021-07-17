import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 300)
        self.setWindowTitle('MyApp')

        self.label = QLabel(self)
        self.label.setGeometry(0,0,200,200)
        self.show()

    #키를 누를 때
    def keyPressEvent(self, event):
        key = event.key()
        self.label.setText(str(key)+'press')

    #키를 뗄 때
    def keyReleaseEvent(self, event):
        key = event.key()
        self.label.setText(str(key)+'release')


if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = MyApp()
   sys.exit(app.exec_())