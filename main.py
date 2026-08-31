import streamlit as st
import random

# 페이지 설정 (다크 모드 기본)
st.set_page_config(
    page_title="💀 붉은 저택의 위령제",
    page_icon="🩸",
    layout="wide"
)

# 공포 분위기를 극대화하는 커스텀 CSS (어두운 테마, 글자 흔들림, 피 빛 효과)
st.markdown("""
<style>
    /* 전체 배경: 칠흑 같은 검은색 및 빨간 그라데이션 */
    .stApp {
        background: radial-gradient(circle, #1a0000 0%, #000000 100%);
        color: #e0e0e0;
        font-family: 'Courier New', Courier, monospace;
    }

    /* 메인 타이틀 피 빛 붉은색 및 진동 효과 */
    .horror-title {
        font-size: 3rem;
        font-weight: 900;
        color: #ff0000;
        text-align: center;
        text-shadow: 0 0 10px #ff0000, 0 0 20px #8b0000;
        animation: glitch 1s infinite alternate;
    }

    /* 섬뜩한 텍스트 애니메이션 */
    @keyframes glitch {
        0% { transform: translate(0); }
        20% { transform: translate(-2px, 2px); }
        40% { transform: translate(-2px, -2px); }
        60% { transform: translate(2px, 2px); }
        80% { transform: translate(2px, -2px); }
        100% { transform: translate(0); }
    }

    /* 서브 타이틀 및 경고문 */
    .horror-sub {
        font-size: 1.2rem;
        color: #a9a9a9;
        text-align: center;
        margin-bottom: 30px;
    }

    /* 게임 상황판 스타일 */
    .status-box {
        background-color: #0d0d0d;
        border: 2px solid #8b0000;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
    }

    /* 깜빡이는 조명 효과 카드 */
    .story-box {
        background-color: #050505;
        border-left: 5px solid #ff0000;
        padding: 20px;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 20px;
        animation: blinker 2s linear infinite;
    }

    @keyframes blinker {
        50% { opacity: 0.7; }
    }

    /* 스트림릿 버튼 스타일 덮어쓰기 */
    .stButton>button {
        width: 100%;
        background-color: #2b0000;
        color: #ffffff;
        border: 1px solid #ff0000;
        font-size: 1.1rem;
        padding: 10px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #ff0000;
        color: #000000;
        font-weight: bold;
        box-shadow: 0 0 15px #ff0000;
    }
</style>
""", unsafe_allow_html=True)

# 게임 상태 초기화
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'stamina' not in st.session_state:
    st.session_state.stamina = 100
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'current_room' not in st.session_state:
    st.session_state.current_room = "현관"
if 'ghost_near' not in st.session_state:
    st.session_state.ghost_near = False
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'escaped' not in st.session_state:
    st.session_state.escaped = False

# 리셋 함수
def restart_game():
    st.session_state.game_started = True
    st.session_state.stamina = 100
    st.session_state.inventory = []
    st.session_state.current_room = "현관"
    st.session_state.ghost_near = False
    st.session_state.game_over = False
    st.session_state.escaped = False

# 배경음악 (에러 원인이 되었던 html 구문을 한 줄 문자열로 안전하게 수정)
st.components.v1.html(
    '<audio autoplay loop hidden><source src="https://assets.mixkit.co/active_storage/sfx/2874/2874-preview.mp3" type="audio/mpeg"></audio>',
    height=0
)

# 헤더
st.markdown("<h1 class='horror-title'>💀 붉은 저택의 위령제 🩸</h1>", unsafe_allow_html=True)
st.markdown("<p class='horror-sub'>🔊 볼륨을 높이고, 헤드셋을 착용하십시오. 불을 끄는 것을 권장합니다...</p>", unsafe_allow_html=True)

