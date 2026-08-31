import streamlit as st
import random

# 페이지 설정 (다크 모드 기본)
st.set_page_config(
    page_title="💀 붉은 저택의 위령제: 심연",
    page_icon="🩸",
    layout="wide"
)

# 공포 분위기를 극대화하는 커스텀 CSS
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle, #1a0000 0%, #000000 100%);
        color: #e0e0e0;
        font-family: 'Courier New', Courier, monospace;
    }

    .horror-title {
        font-size: 3rem;
        font-weight: 900;
        color: #ff0000;
        text-align: center;
        text-shadow: 0 0 10px #ff0000, 0 0 20px #8b0000;
        animation: glitch 1s infinite alternate;
    }

    @keyframes glitch {
        0% { transform: translate(0); }
        20% { transform: translate(-2px, 2px); }
        40% { transform: translate(-2px, -2px); }
        60% { transform: translate(2px, 2px); }
        80% { transform: translate(2px, -2px); }
        100% { transform: translate(0); }
    }

    .horror-sub {
        font-size: 1.1rem;
        color: #a9a9a9;
        text-align: center;
        margin-bottom: 30px;
    }

    .status-box {
        background-color: #0d0d0d;
        border: 2px solid #8b0000;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
    }

    .story-box {
        background-color: #050505;
        border-left: 5px solid #ff0000;
        padding: 20px;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 20px;
        animation: blinker 2.5s linear infinite;
    }

    @keyframes blinker {
        50% { opacity: 0.7; }
    }

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
if 'current_ghost' not in st.session_state:
    st.session_state.current_ghost = None
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'escaped' not in st.session_state:
    st.session_state.escaped = False

# 귀신 데이터베이스
GHOST_TYPES = {
    "처녀귀신": {
        "name": "🕸️ 소박을 맞고 죽은 원혼",
        "desc": "긴 머리채를 늘어뜨린 채 피눈물을 흘리며 울부짖고 있습니다. 눈을 마주치면 정신이 아득해집니다.",
        "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?auto=format&fit=crop&w=800&q=80",
        "correct_action": "눈 감고 기도하기",
        "damage": 30
    },
    "기어다니는원혼": {
        "name": "🕷️ 기괴하게 꺾인 자",
        "desc": "관절이 기괴하게 꺾인 채 벽과 천장을 빠르게 기어다닙니다! 소리에 매우 민감합니다.",
        "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80",
        "correct_action": "숨죽이고 재빨리 숨기",
        "damage": 40
    },
    "거울속환영": {
        "name": "🪞 형체 없는 거울 속 환영",
        "desc": "당신의 얼굴을 한 무언가가 거울 속에서 비웃으며 손을 내밀고 있습니다.",
        "image": "https://images.unsplash.com/photo-1514539079130-25950c84af65?auto=format&fit=crop&w=800&q=80",
        "correct_action": "거울을 깨뜨리기",
        "damage": 25
    }
}

# 리셋 함수
def restart_game():
    st.session_state.game_started = True
    st.session_state.stamina = 100
    st.session_state.inventory = []
    st.session_state.current_room = "현관"
    st.session_state.current_ghost = None
    st.session_state.game_over = False
    st.session_state.escaped = False

# 귀신 스폰 로직
def check_ghost_spawn():
    if st.session_state.current_room != "현관" and random.random() < 0.45:
        ghost_key = random.choice(list(GHOST_TYPES.keys()))
        st.session_state.current_ghost = GHOST_TYPES[ghost_key]
    else:
        st.session_state.current_ghost = None

# 오디오 효과
st.components.v1.html(
    '<audio autoplay loop hidden><source src="https://assets.mixkit.co/active_storage/sfx/2874/2874-preview.mp3" type="audio/mpeg"></audio>',
    height=0
)

# 타이틀
st.markdown("<h1 class='horror-title'>💀 붉은 저택의 위령제: 심연 🩸</h1>", unsafe_allow_html=True)
st.markdown("<p class='horror-sub'>🔊 헤드셋을 착용하고 불을 끄세요. 저택 안의 원혼들이 당신의 숨소리를 듣고 있습니다.</p>", unsafe_allow_html=True)

