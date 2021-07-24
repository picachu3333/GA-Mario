import sys, retro
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import numpy as np


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # 게임 환경 생성
        env = retro.make(game='SuperMarioBros-Nes', state='Level8-1')
        # 새게임 시작
        env.reset()

        # 화면가져오기
        screen = env.get_screen()

        # 창 크기 고정
        self.setFixedSize(screen.shape[0]*2, screen.shape[1]*2)
        # 창 제목 설정
        self.setWindowTitle('GA-Mario')

        label_image = QLabel(self)

        image = np.array(screen)
        qimage = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(screen.shape[0]*2, screen.shape[1]*2, Qt.IgnoreAspectRatio)

        label_image.setPixmap(pixmap)
        label_image.setGeometry(0, 0, screen.shape[0]*2, screen.shape[1]*2)

        # 창 띄우기
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())