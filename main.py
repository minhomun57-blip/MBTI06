from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

# 게임 앱 생성
app = Ursina()

# 기본 화면 설정
window.title = "3D 어둠 속의 탈출 (WASD 이동)"
window.borderless = False
window.fullscreen = False
window.fps_counter.enabled = True

# 1. 환경 및 안개 설정 (어두운 분위기 연출)
scene.fog_color = color.black
scene.fog_density = (0.05, 0.25) # 자욱한 어둠 안개

# 조명 (매우 어두운 기본 조명)
ambient_light = AmbientLight(color=color.rgb(10, 10, 15))

# 2. 1인칭 플레이어 컨트롤러 (WASD + 마우스 이동)
player = FirstPersonController(
    speed=5,
    mouse_sensitivity=Vec2(40, 40),
    position=(0, 1, -10)
)
player.cursor.color = color.red # 붉은 점 에임

# 플레이어 손전등 (카메라에 고정된 조명)
flashlight = SpotLight(parent=camera, position=(0.2, -0.2, 0), color=color.rgb(255, 240, 200))
flashlight.look_at(camera.position + camera.forward * 10)

# 3. 맵 구현 (폐쇄된 지하 복도/저택)
# 바닥
floor = Entity(
    model='plane',
    scale=(40, 1, 40),
    color=color.dark_gray,
    texture='white_cube',
    collider='box'
)

# 천장
ceiling = Entity(
    model='plane',
    scale=(40, 1, 40),
    position=(0, 8, 0),
    rotation=(180, 0, 0),
    color=color.black,
    collider='box'
)

# 외벽 세우기
walls = [
    Entity(model='cube', scale=(40, 8, 1), position=(0, 4, 20), color=color.gray, collider='box'),
    Entity(model='cube', scale=(40, 8, 1), position=(0, 4, -20), color=color.gray, collider='box'),
    Entity(model='cube', scale=(1, 8, 40), position=(20, 4, 0), color=color.gray, collider='box'),
    Entity(model='cube', scale=(1, 8, 40), position=(-20, 4, 0), color=color.gray, collider='box'),
]

# 내부 장애물 기둥
for i in range(5):
    rx = random.randint(-15, 15)
    rz = random.randint(-15, 15)
    Entity(model='cube', scale=(2, 8, 2), position=(rx, 4, rz), color=color.dark_gray, collider='box')

# 4. 3D 귀신 (몬스터) 생성
# 기괴하게 창백하고 길쭉한 형상의 3D 귀신
ghost = Entity(
    model='cube', # 실제 게임 시 3D 몬스터 모델(.obj/.gltf) 파일로 대체 가능
    scale=(1.2, 3.5, 1.2),
    position=(0, 1.75, 15),
    color=color.rgb(220, 220, 220), # 창백한 색상
    collider='box'
)

# 귀신 눈빛 (붉은 빛)
ghost_eye1 = Entity(parent=ghost, model='sphere', scale=0.15, position=(-0.25, 1.2, -0.5), color=color.red)
ghost_eye2 = Entity(parent=ghost, model='sphere', scale=0.15, position=(0.25, 1.2, -0.5), color=color.red)

# 5. 미션 아이템 (탈출 열쇠)
key = Entity(
    model='sphere',
    scale=0.4,
    position=(15, 0.5, -15),
    color=color.yellow,
    collider='box'
)

# UI 텍스트
instructions = Text(
    text="WASD: 이동 | Shift: 달리기 | 마우스: 둘러보기\n어둠 속에서 [노란색 열쇠]를 찾아 귀신을 피해 탈출하세요!",
    origin=(0, 4),
    scale=1.2,
    color=color.white
)

game_over_text = Text(text="", origin=(0, 0), scale=2, color=color.red)

has_key = False
ghost_speed = 2.2

# 6. 실시간 게임 루프 (매 프레임 업데이트)
def update():
    global has_key, ghost_speed

    if not player.enabled:
        return

    # 달리기 기능 (Left Shift)
    if held_keys['left shift']:
        player.speed = 8
    else:
        player.speed = 5

    # 귀신이 플레이어를 향해 천천히 추격 (3D 위치 계산)
    ghost.look_at(player.position)
    # 귀신의 y축 회전만 유지 (기우러짐 방지)
    ghost.rotation_x = 0
    ghost.rotation_z = 0
    
    # 플레이어 쪽으로 이동
    direction = (player.position - ghost.position).normalized()
    ghost.position += direction * ghost_speed * time.dt

    # 귀신 기괴하게 떨리는 무서운 효과
    ghost.x += random.uniform(-0.03, 0.03)

    # 거리 계산
    dist_to_ghost = distance(player.position, ghost.position)
    
    # 플레이어와 귀신이 가까워지면 심장박동처럼 카메라 흔들림 연출
    if dist_to_ghost < 8:
        camera.x = random.uniform(-0.05, 0.05)
        camera.y = random.uniform(-0.05, 0.05)
        ghost_speed = 3.5 # 가까워지면 더 빠르게 추격
    else:
        ghost_speed = 2.2

    # 잡아먹혔을 때 (게임 오버)
    if dist_to_ghost < 1.8:
        player.enabled = False
        mouse.locked = False
        game_over_text.text = "귀신에게 잡혔습니다...\n[ Esc를 눌러 종료 ]"

    # 열쇠 획득 체크
    if not has_key and distance(player.position, key.position) < 1.5:
        has_key = True
        destroy(key)
        instructions.text = "열쇠를 찾았습니다! 출발 지점(Z: -18) 문으로 탈출하세요!"
        instructions.color = color.green

    # 탈출 성공 체크
    if has_key and player.z < -18:
        player.enabled = False
        mouse.locked = False
        game_over_text.text = "축하합니다! 어둠을 뚫고 탈출했습니다!"
        game_over_text.color = color.cyan

# 키 입력 처리
def input(key_name):
    if key_name == 'escape':
        application.quit()

# 게임 실행
app.run()
