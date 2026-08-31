import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(
    page_title="💀 붉은 저택: 자유 탐색",
    page_icon="🩸",
    layout="wide"
)

# 다크 테마 커스텀 CSS
st.markdown("""
<style>
    .stApp {
        background-color: #050505;
        color: #d1d1d1;
        font-family: 'Courier New', Courier, monospace;
    }
    .horror-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ff0000;
        text-align: center;
        text-shadow: 0 0 10px #ff0000;
    }
    .status-panel {
        background-color: #111111;
        border: 2px solid #550000;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .control-panel {
        background-color: #1a1a1a;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 8px;
    }
    .stButton>button {
        width: 100%;
        background-color: #330000;
        color: #ffffff;
        border: 1px solid #ff0000;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff0000;
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)

# 맵 구조 정의 (5x5 크기 지도)
MAP_GRID = {
    (0, 0): {"name": "🔒 현관문 (출구)", "item": None, "desc": "쇠사슬로 잠긴 현관문입니다. 탈출하려면 4개의 신성한 도구가 필요합니다."},
    (0, 1): {"name": "어두운 복도 동쪽", "item": None, "desc": "스산한 바람이 불어오는 길고 어두운 복도입니다."},
    (0, 2): {"name": "🕯️ 제단실", "item": "고대의 부적", "desc": "붉은 양초가 켜진 제단입니다. 의식용 문양이 그려져 있습니다."},
    (1, 0): {"name": "어두운 복도 남쪽", "item": None, "desc": "발걸음 소리가 울려 퍼지는 복도입니다."},
    (1, 1): {"name": "🏚️ 낡은 거실", "item": None, "desc": "찢어진 소파와 부서진 가구들이 널브러져 있습니다."},
    (1, 2): {"name": "📚 서재", "item": "녹슨 열쇠", "desc": "오래된 책들이 쌓여 있습니다. 먼지가 자욱합니다."},
    (2, 0): {"name": "🍽️ 식당", "item": "의식용 소금", "desc": "악취가 나는 식탁이 놓여 있습니다."},
    (2, 1): {"name": "🍷 침실", "item": "은빛 십자가", "desc": "피로 물든 침대가 보입니다."},
    (2, 2): {"name": "🕸️ 지하실 입구", "item": None, "desc": "지하로 내려가는 계단입니다. 깊은 어둠이 깔려 있습니다."}
}

# 세션 상태 초기화
if 'player_x' not in st.session_state:
    st.session_state.player_x = 1
if 'player_y' not in st.session_state:
    st.session_state.player_y = 1
if 'stamina' not in st.session_state:
    st.session_state.stamina = 100
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'searched_pos' not in st.session_state:
    st.session_state.searched_pos = []
if 'ghost_spawned' not in st.session_state:
    st.session_state.ghost_spawned = False
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'escaped' not in st.session_state:
    st.session_state.escaped = False

# 리셋 함수
def restart_game():
    st.session_state.player_x = 1
    st.session_state.player_y = 1
    st.session_state.stamina = 100
    st.session_state.inventory = []
    st.session_state.searched_pos = []
    st.session_state.ghost_spawned = False
    st.session_state.game_over = False
    st.session_state.escaped = False

# 이동 처리 함수
def move_player(dx, dy):
    new_x = st.session_state.player_x + dx
    new_y = st.session_state.player_y + dy
    if (new_x, new_y) in MAP_GRID:
        st.session_state.player_x = new_x
        st.session_state.player_y = new_y
        
        # 이동 시 30% 확률로 귀신 조우
        if random.random() < 0.3 and (new_x, new_y) != (0, 0):
            st.session_state.ghost_spawned = True
        else:
            st.session_state.ghost_spawned = False
    else:
        st.toast("벽에 막혀 이동할 수 없습니다!", icon="🧱")

# 헤더
st.markdown("<h1 class='horror-title'>💀 붉은 저택: 자유 탐색 🩸</h1>", unsafe_allow_html=True)

if not st.session_state.game_over and not st.session_state.escaped:
    
    current_pos = (st.session_state.player_x, st.session_state.player_y)
    current_room = MAP_GRID[current_pos]

    # 상태 표시줄
    st.markdown(f"""
    <div class='status-panel'>
        🩸 <strong>정신력(HP):</strong> {st.session_state.stamina}% | 
        📍 <strong>현재 위치:</strong> {current_room['name']} (좌표: {current_pos}) | 
        🎒 <strong>소지품:</strong> {', '.join(st.session_state.inventory) if st.session_state.inventory else '없음'}
    </div>
    """, unsafe_allow_html=True)

    # 귀신 습격 이벤트
    if st.session_state.ghost_spawned:
        st.error("⚠️ 쿵... 쿵... 근처에서 이상한 소리가 납니다! 귀신의 기운이 느껴집니다.")
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("🏃 도망치기 (체력 -15)"):
                st.session_state.stamina -= 15
                st.session_state.ghost_spawned = False
                if st.session_state.stamina <= 0:
                    st.session_state.game_over = True
                st.rerun()
        with col_act2:
            if st.button("🔦 후두려 때리기 / 격퇴 시도"):
                if "의식용 소금" in st.session_state.inventory:
                    st.success("소금을 뿌려 귀신을 퇴치했습니다!")
                    st.session_state.ghost_spawned = False
                else:
                    st.error("무기가 없어 귀신에게 습격당했습니다! (체력 -30)")
                    st.session_state.stamina -= 30
                    st.session_state.ghost_spawned = False
                    if st.session_state.stamina <= 0:
                        st.session_state.game_over = True
                st.rerun()

    else:
        # 방 정보 출력
        st.info(f"👁️ {current_room['desc']}")

        # 조작 컨트롤 패널 (상/하/좌/우 + 행동)
        st.markdown("### 🎮 탐색 패널")
        col_left, col_mid, col_right = st.columns([1, 1, 1])

        with col_mid:
            if st.button("⬆️ 북쪽으로 이동"):
                move_player(-1, 0)
                st.rerun()

        col_l, col_m, col_r = st.columns([1, 1, 1])
        with col_l:
            if st.button("⬅️ 서쪽으로 이동"):
                move_player(0, -1)
                st.rerun()
        with col_m:
            # 수색 및 탈출 행동
            if current_pos == (0, 0):
                if st.button("🔓 현관문 탈출 시도"):
                    required = ["녹슨 열쇠", "고대의 부적", "은빛 십자가", "의식용 소금"]
                    if all(i in st.session_state.inventory for i in required):
                        st.session_state.escaped = True
                    else:
                        st.error(f"열쇠와 성물이 부족합니다! 필요: {', '.join(required)}")
                    st.rerun()
            else:
                if st.button("🔍 주변 수색하기"):
                    if current_pos not in st.session_state.searched_pos:
                        st.session_state.searched_pos.append(current_pos)
                        found_item = current_room["item"]
                        if found_item:
                            st.session_state.inventory.append(found_item)
                            st.success(f"🎉 아이템 발견: [{found_item}]을 획득했습니다!")
                        else:
                            st.warning("아무것도 찾지 못했습니다.")
                    else:
                        st.toast("이미 수색한 장소입니다.", icon="⚠️")
                    st.rerun()
        with col_r:
            if st.button("➡️ 동쪽으로 이동"):
                move_player(0, 1)
                st.rerun()

        with col_mid:
            if st.button("⬇️ 남쪽으로 이동"):
                move_player(1, 0)
                st.rerun()

# 게임 오버
elif st.session_state.game_over:
    st.error("💥 정신력을 모두 잃었습니다... 저택의 어둠 속으로 끌려갑니다.")
    if st.button("🔄 다시 시작"):
        restart_game()
        st.rerun()

# 탈출 성공
elif st.session_state.escaped:
    st.balloons()
    st.success("🎉 모든 구송품을 사용해 저택을 무사히 탈출했습니다!")
    if st.button("🔄 다시 시작"):
        restart_game()
        st.rerun()
