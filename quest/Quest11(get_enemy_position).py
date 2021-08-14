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

        ## 모든 화면의 타일 표시
        full_screen_tiles = ram[0x0500:0x069F + 1]

        full_screen_tile_count = full_screen_tiles.shape[0]

        full_screen_page1_tile = full_screen_tiles[:full_screen_tile_count // 2].reshape((13, 16))
        full_screen_page2_tile = full_screen_tiles[full_screen_tile_count // 2:].reshape((13, 16))

        full_screen_tiles = np.concatenate((full_screen_page1_tile, full_screen_page2_tile), axis=1).astype(np.int)

        ## 적의 타일 표시(풀스크린(모든화면 타일)에서 표시)

        # 0x000F-0x0013	Enemy drawn? Max 5 enemies at once.
        # 0 - No
        # 1 - Yes (not so much drawn as "active" or something)
        enemy_drawn = ram[0x000F:0x0013 + 1]

        # 0x006E-0x0072	Enemy horizontal position in level
        # 자신이 속한 화면 페이지 번호
        enemy_horizon_position = ram[0x006E:0x0072 + 1]

        # 0x0087-0x008B	Enemy x position on screen
        # 자신이 속한 페이지 속 x 좌표
        enemy_screen_position_x = ram[0x0087:0x008B + 1]

        # 0x00CF-0x00D3	Enemy y pos on screen
        enemy_position_y = ram[0x00CF:0x00D3 + 1]

        # 적 x 좌표
        enemy_position_x = (enemy_horizon_position * 256 + enemy_screen_position_x) % 512

        # 적 타일 좌표
        enemy_tile_position_x = (enemy_position_x + 8) // 16
        enemy_tile_position_y = (enemy_position_y - 8) // 16 - 1

        for i in range(len(enemy_drawn)):
            if enemy_drawn[i] == 1:
                # painter.setBrush(QBrush(Qt.red))
                # painter.drawRect(self.width * self.screen_size + 16 * enemy_tile_position_x[i], 0 + 16 * enemy_tile_position_y[i], 16, 16)
                full_screen_tiles[enemy_tile_position_y[i]][enemy_tile_position_x[i]] = -1

        for i in range(full_screen_tiles.shape[0]):
            for j in range(full_screen_tiles.shape[1]):
                if full_screen_tiles[i][j] == 0:
                    painter.setBrush(QBrush(Qt.lightGray))
                    painter.drawRect(self.width * self.screen_size + 16 * j, 0 + 16 * i, 16, 16)

                elif full_screen_tiles[i][j] == -1:
                    painter.setBrush(QBrush(Qt.red))
                    painter.drawRect(self.width * self.screen_size + 16 * j, 0 + 16 * i, 16, 16)

                else:
                    painter.setBrush(QBrush(Qt.cyan))
                    painter.drawRect(self.width * self.screen_size + 16 * j, 0 + 16 * i, 16, 16)

        ## 현재 화면의 타일 표시

        # 현재 화면이 속한 페이지 번호
        current_screen_page = ram[0x071A]

        # 페이지 속 현재 화면 위치
        screen_position = ram[0x071C]

        # 화면 오프셋
        screen_offset = (256 * current_screen_page + screen_position) % 512

        # 타일 화면 오프셋
        screen_tile_offset = screen_offset // 16

        # 현재 화면 추출
        screen_tiles = np.concatenate((full_screen_tiles, full_screen_tiles), axis=1)[:, screen_tile_offset:screen_tile_offset + 16]

        for i in range(screen_tiles.shape[0]):
            for j in range(screen_tiles.shape[1]):
                if screen_tiles[i][j] == 0:
                    painter.setBrush(QBrush(Qt.lightGray))
                    painter.drawRect(self.width * self.screen_size + 16 * j, 250 + 16 * i, 16, 16)

                elif screen_tiles[i][j] == -1:
                    painter.setBrush(QBrush(Qt.red))
                    painter.drawRect(self.width * self.screen_size + 16 * j, 250 + 16 * i, 16, 16)

                else:
                    painter.setBrush(QBrush(Qt.cyan))
                    painter.drawRect(self.width * self.screen_size + 16 * j, 250 + 16 * i, 16, 16)

        ## 플레이어의 타일 표시(현재 화면의 타일에 표시)

        # 0x03AD	Player x pos within current screen offset
        # 현재 화면 속 플레이어 x 좌표
        player_position_x = ram[0x03AD]
        # 0x03B8	Player y pos within current screen
        # 현재 화면 속 플레이어 y좌표
        player_position_y = ram[0x03B8]

        # 타일 좌표로 변환 (고해상도의 좌표를 타일에 표현하기 위해 16*16의 픽셀을 한 타일에 표현하기 위해서 나눠줌)
        player_tile_position_x = (player_position_x + 8) // 16
        player_tile_position_y = (player_position_y + 8) // 16 - 1

        painter.setBrush(QBrush(Qt.blue))
        painter.drawRect(self.width * self.screen_size + 16 * player_tile_position_x,250 + 16 * player_tile_position_y, 16, 16)








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