# 1. 게임 시작 화면
if not st.session_state.game_started:
    st.markdown("""
    <div class='story-box'>
        비바람이 몰아치던 밤, 길을 잃은 당신은 오랜 세월 방치된 저택 안으로 들어섰습니다.<br>
        쿠쿵- 하는 소리와 함께 현관문이 굳게 닫히고, 쇠사슬이 감기는 소리가 들립니다.<br><br>
        저택 안에 존재하는 다양한 원혼들을 피하고, 탈출에 필요한 4가지 핵심 구송품<br>
        <strong>[녹슨 열쇠, 고대의 부적, 은빛 십자가, 의식용 소금]</strong>을 모두 찾아 탈출하십시오.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("👁️ 어둠 속으로 진입하기"):
        st.session_state.game_started = True
        st.rerun()

# 2. 게임 진행 화면
elif not st.session_state.game_over and not st.session_state.escaped:
    
    # 상태창
    st.markdown(f"""
    <div class='status-box'>
        🩸 <strong>정신력(HP):</strong> {st.session_state.stamina}% &nbsp;|&nbsp;
        📍 <strong>현재 위치:</strong> {st.session_state.current_room} &nbsp;|&nbsp;
        🎒 <strong>소지품:</strong> {', '.join(st.session_state.inventory) if st.session_state.inventory else '없음'}
    </div>
    """, unsafe_allow_html=True)

    # 귀신 조우 이벤트
    if st.session_state.current_ghost is not None:
        ghost = st.session_state.current_ghost
        st.error(f"⚠️ 경고! {ghost['name']}이(가) 나타났습니다!")
        st.markdown(f"<div class='story-box'>{ghost['desc']}</div>", unsafe_allow_html=True)
        st.image(ghost['image'], use_container_width=True)
        
        st.markdown("### 🚨 대처 방법을 선택하십시오!")
        c1, c2, c3 = st.columns(3)
        
        action_chosen = None
        with c1:
            if st.button("😱 숨죽이고 재빨리 숨기"):
                action_chosen = "숨죽이고 재빨리 숨기"
        with c2:
            if st.button("🙏 눈 감고 기도하기"):
                action_chosen = "눈 감고 기도하기"
        with c3:
            if st.button("💥 거울을 깨뜨리기"):
                action_chosen = "거울을 깨뜨리기"

        if action_chosen:
            if action_chosen == ghost['correct_action']:
                st.success(f"현명한 판단입니다! {ghost['name']}이(가) 어둠 속으로 사라졌습니다.")
                st.session_state.current_ghost = None
                st.rerun()
            else:
                damage = ghost['damage']
                st.session_state.stamina -= damage
                st.error(f"잘못된 선택입니다! 원혼에게 공격받아 정신력이 {damage}% 감소했습니다.")
                st.session_state.current_ghost = None
                if st.session_state.stamina <= 0:
                    st.session_state.game_over = True
                st.rerun()

    else:
        st.markdown("<hr style='border-color: #8b0000;'>", unsafe_allow_html=True)

        # [현관]
        if st.session_state.current_room == "현관":
            st.image("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80", use_container_width=True)
            st.markdown("<div class='story-box'>굳게 닫힌 거대한 목재 문입니다. 봉인을 해제하려면 4개의 탈출 도구가 모두 필요합니다.</div>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🚪 중앙 복도로 이동"):
                    st.session_state.current_room = "중앙 복도"
                    check_ghost_spawn()
                    st.rerun()
            with c2:
                if st.button("🔓 문 열기 (탈출 시도)"):
                    needed = ["녹슨 열쇠", "고대의 부적", "은빛 십자가", "의식용 소금"]
                    if all(item in st.session_state.inventory for item in needed):
                        st.session_state.escaped = True
                        st.rerun()
                    else:
                        st.error(f"봉인이 풀리지 않습니다! 필요 아이템: {', '.join(needed)}")

        # [중앙 복도]
        elif st.session_state.current_room == "중앙 복도":
            st.image("https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&q=80", use_container_width=True)
            st.markdown("<div class='story-box'>여러 갈래로 나뉘는 복도입니다. 사방에서 시선이 느껴집니다.</div>", unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                if st.button("📚 서재"):
                    st.session_state.current_room = "서재"
                    check_ghost_spawn()
                    st.rerun()
            with c2:
                if st.button("🍽️ 다이닝 룸"):
                    st.session_state.current_room = "다이닝 룸"
                    check_ghost_spawn()
                    st.rerun()
            with c3:
                if st.button("🕯️ 지하 의식실"):
                    st.session_state.current_room = "지하 의식실"
                    check_ghost_spawn()
                    st.rerun()
            with c4:
                if st.button("🏃 현관으로 돌아가기"):
                    st.session_state.current_room = "현관"
                    st.rerun()

        # [서재]
        elif st.session_state.current_room == "서재":
            st.image("https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=800&q=80", use_container_width=True)
            st.markdown("<div class='story-box'>수많은 금서들이 꽂혀있는 서재입니다. 책상 서랍에서 무언가 빛납니다.</div>", unsafe_allow_html=True)
            
            if "녹슨 열쇠" not in st.session_state.inventory:
                if st.button("🔑 책상 서랍 훔쳐보기"):
                    st.session_state.inventory.append("녹슨 열쇠")
                    st.success("아이템 획득: [녹슨 열쇠]")
                    st.rerun()
            else:
                st.info("책상 서랍은 텅 비어 있습니다.")

            if st.button("🚪 중앙 복도로 나가기"):
                st.session_state.current_room = "중앙 복도"
                check_ghost_spawn()
                st.rerun()

        # [다이닝 룸]
        elif st.session_state.current_room == "다이닝 룸":
            st.image("https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80", use_container_width=True)
            st.markdown("<div class='story-box'>썩은 음식 냄새가 진동하는 식당입니다. 식탁 위에 소금 단지가 놓여 있습니다.</div>", unsafe_allow_html=True)
            
            if "의식용 소금" not in st.session_state.inventory:
                if st.button("🧂 소금 단지 열기"):
                    st.session_state.inventory.append("의식용 소금")
                    st.success("아이템 획득: [의식용 소금]")
                    st.rerun()
            else:
                st.info("소금 단지가 엎질러져 있습니다.")

            if st.button("🚪 중앙 복도로 나가기"):
                st.session_state.current_room = "중앙 복도"
                check_ghost_spawn()
                st.rerun()

        # [지하 의식실]
        elif st.session_state.current_room == "지하 의식실":
            st.image("https://images.unsplash.com/photo-1514539079130-25950c84af65?auto=format&fit=crop&w=800&q=80", use_container_width=True)
            st.markdown("<div class='story-box'>붉은 양초로 둘러싸인 제단입니다. 마법진 위에 신성한 물건들이 놓여 있습니다.</div>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if "고대의 부적" not in st.session_state.inventory:
                    if st.button("📜 부적 집어들기"):
                        st.session_state.inventory.append("고대의 부적")
                        st.success("아이템 획득: [고대의 부적]")
                        st.rerun()
            with c2:
                if "은빛 십자가" not in st.session_state.inventory:
                    if st.button("✝️ 십자가 챙기기"):
                        st.session_state.inventory.append("은빛 십자가")
                        st.success("아이템 획득: [은빛 십자가]")
                        st.rerun()

            if st.button("🚪 중앙 복도로 올라가기"):
                st.session_state.current_room = "중앙 복도"
                check_ghost_spawn()
                st.rerun()

# 3. 게임 오버 화면
elif st.session_state.game_over:
    st.markdown("<h1 style='text-align: center; color: red;'>💥 GAME OVER 💥</h1>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1509248961158-e54f6934749c?auto=format&fit=crop&w=800&q=80", use_container_width=True)
    st.error("당신의 정신력이 한계에 도달했습니다. 영혼을 빼앗겨 영원히 이 저택을 방황하게 됩니다...")
    if st.button("🔄 다시 도전하기"):
        restart_game()
        st.rerun()

# 4. 게임 클리어 화면
elif st.session_state.escaped:
    st.balloons()
    st.markdown("<h1 style='text-align: center; color: #00ff00;'>🎉 탈출 성공! 🎉</h1>", unsafe_allow_html=True)
    st.success("4개의 성물을 이용해 봉인을 풀고 저택을 무사히 탈출했습니다! 동이 터오기 시작합니다.")
    if st.button("🔄 처음부터 다시 하기"):
        restart_game()
        st.rerun()
