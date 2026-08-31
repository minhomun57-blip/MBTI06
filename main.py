import streamlit as st
import random
import time

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

# 배경음악 (HTML audio 연동)
st.components.v1.html("""
    <audio autoplay loop hidden>
        <source src="