# 1. 게임 시작 화면
if not st.session_state.game_started:
    st.markdown("""
    <div class='story-box'>
        비가 거세게 내리치는 밤, 당신은 차 고장으로 인해 산속의 오래된 폐가로 피신했습니다.<br>
        하지만 쿵- 소리와 함께 현관문이 굳게 닫혀버렸습니다.<br><br>
        <strong>"누군가... 문 뒤에 있어..."</strong><br><br>
        이 집의 피 비린내 나는 비밀을 풀고, 3개의 탈출 도구(녹슨 열쇠, 부적, 십자가)를 찾아 살아남으십시오.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("👁️ 어둠 속으로 들어가지 (게임 시작)"):
        st.session_state.game_started = True
        st.rerun()

# 2. 게임 진행 화면
elif not st.session_state.game_over and not st.session_state.escaped:
    
    # 상단 상태창
    st.markdown(f"""
    <div class='status-box'>
        🩸 <strong>정신력(체력):</strong> {st.session_state.stamina}% &nbsp;|&nbsp;
        📍 <strong>현재 위치:</strong> {st.session_state.current_room} &nbsp;|&nbsp;
        🎒 <strong>인벤토리:</strong> {', '.join(st.session_state.inventory) if st.session_state.inventory else '없음'}
    </div>
    """, unsafe_allow_html=True)

    # 귀신 습격 이벤트 발생 시 (현관이 아닐 때 확률 발생)
    if st.session_state.ghost_near and st.session_state.current_room != "현관":
        st.error("⚠️ 쿵... 쿵... 차가운 한기가 느껴집니다. 귀신이 당신의 뒤에 서 있습니다!")
        st.image("https://images.unsplash.com/photo-1509248961158-e54f6934749c?auto=format&fit=crop&w=800&q=80", caption="그녀와 눈이 마주쳤습니다...", use_container_width=True)
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            if st.button("😱 숨죽이고 숨기"):
                if random.random() < 0.7:
                    st.session_state.ghost_near = False
                    st.success("👻 귀신이 당신을 보지 못하고 스쳐 지나갔습니다...")
                    st.rerun()
                else:
                    st.session_state.stamina -= 35
                    st.session_state.ghost_near = False
                    st.error("🩸 귀신에게 공격당했습니다! 정신력이 크게 감소합니다.")
                    if st.session_state.stamina <= 0:
                        st.session_state.game_over = True
                    st.rerun()
        with col_g2:
            if st.button("🏃 무작정 도망치기"):
                st.session_state.stamina -= 20
                st.session_state.ghost_near = False
                st.warning("💨 허겁지겁 도망쳤지만 무릎을 다쳤습니다.")
                if st.session_state.stamina <= 0:
                    st.session_state.game_over = True
                st.rerun()

    else:
        # 방별 스토리 및 선택지
        st.markdown("<hr style='border-color: #8b0000;'>", unsafe_allow_html=True)

        # [현관]
        if st.session_state.current_room == "현관":
            st.image("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80", use_container_width=True)
            st.markdown("<div class='story-box'>출구 문이 쇠사슬로 묶여 있습니다. 열쇠와 결계를 풀 물건들이 필요합니다.</div>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🚪 복도로 이동"):
                    st.session_state.current_room = "어두운 복도"
                    st.session_state.ghost_near = random.random() < 0.35
                    st.rerun()
            with c2:
                if st.button("🔓 문 열기 (탈출 시도)"):
                    needed = ["녹슨 열쇠", "고대의 부적", "은빛 십자가"]
                    if all(item in st.session_state.inventory for item in needed):
                        st.session_state.escaped = True
                        st.rerun()
                    else:
                        st.error(f"문이 열리지 않습니다! 필요 아이템: {', '.join(needed)}")

        # [어두운 복도]
        elif st.session_state.current_room == "어두운 복도":
            st.image("https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80", use_container_width=True)
            st.markdown("<div class='story-box'>기나긴 복도입니다. 양옆으로 서재와 지하실로 들어가는 문이 보입니다.</div>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("📚 서재로 들어가기"):
                    st.session_state.current_room = "서재"
                    st.session_state.ghost_near = random.random() < 0.35
                    st.rerun()
            with c2:
                if st.button("🕯️ 지하 의식실로 내려가기"):
                    st.session_state.current_room = "지하 의식실"
                    st.session_state.ghost_near = random.random() < 0.35
                    st.rerun()
            with c3:
                if st.button("🏃 현관으로 돌아가기"):
                    st.session_state.current_room = "현관"
                    st.rerun()

        # [서재]
        elif st.session_state.current_room == "서재":
            st.image("https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=800&q=80", use_container_width=True)
            st.markdown("<div class='story-box'>수많은 낡은 책들이 쌓여있습니다. 책상 위에서 반짝이는 것이 보입니다.</div>", unsafe_allow_html=True)
            
            if "녹슨 열쇠" not in st.session_state.inventory:
                if st.button("🔑 서랍 수색하기"):
                    st.session_state.inventory.append("녹슨 열쇠")
                    st.success("아이템 획득: [녹슨 열쇠]를 찾았습니다!")
                    st.rerun()
            else:
                st.info("서랍은 이미 비어 있습니다.")

            if st.button("🚪 복도로 나아가기"):
                st.session_state.current_room = "어두운 복도"
                st.session_state.ghost_near = random.random() < 0.35
                st.rerun()

        # [지하 의식실]
        elif st.session_state.current_room == "지하 의식실":
            st.image("https://images.unsplash.com/photo-1514539079130-25950c84af65?auto=format&fit=crop&w=800&q=80", use_container_width=True)
            st.markdown("<div class='story-box'>붉은 양초가 켜져 있는 기괴한 공간입니다. 제단 위에 무언가 올려져 있습니다.</div>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if "고대의 부적" not in st.session_state.inventory:
                    if st.button("📜 제단 위의 부적 집기"):
                        st.session_state.inventory.append("고대의 부적")
                        st.success("아이템 획득: [고대의 부적]을 챙겼습니다!")
                        st.rerun()
            with c2:
                if "은빛 십자가" not in st.session_state.inventory:
                    if st.button("✝️ 벽에 걸린 십자가 떼어내기"):
                        st.session_state.inventory.append("은빛 십자가")
                        st.success("아이템 획득: [은빛 십자가]를 챙겼습니다!")
                        st.rerun()

            if st.button("🚪 복도로 올라가기"):
                st.session_state.current_room = "어두운 복도"
                st.session_state.ghost_near = random.random() < 0.35
                st.rerun()

# 3. 게임 오버 화면
elif st.session_state.game_over:
    st.markdown("<h1 style='text-align: center; color: red;'>💥 GAME OVER 💥</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80", use_container_width=True)
    st.error("당신의 정신력이 모두 소진되었습니다. 붉은 저택의 새로운 원혼이 되었습니다...")
    if st.button("🔄 다시 도전하기"):
        restart_game()
        st.rerun()

# 4. 게임 클리어 화면
elif st.session_state.escaped:
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: #00ff00;'>🎉 탈출 성공! 🎉</h1>", unsafe_allow_html=True)
    st.success("모든 결계를 풀고 저택을 무사히 탈출했습니다! 당신은 밤을 살아남았습니다.")
    if st.button("🔄 처음부터 다시 하기"):
        restart_game()
        st.rerun()
