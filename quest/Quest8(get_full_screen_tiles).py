import sys, retro
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import numpy as np

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # 게임 환경 생성
        self.env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
        # 새게임 시작
        self.env.reset()

        self.screen_size = 2

        # 키배열 : B, NULL, SELECT, START, Up, Down, Left, Right, A
        self.button = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.game_speed = 60

        # 화면 가져오기
        screen = self.env.get_screen()

        # 화면 크기
        self.width = screen.shape[0]
        self.height = screen.shape[1]

        # 창 크기 고정
        self.setFixedSize(self.width * self.screen_size + 600, self.height * self.screen_size)
        # 창 제목 설정
        self.setWindowTitle('GA-Mario')

        self.label_image = QLabel(self)
        self.label_image.setGeometry(0, 0, self.width * self.screen_size, self.height * self.screen_size)

        # 타이머 생성
        self.qtimer = QTimer(self)
        # 타이머에 실행할 함수 연결
        self.qtimer.timeout.connect(self.timer)
        # 1초(1000밀리초)마다 연결된 함수를 실행
        self.qtimer.start(1000//self.game_speed)

        # 창 띄우기
        self.show()


    def timer(self):
        self.env.step(np.array(self.button))

        # 화면 가져오기
        screen = self.env.get_screen()

        image = np.array(screen)
        qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(self.width * self.screen_size, self.height * self.screen_size, Qt.IgnoreAspectRatio)

        self.label_image.setPixmap(pixmap)

        self.update()



    def paintEvent(self,event):
        # 그리기 도구
        painter = QPainter()
        # 그리기 시작
        painter.begin(self)

        # 램
        ram = self.env.get_ram()

        full_screen_tiles = ram[0x0500:0x069F + 1]

        full_screen_tile_count = full_screen_tiles.shape[0]

        full_screen_page1_tile = full_screen_tiles[:full_screen_tile_count // 2].reshape((13, 16))
        full_screen_page2_tile = full_screen_tiles[full_screen_tile_count // 2:].reshape((13, 16))

        full_screen_tiles = np.concatenate((full_screen_page1_tile, full_screen_page2_tile), axis=1).astype(np.int)

        for i in range(full_screen_tiles.shape[0]):
            for j in range(full_screen_tiles.shape[1]):

                if full_screen_tiles[i][j] == 0x00:
                    painter.setBrush(QBrush(Qt.lightGray))
                    painter.drawRect(self.width * self.screen_size + 16 * j, 0 + 16 * i, 16, 16)

                else:
                    painter.setBrush(QBrush(Qt.cyan))
                    painter.drawRect(self.width * self.screen_size + 16 * j, 0 + 16 * i, 16, 16)


    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Up:
            self.button[4] = 1

        if key == Qt.Key_Down:
            self.button[5] = 1

        if key == Qt.Key_Left:
            self.button[6] = 1

        if key == Qt.Key_Right:
            self.button[7] = 1

        if key == Qt.Key_Z:
            self.button[8] = 1

        if key == Qt.Key_X:
            self.button[0] = 1

        if key == Qt.Key_N:
            self.button[2] = 1

        if key == Qt.Key_M:
            self.button[3] = 1

        # if key == Qt.Key_1:
        #     self.screen_size -= 0.25
        #     # 창 크기 고정
        #     self.setFixedSize(self.width * self.screen_size, self.height * self.screen_size)
        #     self.label_image.setGeometry(0, 0, self.width * self.screen_size, self.height * self.screen_size)
        #     print(self.screen_size,"size")
        #
        # if key == Qt.Key_2:
        #     self.screen_size += 0.25
        #     # 창 크기 고정
        #     self.setFixedSize(self.width * self.screen_size, self.height * self.screen_size)
        #     self.label_image.setGeometry(0, 0, self.width * self.screen_size, self.height * self.screen_size)
        #     print(self.screen_size, "size")

        if key == Qt.Key_R:
            self.env.reset()

        if key == 46:
            self.game_speed += 10
            if (self.game_speed > 200):
                self.game_speed = 200
            self.qtimer.stop()
            self.qtimer.start(1000//self.game_speed)
            print(self.game_speed, "speed")

        if key == 44:
            self.game_speed -= 10
            if (self.game_speed < 10):
                self.game_speed = 10
            self.qtimer.stop()
            self.qtimer.start(1000 // self.game_speed)
            print(self.game_speed, "speed")

    def keyReleaseEvent(self, event):
        key = event.key()

        if key == Qt.Key_Up:
            self.button[4] = 0

        if key == Qt.Key_Down:
            self.button[5] = 0

        if key == Qt.Key_Left:
            self.button[6] = 0

        if key == Qt.Key_Right:
            self.button[7] = 0

        if key == Qt.Key_Z:
            self.button[8] = 0

        if key == Qt.Key_X:
            self.button[0] = 0

        if key == Qt.Key_N:
            self.button[2] = 0

        if key == Qt.Key_M:
            self.button[3] = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())