import tkinter as tk
import math
import random

class HorrorGame3D:
    def __init__(self, root):
        self.root = root
        self.root.title("어둠 속의 탈출 - 3D First Person")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # 3D 캔버스 설정
        self.canvas = tk.Canvas(root, width=800, height=600, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 플레이어 상태 (1인칭 시점 및 위치)
        self.px = 2.0
        self.py = 2.0
        self.angle = 0.0  # 보는 각도(라디안)
        self.fov = math.pi / 3  # 시야각(60도)
        self.move_speed = 0.08
        self.rot_speed = 0.05
        self.stamina = 100.0

        # 게임 진행 변수
        self.has_key = False
        self.game_over = False
        self.escaped = False
        self.jumpscare_timer = 0

        # 맵 구조 (1: 벽, 0: 통로, 2: 열쇠, 3: 출구)
        self.map_grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 2, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 3, 1, 1, 1, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        # 3D 귀신 위치
        self.gx = 7.5
        self.gy = 7.5
        self.ghost_speed = 0.035

        # 키 입력을 위한 상태 저장
        self.keys = {}
        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)

        # 게임 루프 시작
        self.game_loop()

    def key_down(self, event):
        self.keys[event.keysym.lower()] = True

    def key_up(self, event):
        self.keys[event.keysym.lower()] = False

    def process_movement(self):
        if self.game_over:
            return

        # Shift 입력 시 달리며 스테미나 소비
        speed = self.move_speed
        if self.keys.get("shift_l") or self.keys.get("shift_r"):
            if self.stamina > 5:
                speed *= 1.6
                self.stamina -= 0.8
        else:
            self.stamina = min(100.0, self.stamina + 0.3)

        # 회전 (A, D 키 또는 좌우 화살표)
        if self.keys.get("a") or self.keys.get("left"):
            self.angle -= self.rot_speed
        if self.keys.get("d") or self.keys.get("right"):
            self.angle += self.rot_speed

        # 이동 계산 (W, S 키)
        dx = math.cos(self.angle) * speed
        dy = math.sin(self.angle) * speed

        if self.keys.get("w") or self.keys.get("up"):
            if self.map_grid[int(self.py)][int(self.px + dx)] == 0:
                self.px += dx
            if self.map_grid[int(self.py + dy)][int(self.px)] == 0:
                self.py += dy
        if self.keys.get("s") or self.keys.get("down"):
            if self.map_grid[int(self.py)][int(self.px - dx)] == 0:
                self.px -= dx
            if self.map_grid[int(self.py - dy)][int(self.px)] == 0:
                self.py -= dy

        # 열쇠 획득 체크
        ix, iy = int(self.px), int(self.py)
        if self.map_grid[iy][ix] == 2:
            self.has_key = True
            self.map_grid[iy][ix] = 0

        # 탈출 체크
        if self.map_grid[iy][ix] == 3 and self.has_key:
            self.escaped = True
            self.game_over = True

    def update_ghost(self):
        if self.game_over:
            return

        # 귀신이 플레이어를 실시간 추격
        dx = self.px - self.gx
        dy = self.py - self.gy
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 0.1:
            self.gx += (dx / dist) * self.ghost_speed
            self.gy += (dy / dist) * self.ghost_speed

        # 잡혔을 때 게임 오버
        if dist < 0.6:
            self.jumpscare_timer = 15
            self.game_over = True

    def render_3d(self):
        self.canvas.delete("all")
        w, h = 800, 600
        num_rays = 80  # 가로 레이캐스팅 광선 수

        # 천장/바닥 어두운 배경 연출
        self.canvas.create_rectangle(0, 0, w, h // 2, fill="#0a0a0a")
        self.canvas.create_rectangle(0, h // 2, w, h, fill="#141414")

        # 레이캐스팅(Raycasting)으로 3D 벽 렌더링
        for i in range(num_rays):
            ray_angle = (self.angle - self.fov / 2) + (i / num_rays) * self.fov
            distance_to_wall = 0.0
            hit_wall = False
            
            cos_a = math.cos(ray_angle)
            sin_a = math.sin(ray_angle)

            while not hit_wall and distance_to_wall < 10.0:
                distance_to_wall += 0.05
                test_x = int(self.px + cos_a * distance_to_wall)
                test_y = int(self.py + sin_a * distance_to_wall)

                if test_x < 0 or test_x >= 10 or test_y < 0 or test_y >= 10:
                    hit_wall = True
                    distance_to_wall = 10.0
                elif self.map_grid[test_y][test_x] == 1:
                    hit_wall = True

            # 어두운 시야 거리 감쇄 계산 (손전등 효과)
            corrected_dist = distance_to_wall * math.cos(ray_angle - self.angle)
            wall_height = min(h, int(h / (corrected_dist + 0.0001)))
            
            # 음영 처리
            shade = max(0, int(200 - (corrected_dist * 20)))
            color_hex = f"#{shade:02x}{int(shade*0.2):02x}{int(shade*0.2):02x}"

            x1 = i * (w / num_rays)
            x2 = (i + 1) * (w / num_rays)
            y1 = (h // 2) - (wall_height // 2)
            y2 = (h // 2) + (wall_height // 2)

            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color_hex, outline="")

        # 3D 귀신 시각화
        dx = self.gx - self.px
        dy = self.gy - self.py
        sprite_dist = math.sqrt(dx * dx + dy * dy)
        sprite_angle = math.atan2(dy, dx) - self.angle

        # 회전 보정
        while sprite_angle < -math.pi: sprite_angle += 2 * math.pi
        while sprite_angle > math.pi: sprite_angle -= 2 * math.pi

        if -self.fov / 2 < sprite_angle < self.fov / 2 and sprite_dist > 0.5:
            screen_x = (w // 2) + int(math.tan(sprite_angle) * (w // 2))
            size = min(400, int(h / sprite_dist))
            
            # 창백한 붉은 눈의 3D 형상
            self.canvas.create_oval(
                screen_x - size // 3, (h // 2) - size // 2,
                screen_x + size // 3, (h // 2) + size // 2,
                fill="#d0d0d0", outline="#aa0000", width=2
            )
            self.canvas.create_oval(
                screen_x - size // 6, (h // 2) - size // 4,
                screen_x - size // 10, (h // 2) - size // 6,
                fill="red"
            )
            self.canvas.create_oval(
                screen_x + size // 10, (h // 2) - size // 4,
                screen_x + size // 6, (h // 2) - size // 6,
                fill="red"
            )

        # HUD UI 연출
        self.canvas.create_text(
            110, 30, text=f"스테미나: {int(self.stamina)}%", fill="white", font=("맑은 고딕", 12)
        )
        key_status = "열쇠 보유: O" if self.has_key else "열쇠 보유: X (미션: 노란 영역을 찾으세요)"
        self.canvas.create_text(
            200, 55, text=key_status, fill="yellow" if self.has_key else "gray", font=("맑은 고딕", 12)
        )

        # 게임 오버/점프스케어 화면
        if self.jumpscare_timer > 0:
            self.canvas.create_rectangle(0, 0, w, h, fill="darkred")
            self.canvas.create_text(
                w // 2, h // 2, text="귀신에게 잡혔습니다!", fill="black", font=("맑은 고딕", 32, "bold")
            )
            self.jumpscare_timer -= 1
        elif self.escaped:
            self.canvas.create_rectangle(0, 0, w, h, fill="black")
            self.canvas.create_text(
                w // 2, h // 2, text="축하합니다! 어둠 속에서 탈출했습니다!", fill="cyan", font=("맑은 고딕", 28)
            )

    def game_loop(self):
        self.process_movement()
        self.update_ghost()
        self.render_3d()
        self.root.after(30, self.game_loop)

# 앱 실행
if __name__ == "__main__":
    root = tk.Tk()
    game = HorrorGame3D(root)
    root.mainloop()
