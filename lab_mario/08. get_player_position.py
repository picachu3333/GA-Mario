# get_player_position.py

import retro

env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
env.reset()

ram = env.get_ram()

# 0x03AD	Player x pos within current screen offset
# 현재 화면 속 플레이어 x 좌표
player_position_x = ram[0x03AD]
# 0x03B8	Player y pos within current screen
# 현재 화면 속 플레이어 y좌표
player_position_y = ram[0x03B8]

print(player_position_x, player_position_y)

# 타일 좌표로 변환 (고해상도의 좌표를 타일에 표현하기 위해 16*16의 픽셀을 한 타일에 표현하기 위해서 나눠줌)
player_tile_position_x = player_position_x // 16
player_tile_position_y = player_position_y // 16

print(player_tile_position_x, player_tile_position_y)