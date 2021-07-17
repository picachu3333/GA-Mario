#03.get_screen.py
import retro

#게임 환경 생성
env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
#새게임 시작
env.reset()


#화면가져오기
screen = env.get_screen()

print(screen.shape)
print(screen)
