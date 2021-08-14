import sys
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 300)
        self.setWindowTitle('GA Mario')
        self.show()

    def paintEvent(self, event):
        # 그리기 도구
        painter = QPainter()
        # 그리기 시작
        painter.begin(self)

        #사각형 그리기
        painter.setPen(QPen(Qt.red, 1.0, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.blue))
        painter.drawRect(0, 0, 50, 50)

        painter.setPen(QPen(Qt.yellow, 1.0, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawRect(50, 0, 50, 50)

        painter.setPen(QPen(Qt.green, 1.0, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawRect(0, 50, 50, 50)

        painter.setPen(QPen(Qt.blue, 1.0, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red))
        painter.drawRect(50, 50, 50, 50)

        #선그리기
        painter.setPen(QPen(Qt.darkRed, 2.0, Qt.SolidLine))
        painter.drawLine(0+25, 130+25, 60+25, 240+25)

        painter.setPen(QPen(Qt.darkYellow, 2.0, Qt.SolidLine))
        painter.drawLine(60+25, 130+25, 60+25, 240+25)

        painter.setPen(QPen(Qt.magenta, 2.0, Qt.SolidLine))
        painter.drawLine(120+25, 130+25, 60+25, 240+25)

        #원 그리기
        painter.setPen(QPen(Qt.black, 1.0, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.cyan))
        painter.drawEllipse(0, 130, 50, 50)

        painter.setPen(QPen(Qt.black, 1.0, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(60, 130, 50, 50)

        painter.setPen(QPen(Qt.black, 1.0, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red))
        painter.drawEllipse(120, 130, 50, 50)

        painter.setPen(QPen(Qt.black, 1.0, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.gray))
        painter.drawEllipse(60, 240, 50, 50)

        # 텍스트 그리기
        painter.setPen(QPen(Qt.darkCyan, 1.0, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawText(130, 250, '안녕하세요')

        painter.end()



if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = MyApp()
   sys.exit(app.exec_())