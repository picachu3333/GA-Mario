#05.pyqt_timer.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # 창 크기 고정
        self.setFixedSize(400, 300)
        # 창 제목 설정
        self.setWindowTitle('MyApp')

        #타이머 생성
        qtimer = QTimer(self)
        #타이머에 실행할 함수 연결
        qtimer.timeout.connect(self.timer)
        #1초(1000밀리초)마다 연결된 함수를 실행
        qtimer.start(1000)

        # 창 띄우기
        self.show()

    #주기적으로 실행할 함수
    def timer(self):
        print('timer')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())