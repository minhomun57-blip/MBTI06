```python
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🏚️ 저주받은 저택 - 개선판",
    layout="wide",
)

st.title("🏚️ 저주받은 저택: 개선된 호러 에디션")
st.caption(
    "W/S: 전후 이동 | A/D: 좌우 이동 | ←/→: 시점 회전 | "
    "E: 달리기 | R: 문/아이템 상호작용 | 1: 회복 | "
    "2: 손전등 강화 | 3: 퇴마부적 | 클릭: 공격"
)

horror_game_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">

<style>
html, body {
    margin: 0;
    padding: 0;
    background: #000;
    overflow: hidden;
    font-family: 'Courier New', monospace;
    user-select: none;
}

#game-wrapper {
    position: relative;
    width: 100%;
    height: 620px;
    overflow: hidden;
    background: #000;
}

#canvas {
    width: 100%;
    height: 580px;
    display: block;
    cursor: grab;
    outline: none;
}

#canvas:active {
    cursor: grabbing;
}

#ui {
    position: absolute;
    top: 15px;
    left: 15px;
    color: #d0d0d0;
    text-shadow: 2px 2px 5px #000;
    font-size: 13px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 10;
    pointer-events: none;
}

.bar-container {
    width: 220px;
    height: 12px;
    background: rgba(0,0,0,0.9);
    border: 1px solid #444;
    border-radius: 2px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    width: 100%;
    transition: width 0.05s linear;
}

#hp-bar {
    background: linear-gradient(90deg, #500, #ff0000);
}

#stamina-bar {
    background: linear-gradient(90deg, #050, #00ff44);
}

#inventory {
    position: absolute;
    bottom: 15px;
    right: 15px;
    display: flex;
    gap: 8px;
    z-index: 10;
    pointer-events: none;
}

.slot {
    width: 65px;
    height: 65px;
    border: 1px solid #333;
    background: rgba(5,5,5,0.9);
    color: #aaa;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    border-radius: 3px;
    text-align: center;
}

.slot-key {
    color: #ffaa00;
    font-size: 10px;
    margin-bottom: 2px;
    font-weight: bold;
}

#msg {
    position: absolute;
    top: 30%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #ff1111;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
    text-shadow: 0 0 10px #000;
    z-index: 10;
    pointer-events: none;
    letter-spacing: 1px;
    max-width: 80%;
}

#room-info {
    position: absolute;
    top: 15px;
    right: 15px;
    color: #aaa;
    font-size: 11px;
    text-align: right;
    z-index: 10;
    pointer-events: none;
}

#crosshair {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 12px;
    height: 12px;
    transform: translate(-50%, -50%);
    z-index: 8;
    pointer-events: none;
}

#crosshair::before,
#crosshair::after {
    content: "";
    position: absolute;
    background: rgba(255,255,255,0.7);
}

#crosshair::before {
    width: 12px;
    height: 1px;
    top: 5px;
    left: 0;
}

#crosshair::after {
    width: 1px;
    height: 12px;
    top: 0;
    left: 5px;
}

#glitch-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 7;
    opacity: 0;
    background:
        repeating-linear-gradient(
            0deg,
            rgba(255,0,0,0.18),
            rgba(255,0,0,0.18) 2px,
            transparent 2px,
            transparent 4px
        );
}

#ending,
#jumpscare {
    display: none;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 580px;
    z-index: 100;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
}

#ending {
    background:
        radial-gradient(circle, rgba(80,80,30,0.5), #020202 70%);
    color: #ffd700;
}

#ending h1 {
    font-size: 42px;
    letter-spacing: 8px;
    text-shadow: 0 0 25px #ffcc00;
}

#ending p {
    color: #ddd;
    font-size: 16px;
    line-height: 2;
}

#jumpscare {
    background: #050000;
    animation: flash-red 0.08s infinite alternate;
}

@keyframes flash-red {
    0% { background-color: #000; }
    100% { background-color: #250000; }
}

#scare-face {
    width: 340px;
    height: 400px;
    background:
        radial-gradient(circle, #800 0%, #200 50%, #000 100%);
    border-radius: 45% 45% 50% 50%;
    position: relative;
    box-shadow: 0 0 150px #f00;
    animation: violent-shake 0.015s infinite alternate;
}

.eye {
    position: absolute;
    top: 25%;
    width: 65px;
    height: 85px;
    background: #fff;
    border-radius: 50%;
    box-shadow: inset 0 0 30px #f00, 0 0 20px #ff0000;
}

.eye.left {
    left: 18%;
    transform: rotate(-15deg);
}

.eye.right {
    right: 18%;
    transform: rotate(15deg);
}

.pupil {
    position: absolute;
    top: 30%;
    left: 30%;
    width: 14px;
    height: 14px;
    background: #000;
    border-radius: 50%;
    box-shadow: 0 0 12px #f00;
}

.mouth {
    position: absolute;
    bottom: 8%;
    left: 10%;
    width: 80%;
    height: 150px;
    background: #000;
    border-radius: 10px 10px 70px 70px;
    border: 4px solid #a00;
    overflow: hidden;
}

.teeth {
    width: 100%;
    height: 35px;
    background:
        repeating-linear-gradient(
            90deg,
            #eee,
            #eee 14px,
            #200 14px,
            #200 20px
        );
}

.blood-drip {
    position: absolute;
    top: 0;
    width: 100%;
    height: 100%;
    background:
        linear-gradient(
            180deg,
            rgba(150,0,0,0.6) 0%,
            transparent 80%
        );
}

#scare-text {
    color: #ff0000;
    font-size: 28px;
    font-weight: 900;
    margin-top: 25px;
    text-shadow: 0 0 25px #ff0000;
}

.game-button {
    margin-top: 25px;
    padding: 12px 32px;
    font-size: 15px;
    background: #050505;
    color: #ff3333;
    border: 1px solid #ff0000;
    cursor: pointer;
    font-weight: bold;
}

.game-button:hover {
    background: #400;
    color: #fff;
}

@keyframes violent-shake {
    0% {
        transform: translate(10px, -10px) scale(1.1);
    }
    100% {
        transform: translate(-10px, 10px) scale(1.22);
    }
}
</style>
</head>

<body>

<div id="game-wrapper">

<div id="glitch-overlay"></div>

<div id="ui">
    <div>
        <span>생명력</span>
        <div class="bar-container">
            <div id="hp-bar" class="bar-fill"></div>
        </div>
    </div>

    <div>
        <span>스테미나</span>
        <div class="bar-container">
            <div id="stamina-bar" class="bar-fill"></div>
        </div>
    </div>

    <div>
        무기:
        <span id="weapon" style="color:#ffcc00;">맨손</span>
    </div>
</div>

<div id="room-info">
    <div
        style="color:#ff3333;font-weight:bold;"
        id="current-room-name"
    >
        현재 위치: 중앙 복도
    </div>

    <div>
        W/S 이동 · A/D 좌우 이동 · ←/→ 회전
    </div>
</div>

<div id="inventory">

    <div class="slot">
        <span class="slot-key">[1]</span>
        회복약<br>
        <span id="cnt-potion">0</span>
    </div>

    <div class="slot">
        <span class="slot-key">[2]</span>
        배터리<br>
        <span id="cnt-battery">0</span>
    </div>

    <div class="slot">
        <span class="slot-key">[3]</span>
        퇴마부적<br>
        <span id="cnt-talisman">1</span>
    </div>

    <div class="slot">
        <span class="slot-key">[4]</span>
        탈출열쇠<br>
        <span id="cnt-key">미획득</span>
    </div>

</div>

<div id="crosshair"></div>

<div id="msg">
    화면을 클릭한 뒤 W/A/S/D로 이동하세요
</div>

<div id="jumpscare">

    <div id="scare-face">

        <div class="eye left">
            <div class="pupil"></div>
        </div>

        <div class="eye right">
            <div class="pupil"></div>
        </div>

        <div class="mouth">
            <div class="teeth"></div>
            <div class="blood-drip"></div>
        </div>

    </div>

    <div id="scare-text">
        당신의 영혼은 이제 저택의 일부입니다...
    </div>

    <button
        class="game-button"
        onclick="resetGame()"
    >
        다시 도전하기
    </button>

</div>

<div id="ending">

    <h1>탈출 성공</h1>

    <p>
        피묻은 열쇠로 마지막 문을 열었습니다.<br>
        저택의 저주는 당신을 붙잡지 못했습니다.
    </p>

    <button
        class="game-button"
        onclick="resetGame()"
    >
        다시 플레이
    </button>

</div>

<canvas id="canvas" tabindex="0"></canvas>

<script>

/* =========================================================
   AUDIO
========================================================= */

const AudioContext =
    window.AudioContext ||
    window.webkitAudioContext;

let audioCtx = null;

function initAudio() {

    if (!audioCtx) {
        audioCtx = new AudioContext();
    }

    if (audioCtx.state === "suspended") {
        audioCtx.resume();
    }
}

function playSound(type) {

    if (!audioCtx) return;

    const now = audioCtx.currentTime;

    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();

    if (type === "attack") {

        osc.type = "sawtooth";

        osc.frequency.setValueAtTime(
            140,
            now
        );

        osc.frequency.exponentialRampToValueAtTime(
            30,
            now + 0.15
        );

        gain.gain.setValueAtTime(
            0.4,
            now
        );

        gain.gain.exponentialRampToValueAtTime(
            0.01,
            now + 0.15
        );

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(now + 0.15);
    }

    else if (type === "hit") {

        osc.type = "square";

        osc.frequency.setValueAtTime(
            80,
            now
        );

        osc.frequency.exponentialRampToValueAtTime(
            15,
            now + 0.2
        );

        gain.gain.setValueAtTime(
            0.5,
            now
        );

        gain.gain.exponentialRampToValueAtTime(
            0.01,
            now + 0.2
        );

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(now + 0.2);
    }

    else if (type === "item") {

        osc.type = "sine";

        osc.frequency.setValueAtTime(
            520,
            now
        );

        osc.frequency.exponentialRampToValueAtTime(
            1040,
            now + 0.18
        );

        gain.gain.setValueAtTime(
            0.3,
            now
        );

        gain.gain.exponentialRampToValueAtTime(
            0.01,
            now + 0.18
        );

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(now + 0.18);
    }

    else if (type === "door") {

        osc.type = "triangle";

        osc.frequency.setValueAtTime(
            120,
            now
        );

        osc.frequency.linearRampToValueAtTime(
            60,
            now + 0.3
        );

        gain.gain.setValueAtTime(
            0.4,
            now
        );

        gain.gain.exponentialRampToValueAtTime(
            0.01,
            now + 0.3
        );

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(now + 0.3);
    }

    else if (type === "jumpscare") {

        osc.type = "sawtooth";

        osc.frequency.setValueAtTime(
            180,
            now
        );

        osc.frequency.linearRampToValueAtTime(
            1100,
            now + 0.08
        );

        osc.frequency.linearRampToValueAtTime(
            60,
            now + 1.2
        );

        gain.gain.setValueAtTime(
            1,
            now
        );

        gain.gain.exponentialRampToValueAtTime(
            0.01,
            now + 1.2
        );

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(now + 1.2);
    }
}


/* =========================================================
   CANVAS
========================================================= */

const canvas =
    document.getElementById("canvas");

const ctx =
    canvas.getContext("2d");

canvas.width = 800;
canvas.height = 580;


/* =========================================================
   TEXTURES
========================================================= */

const wallTex =
    document.createElement("canvas");

wallTex.width = 64;
wallTex.height = 64;

const wCtx =
    wallTex.getContext("2d");

wCtx.fillStyle = "#2d1d1a";
wCtx.fillRect(0, 0, 64, 64);

wCtx.fillStyle = "#140a08";

for (let i = 0; i < 64; i += 16) {

    wCtx.fillRect(
        0,
        i,
        64,
        2
    );

    for (let j = 0; j < 64; j += 16) {

        const offset =
            (i / 16) % 2 === 0
                ? 0
                : 8;

        wCtx.fillRect(
            j + offset,
            i,
            2,
            16
        );
    }
}


const doorTex =
    document.createElement("canvas");

doorTex.width = 64;
doorTex.height = 64;

const dCtx =
    doorTex.getContext("2d");

dCtx.fillStyle = "#221108";
dCtx.fillRect(0, 0, 64, 64);

dCtx.fillStyle = "#4a2b16";
dCtx.fillRect(3, 3, 58, 58);

dCtx.fillStyle = "#3a200f";

for (let x = 4; x < 60; x += 6) {
    dCtx.fillRect(
        x,
        4,
        2,
        56
    );
}


/* 문 패널 */

function drawPanel(px, py, pw, ph) {

    dCtx.fillStyle = "#1e0d05";

    dCtx.fillRect(
        px,
        py,
        pw,
        ph
    );

    dCtx.fillStyle = "#5c381d";

    dCtx.fillRect(
        px + 2,
        py + 2,
        pw - 4,
        ph - 4
    );

    dCtx.fillStyle = "#361d0d";

    dCtx.fillRect(
        px + 4,
        py + 4,
        pw - 8,
        ph - 8
    );
}

drawPanel(8, 8, 21, 22);
drawPanel(35, 8, 21, 22);
drawPanel(8, 34, 21, 22);
drawPanel(35, 34, 21, 22);


/* =========================================================
   MAP
========================================================= */

const initialMap = [

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

[1,0,0,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,0,0,1],

[1,0,0,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,0,0,1],

[1,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,1],

[1,1,1,1,1,0,1,1,2,1,1,1,2,1,1,0,1,1,1,1,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],

[1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1],

[1,0,1,0,0,0,2,0,1,0,0,0,1,0,2,0,0,0,1,0,1],

[1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1],

[1,0,1,1,2,1,1,0,0,0,0,0,0,0,1,1,2,1,1,0,1],

[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],

[1,0,1,1,2,1,1,0,0,0,0,0,0,0,1,1,2,1,1,0,1],

[1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1],

[1,0,1,0,0,0,2,0,1,0,0,0,1,0,2,0,0,0,1,0,1],

[1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],

[1,1,1,1,1,0,1,1,2,1,1,1,2,1,1,0,1,1,1,1,1],

[1,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,1],

[1,0,0,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,0,0,1],

[1,0,0,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,0,3,1],

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

];

const MAP_SIZE = initialMap.length;


/* =========================================================
   GAME STATE
========================================================= */

let houseMap;

let px;
let py;

let angle;

let hp;
let stamina;

let flashRange;

let gameOver;

let gameWon;

let items;

let isAttacking;

let ghosts;

let worldItems;

let furnitureList;

let zBuffer =
    new Array(160).fill(0);

let screenShake = 0;

let animTimer = 0;

const fov = Math.PI * 0.42;


/* =========================================================
   GAME INITIALIZATION
========================================================= */

function initGame() {

    houseMap =
        JSON.parse(
            JSON.stringify(initialMap)
        );

    px = 10.5;
    py = 10.5;

    angle = 0;

    hp = 100;
    stamina = 100;

    flashRange = 12;

    gameOver = false;
    gameWon = false;

    isAttacking = 0;

    items = {
        potion: 0,
        battery: 0,
        talisman: 1,
        key: false,
        knife: false
    };


    ghosts = [

        {
            x: 2.5,
            y: 2.5,
            hp: 100,
            stun: 0
        },

        {
            x: 18.5,
            y: 2.5,
            hp: 100,
            stun: 0
        },

        {
            x: 2.5,
            y: 18.5,
            hp: 100,
            stun: 0
        }

    ];


    worldItems = [

        {
            x: 2.5,
            y: 1.5,
            type: "knife",
            name: "녹슨 단검"
        },

        {
            x: 18.5,
            y: 1.5,
            type: "potion",
            name: "의용 회복제"
        },

        {
            x: 1.5,
            y: 8.5,
            type: "battery",
            name: "고전압 배터리"
        },

        {
            x: 19.5,
            y: 8.5,
            type: "potion",
            name: "의용 회복제"
        },

        {
            x: 1.5,
            y: 13.5,
            type: "battery",
            name: "고전압 배터리"
        },

        {
            x: 18.5,
            y: 18.5,
            type: "key",
            name: "피묻은 열쇠"
        }

    ];


    furnitureList = [

        {
            x: 1.5,
            y: 2.5,
            type: "bookshelf",
            name: "오래된 책장",
            radius: 0.45
        },

        {
            x: 3.5,
            y: 1.5,
            type: "desk",
            name: "나무 책상",
            radius: 0.55
        },

        {
            x: 3.5,
            y: 2.2,
            type: "chair",
            name: "낡은 의자",
            radius: 0.3
        },

        {
            x: 19.5,
            y: 2.5,
            type: "bed",
            name: "녹슨 침대",
            radius: 0.7
        },

        {
            x: 17.5,
            y: 1.5,
            type: "cabinet",
            name: "약품 보관함",
            radius: 0.45
        },

        {
            x: 9.5,
            y: 10.5,
            type: "clock",
            name: "괘종시계",
            radius: 0.35
        },

        {
            x: 11.5,
            y: 10.5,
            type: "chair",
            name: "복도 의자",
            radius: 0.3
        },

        {
            x: 10.5,
            y: 6.5,
            type: "candelabra",
            name: "촛대",
            radius: 0.2
        },

        {
            x: 10.5,
            y: 14.5,
            type: "candelabra",
            name: "촛대",
            radius: 0.2
        },

        {
            x: 1.5,
            y: 18.5,
            type: "bed",
            name: "핏자국이 남은 침대",
            radius: 0.7
        },

        {
            x: 3.5,
            y: 19.5,
            type: "bookshelf",
            name: "작은 책장",
            radius: 0.45
        },

        {
            x: 19.5,
            y: 17.5,
            type: "cabinet",
            name: "철제 보관함",
            radius: 0.45
        },

        {
            x: 17.5,
            y: 19.5,
            type: "desk",
            name: "실험용 책상",
            radius: 0.55
        }

    ];


    document.getElementById(
        "jumpscare"
    ).style.display = "none";

    document.getElementById(
        "ending"
    ).style.display = "none";

    document.getElementById(
        "msg"
    ).innerText =
        "문이나 아이템 가까이에서 R을 누르세요";

    document.getElementById(
        "msg"
    ).style.color = "#ff3333";

    updateUI();
}

function resetGame() {
    initGame();
}


/* =========================================================
   INPUT
========================================================= */

const keys = {};


window.addEventListener(
    "keydown",
    function(e) {

        /*
         * e.code 사용:
         * 한글 입력 상태에서도
         * 물리적인 키 위치를 안정적으로 인식
         */

        switch (e.code) {

            case "KeyW":
                keys.w = true;
                break;

            case "KeyA":
                keys.a = true;
                break;

            case "KeyS":
                keys.s = true;
                break;

            case "KeyD":
                keys.d = true;
                break;

            case "KeyE":
                keys.e = true;
                break;

            case "KeyR":
                keys.r = true;

                if (!gameOver) {
                    handleInteract();
                }

                break;
        }


        if (
            e.code === "ArrowLeft"
        ) {
            keys.left = true;
            e.preventDefault();
        }

        if (
            e.code === "ArrowRight"
        ) {
            keys.right = true;
            e.preventDefault();
        }

        if (
            e.code === "ArrowUp" ||
            e.code === "ArrowDown"
        ) {
            e.preventDefault();
        }


        if (e.key === "1" && !gameOver) {

            if (items.potion > 0) {

                hp =
                    Math.min(
                        100,
                        hp + 60
                    );

                items.potion--;

                playSound("item");

                showTmpMsg(
                    "💊 체력을 회복했습니다."
                );

                updateUI();
            }
        }


        if (e.key === "2" && !gameOver) {

            if (items.battery > 0) {

                flashRange = 16;

                items.battery--;

                playSound("item");

                showTmpMsg(
                    "🔋 손전등 출력이 강화되었습니다."
                );

                updateUI();
            }
        }


        if (e.key === "3" && !gameOver) {

            if (items.talisman > 0) {

                ghosts.forEach(
                    function(g) {

                        g.stun = 200;

                        const dx =
                            g.x - px;

                        const dy =
                            g.y - py;

                        g.x += dx * 0.5;
                        g.y += dy * 0.5;
                    }
                );

                items.talisman--;

                playSound("item");

                screenShake = 12;

                showTmpMsg(
                    "📜 부적으로 주변의 원혼을 퇴마했습니다!"
                );

                updateUI();
            }
        }

    }
);


window.addEventListener(
    "keyup",
    function(e) {

        switch (e.code) {

            case "KeyW":
                keys.w = false;
                break;

            case "KeyA":
                keys.a = false;
                break;

            case "KeyS":
                keys.s = false;
                break;

            case "KeyD":
                keys.d = false;
                break;

            case "KeyE":
                keys.e = false;
                break;
        }


        if (
            e.code === "ArrowLeft"
        ) {
            keys.left = false;
        }

        if (
            e.code === "ArrowRight"
        ) {
            keys.right = false;
        }

    }
);


/* =========================================================
   MOUSE
========================================================= */

let isMouseDown = false;
let lastMouseX = 0;

canvas.addEventListener(
    "mousedown",
    function(e) {

        initAudio();

        canvas.focus();

        isMouseDown = true;

        lastMouseX = e.clientX;


        if (
            items.knife &&
            isAttacking === 0 &&
            !gameOver
        ) {

            isAttacking = 10;

            playSound("attack");

            checkAttackHit();
        }

    }
);


window.addEventListener(
    "mouseup",
    function() {
        isMouseDown = false;
    }
);


window.addEventListener(
    "mousemove",
    function(e) {

        if (isMouseDown && !gameOver) {

            const dx =
                e.clientX - lastMouseX;

            angle += dx * 0.006;

            lastMouseX =
                e.clientX;
        }

    }
);


/* =========================================================
   MESSAGE
========================================================= */

function showTmpMsg(txt) {

    const msgEl =
        document.getElementById("msg");

    msgEl.innerText = txt;

    setTimeout(
        function() {

            if (
                !gameOver &&
                msgEl.innerText === txt
            ) {
                msgEl.innerText = "";
            }

        },
        2500
    );
}


/* =========================================================
   COLLISION
========================================================= */

function isWall(x, y) {

    if (
        x < 0 ||
        x >= MAP_SIZE ||
        y < 0 ||
        y >= MAP_SIZE
    ) {
        return true;
    }

    const tile =
        houseMap[
            Math.floor(y)
        ][
            Math.floor(x)
        ];

    return (
        tile === 1 ||
        tile === 2
    );
}


function isFurnitureCollision(x, y) {

    for (
        let i = 0;
        i < furnitureList.length;
        i++
    ) {

        const f =
            furnitureList[i];

        /*
         * 촛대는 충돌하지 않게 처리
         */
        if (
            f.type === "candelabra"
        ) {
            continue;
        }

        const dx =
            x - f.x;

        const dy =
            y - f.y;

        const dist =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        if (
            dist <
            f.radius + 0.22
        ) {
            return true;
        }
    }

    return false;
}


function isSolid(x, y) {

    return (
        isWall(x, y) ||
        isFurnitureCollision(x, y)
    );
}


/*
 * X/Y를 따로 검사해서
 * 벽 모서리에 끼이는 현상을 줄인다.
 */

function movePlayer(dx, dy) {

    const margin = 0.22;

    const newX =
        px + dx;

    const newY =
        py + dy;


    if (
        !isSolid(
            newX + Math.sign(dx) * margin,
            py
        )
    ) {
        px = newX;
    }


    if (
        !isSolid(
            px,
            newY + Math.sign(dy) * margin
        )
    ) {
        py = newY;
    }
}


/* =========================================================
   INTERACTION
========================================================= */

function findNearbyDoor() {

    let best = null;
    let bestDist = 1.45;

    for (
        let y = 0;
        y < MAP_SIZE;
        y++
    ) {

        for (
            let x = 0;
            x < MAP_SIZE;
            x++
        ) {

            const tile =
                houseMap[y][x];

            if (
                tile !== 2 &&
                tile !== 3
            ) {
                continue;
            }

            const cx =
                x + 0.5;

            const cy =
                y + 0.5;

            const dist =
                Math.hypot(
                    px - cx,
                    py - cy
                );

            if (
                dist < bestDist
            ) {

                bestDist = dist;

                best = {
                    x: x,
                    y: y,
                    tile: tile
                };
            }
        }
    }

    return best;
}


function findNearbyItem() {

    let bestIndex = -1;
    let bestDist = 1.5;

    for (
        let i = 0;
        i < worldItems.length;
        i++
    ) {

        const item =
            worldItems[i];

        const dist =
            Math.hypot(
                px - item.x,
                py - item.y
            );

        if (
            dist < bestDist
        ) {

            bestDist = dist;
            bestIndex = i;
        }
    }

    return bestIndex;
}


function handleInteract() {

    if (gameOver) {
        return;
    }


    const door =
        findNearbyDoor();


    if (door) {

        if (door.tile === 2) {

            houseMap[
                door.y
            ][
                door.x
            ] = 0;

            playSound("door");

            showTmpMsg(
                "🚪 문을 열었습니다."
            );

            return;
        }


        if (door.tile === 3) {

            if (items.key) {

                gameWon = true;
                gameOver = true;

                playSound("door");

                document.getElementById(
                    "ending"
                ).style.display = "flex";

            } else {

                showTmpMsg(
                    "🔒 잠긴 문입니다. 피묻은 열쇠가 필요합니다."
                );
            }

            return;
        }
    }


    const itemIndex =
        findNearbyItem();


    if (itemIndex !== -1) {

        const item =
            worldItems[itemIndex];

        playSound("item");


        if (
            item.type === "key"
        ) {

            items.key = true;

            showTmpMsg(
                "🔑 피묻은 열쇠를 획득했습니다! 탈출문을 찾으세요."
            );
        }


        else if (
            item.type === "knife"
        ) {

            items.knife = true;

            showTmpMsg(
                "🗡️ 녹슨 단검을 획득했습니다."
            );
        }


        else if (
            item.type === "potion"
        ) {

            items.potion++;

            showTmpMsg(
                "💊 회복제를 획득했습니다."
            );
        }


        else if (
            item.type === "battery"
        ) {

            items.battery++;

            showTmpMsg(
                "🔋 배터리를 획득했습니다."
            );
        }


        worldItems.splice(
            itemIndex,
            1
        );

        updateUI();

        return;
    }


    showTmpMsg(
        "상호작용할 대상이 가까이에 없습니다."
    );
}


/* =========================================================
   ATTACK
========================================================= */

function checkAttackHit() {

    ghosts.forEach(
        function(g) {

            if (g.hp <= 0) {
                return;
            }


            const gdx =
                g.x - px;

            const gdy =
                g.y - py;

            const dist =
                Math.sqrt(
                    gdx * gdx +
                    gdy * gdy
                );


            let gAngle =
                Math.atan2(
                    gdy,
                    gdx
                ) - angle;


            while (
                gAngle < -Math.PI
            ) {
                gAngle +=
                    2 * Math.PI;
            }


            while (
                gAngle > Math.PI
            ) {
                gAngle -=
                    2 * Math.PI;
            }


            if (
                dist < 2.0 &&
                Math.abs(gAngle) < 0.7
            ) {

                g.hp -= 50;

                g.stun = 50;

                playSound("hit");

                screenShake = 8;


                if (
                    g.hp <= 0
                ) {

                    showTmpMsg(
                        "💀 원혼을 성불시켰습니다!"
                    );
                }
            }

        }
    );
}


/* =========================================================
   UI
========================================================= */

function updateUI() {

    document.getElementById(
        "hp-bar"
    ).style.width =
        Math.max(0, hp) + "%";


    document.getElementById(
        "stamina-bar"
    ).style.width =
        Math.max(0, stamina) + "%";


    document.getElementById(
        "weapon"
    ).innerText =
        items.knife
            ? "녹슨 단검 (클릭: 베기)"
            : "맨손";


    document.getElementById(
        "cnt-potion"
    ).innerText =
        items.potion;


    document.getElementById(
        "cnt-battery"
    ).innerText =
        items.battery;


    document.getElementById(
        "cnt-talisman"
    ).innerText =
        items.talisman;


    document.getElementById(
        "cnt-key"
    ).innerText =
        items.key
            ? "획득완료"
            : "미획득";
}


/* =========================================================
   JUMPSCARE
========================================================= */

function triggerJumpscare() {

    gameOver = true;

    playSound("jumpscare");

    document.getElementById(
        "jumpscare"
    ).style.display = "flex";
}


/* =========================================================
   ROOM NAME
========================================================= */

function updateRoomName() {

    const curX =
        Math.floor(px);

    const curY =
        Math.floor(py);

    let roomTxt =
        "중앙 복도";


    if (
        curX < 4 &&
        curY < 4
    ) {

        roomTxt =
            "북서쪽 서재";
    }

    else if (
        curX > 16 &&
        curY < 4
    ) {

        roomTxt =
            "북동쪽 응급실";
    }

    else if (
        curX < 4 &&
        curY > 16
    ) {

        roomTxt =
            "남서쪽 침실";
    }

    else if (
        curX > 16 &&
        curY > 16
    ) {

        roomTxt =
            "남동쪽 지하 밀실";
    }


    document.getElementById(
        "current-room-name"
    ).innerText =
        "현재 위치: " + roomTxt;
}


/* =========================================================
   GAME UPDATE
========================================================= */

function update() {

    if (gameOver) {
        return;
    }


    animTimer += 0.05;


    if (
        screenShake > 0
    ) {
        screenShake--;
    }


    /*
     * 회전
     */

    if (keys.left) {
        angle -= 0.045;
    }

    if (keys.right) {
        angle += 0.045;
    }


    /*
     * 이동 속도
     */

    let speed =
        0.038;


    if (
        keys.e &&
        stamina > 0
    ) {

        speed =
            0.068;

        stamina =
            Math.max(
                0,
                stamina - 0.5
            );

    } else {

        stamina =
            Math.min(
                100,
                stamina + 0.22
            );
    }


    /*
     * 전후 이동
     */

    let forward =
        0;

    if (keys.w) {
        forward += 1;
    }

    if (keys.s) {
        forward -= 1;
    }


    /*
     * 좌우 이동
     */

    let strafe =
        0;

    if (keys.d) {
        strafe += 1;
    }

    if (keys.a) {
        strafe -= 1;
    }


    if (
        forward !== 0 ||
        strafe !== 0
    ) {

        let dx =
            Math.cos(angle) *
            forward *
            speed;

        let dy =
            Math.sin(angle) *
            forward *
            speed;


        dx +=
            Math.cos(
                angle + Math.PI / 2
            ) *
            strafe *
            speed;


        dy +=
            Math.sin(
                angle + Math.PI / 2
            ) *
            strafe *
            speed;


        movePlayer(
            dx,
            dy
        );
    }


    updateRoomName();


    /*
     * 유령 AI
     */

    let minDist =
        999;


    ghosts.forEach(
        function(g) {

            if (g.hp <= 0) {
                return;
            }


            const gdx =
                px - g.x;

            const gdy =
                py - g.y;


            const dist =
                Math.sqrt(
                    gdx * gdx +
                    gdy * gdy
                );


            minDist =
                Math.min(
                    minDist,
                    dist
                );


            if (g.stun > 0) {

                g.stun--;

                return;
            }


            /*
             * 플레이어와 가까울수록
             * 유령이 조금 빨라짐
             */

            let ghostSpeed =
                dist < 5
                    ? 0.024
                    : 0.016;


            if (
                dist > 0.1
            ) {

                const moveX =
                    (gdx / dist) *
                    ghostSpeed;

                const moveY =
                    (gdy / dist) *
                    ghostSpeed;


                if (
                    !isSolid(
                        g.x + moveX,
                        g.y
                    )
                ) {

                    g.x += moveX;
                }


                if (
                    !isSolid(
                        g.x,
                        g.y + moveY
                    )
                ) {

                    g.y += moveY;
                }
            }


            /*
             * 공격 쿨다운 대신
             * 근접 상태에서 지속 피해
             */

            if (
                dist < 0.6
            ) {

                hp -= 1.5;

                screenShake = 5;


                if (
                    hp <= 0
                ) {

                    hp = 0;

                    triggerJumpscare();
                }
            }

        }
    );


    /*
     * 유령 접근 시 글리치
     */

    if (
        minDist < 5.5
    ) {

        document.getElementById(
            "glitch-overlay"
        ).style.opacity =
            (
                5.5 - minDist
            ) /
            5.5 *
            0.75;

    } else {

        document.getElementById(
            "glitch-overlay"
        ).style.opacity = 0;
    }


    if (
        isAttacking > 0
    ) {
        isAttacking--;
    }


    updateUI();
}


/* =========================================================
   ITEM DRAWING
========================================================= */

function draw3DItem(
    type,
    sx,
    sy,
    size
) {

    ctx.save();

    ctx.translate(
        sx,
        sy
    );


    if (type === "key") {

        ctx.fillStyle =
            "#ffd700";

        ctx.beginPath();

        ctx.arc(
            0,
            -size / 3,
            size / 3,
            0,
            Math.PI * 2
        );

        ctx.fill();


        ctx.fillStyle =
            "#111";

        ctx.beginPath();

        ctx.arc(
            0,
            -size / 3,
            size / 6,
            0,
            Math.PI * 2
        );

        ctx.fill();


        ctx.fillStyle =
            "#ffd700";

        ctx.fillRect(
            -size / 12,
            -size / 6,
            size / 6,
            size / 1.2
        );

        ctx.fillRect(
            size / 12,
            size / 4,
            size / 4,
            size / 8
        );

        ctx.fillRect(
            size / 12,
            size / 2.2,
            size / 4,
            size / 8
        );

    }


    else if (type === "knife") {

        ctx.fillStyle =
            "#888";

        ctx.beginPath();

        ctx.moveTo(
            0,
            -size / 1.5
        );

        ctx.lineTo(
            size / 6,
            size / 6
        );

        ctx.lineTo(
            -size / 6,
            size / 6
        );

        ctx.closePath();

        ctx.fill();


        ctx.fillStyle =
            "#4a2511";

        ctx.fillRect(
            -size / 4,
            size / 6,
            size / 2,
            size / 10
        );

        ctx.fillStyle =
            "#2b1408";

        ctx.fillRect(
            -size / 8,
            size / 6 + size / 10,
            size / 4,
            size / 2.5
        );
    }


    else if (type === "potion") {

        ctx.fillStyle =
            "#ff1133";

        ctx.beginPath();

        ctx.arc(
            0,
            size / 4,
            size / 2.2,
            0,
            Math.PI * 2
        );

        ctx.fill();


        ctx.fillStyle =
            "#8b5a2b";

        ctx.fillRect(
            -size / 6,
            -size / 3,
            size / 3,
            size / 6
        );
    }


    else if (type === "battery") {

        ctx.fillStyle =
            "#222";

        ctx.fillRect(
            -size / 3,
            -size / 3,
            size / 1.5,
            size / 1.2
        );

        ctx.fillStyle =
            "#ff6600";

        ctx.fillRect(
            -size / 3,
            0,
            size / 1.5,
            size / 2.4
        );

        ctx.fillStyle =
            "#fff";

        ctx.font =
            `bold ${Math.max(
                10,
                Math.floor(size / 3)
            )}px sans-serif`;

        ctx.textAlign =
            "center";

        ctx.fillText(
            "⚡",
            0,
            size / 5
        );
    }


    ctx.restore();
}


/* =========================================================
   FURNITURE
========================================================= */

function drawFurniture(
    type,
    sx,
    sy,
    size
) {

    ctx.save();

    ctx.translate(
        sx,
        sy
    );


    if (
        type === "bookshelf"
    ) {

        ctx.fillStyle =
            "#3a200d";

        ctx.fillRect(
            -size / 2,
            -size / 1.2,
            size,
            size * 1.2
        );

        ctx.fillStyle =
            "#1e0f06";

        ctx.fillRect(
            -size / 2.3,
            -size / 1.3,
            size / 1.15,
            size * 1.1
        );

    }


    else if (
        type === "desk"
    ) {

        ctx.fillStyle =
            "#422817";

        ctx.fillRect(
            -size / 1.3,
            -size / 4,
            size * 1.5,
            size / 6
        );

        ctx.fillRect(
            -size / 1.4,
            -size / 8,
            size / 8,
            size / 1.5
        );

        ctx.fillRect(
            size / 1.6,
            -size / 8,
            size / 8,
            size / 1.5
        );

    }


    else if (
        type === "chair"
    ) {

        ctx.fillStyle =
            "#3a200d";

        ctx.fillRect(
            -size / 4,
            -size / 1.2,
            size / 2,
            size / 1.8
        );

        ctx.fillRect(
            -size / 3,
            -size / 3,
            size / 1.5,
            size / 8
        );

    }


    else if (
        type === "bed"
    ) {

        ctx.fillStyle =
            "#4a2e1b";

        ctx.fillRect(
            -size / 1.2,
            -size / 6,
            size * 1.6,
            size / 2
        );

        ctx.fillStyle =
            "#aaa";

        ctx.fillRect(
            -size / 1.1,
            -size / 4,
            size * 1.4,
            size / 4
        );

    }


    else if (
        type === "cabinet"
    ) {

        ctx.fillStyle =
            "#333b42";

        ctx.fillRect(
            -size / 3,
            -size / 1.1,
            size / 1.5,
            size * 1.1
        );

    }


    else if (
        type === "clock"
    ) {

        ctx.fillStyle =
            "#2d1a0e";

        ctx.fillRect(
            -size / 4,
            -size,
            size / 2,
            size * 1.3
        );

        ctx.fillStyle =
            "#ffeecc";

        ctx.beginPath();

        ctx.arc(
            0,
            -size / 1.3,
            size / 6,
            0,
            Math.PI * 2
        );

        ctx.fill();

    }


    else if (
        type === "candelabra"
    ) {

        ctx.fillStyle =
            "#887711";

        ctx.fillRect(
            -size / 16,
            -size / 2,
            size / 8,
            size / 1.2
        );

        ctx.fillStyle =
            "#ffaa00";

        ctx.beginPath();

        ctx.arc(
            0,
            -size / 1.8,
            size / 8,
            0,
            Math.PI * 2
        );

        ctx.fill();

        const flicker =
            Math.sin(
                animTimer * 10
            ) * 2;

        ctx.fillStyle =
            "#ffff66";

        ctx.beginPath();

        ctx.arc(
            0,
            -size / 1.4 + flicker,
            size / 12,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }


    ctx.restore();
}


/* =========================================================
   GHOST
========================================================= */

function drawGhost(
    sx,
    sy,
    size,
    stun
) {

    ctx.save();

    ctx.translate(
        sx,
        sy
    );


    const alpha =
        stun > 0
            ? 0.4
            : 0.85;


    ctx.fillStyle =
        `rgba(200,220,255,${alpha})`;


    ctx.beginPath();

    ctx.arc(
        0,
        -size / 2,
        size / 3,
        Math.PI,
        0
    );

    ctx.lineTo(
        size / 3,
        size / 2
    );

    ctx.lineTo(
        -size / 3,
        size / 2
    );

    ctx.closePath();

    ctx.fill();


    ctx.fillStyle =
        stun > 0
            ? "#00ffff"
            : "#ff0000";


    ctx.beginPath();

    ctx.arc(
        -size / 8,
        -size / 1.8,
        size / 12,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.beginPath();

    ctx.arc(
        size / 8,
        -size / 1.8,
        size / 12,
        0,
        Math.PI * 2
    );

    ctx.fill();


    ctx.restore();
}


/* =========================================================
   WEAPON
========================================================= */

function drawWeapon() {

    if (!items.knife) {
        return;
    }


    ctx.save();


    const swingOffset =
        isAttacking > 0
            ? (10 - isAttacking) * 8
            : 0;


    const weaponX =
        canvas.width -
        150 -
        swingOffset;


    const weaponY =
        canvas.height -
        100 +
        swingOffset;


    ctx.translate(
        weaponX,
        weaponY
    );


    ctx.rotate(
        -Math.PI / 4 +
        swingOffset * 0.05
    );


    ctx.fillStyle =
        "#aaa";

    ctx.fillRect(
        -10,
        -120,
        20,
        100
    );


    ctx.fillStyle =
        "#fff";

    ctx.fillRect(
        0,
        -120,
        10,
        100
    );


    ctx.fillStyle =
        "#4a2511";

    ctx.fillRect(
        -20,
        -20,
        40,
        10
    );


    ctx.fillStyle =
        "#2b1408";

    ctx.fillRect(
        -8,
        -10,
        16,
        40
    );


    ctx.restore();
}


/* =========================================================
   RENDER
========================================================= */

function render() {

    ctx.save();


    if (
        screenShake > 0
    ) {

        ctx.translate(
            (Math.random() - 0.5) *
                screenShake,

            (Math.random() - 0.5) *
                screenShake
        );
    }


    /*
     * 천장
     */

    const ceilGrd =
        ctx.createLinearGradient(
            0,
            0,
            0,
            canvas.height / 2
        );

    ceilGrd.addColorStop(
        0,
        "#0a0a0a"
    );

    ceilGrd.addColorStop(
        1,
        "#221515"
    );

    ctx.fillStyle =
        ceilGrd;

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height / 2
    );


    /*
     * 바닥
     */

    const floorGrd =
        ctx.createLinearGradient(
            0,
            canvas.height / 2,
            0,
            canvas.height
        );

    floorGrd.addColorStop(
        0,
        "#1c1010"
    );

    floorGrd.addColorStop(
        1,
        "#050505"
    );

    ctx.fillStyle =
        floorGrd;

    ctx.fillRect(
        0,
        canvas.height / 2,
        canvas.width,
        canvas.height / 2
    );


    const numRays = 160;

    const w =
        canvas.width /
        numRays;


    const curFlashRange =
        flashRange +
        (Math.random() - 0.5) *
        0.2;


    const projDist =
        (canvas.width / 2) /
        Math.tan(fov / 2);


    /*
     * 레이캐스팅
     */

    for (
        let i = 0;
        i < numRays;
        i++
    ) {

        const rayAngle =
            angle -
            fov / 2 +
            (i / numRays) * fov;


        let distance = 0;

        let hit = false;

        let hitType = 1;

        let wallX = 0;


        while (
            !hit &&
            distance <
            curFlashRange
        ) {

            distance += 0.025;


            const rx =
                px +
                Math.cos(rayAngle) *
                distance;


            const ry =
                py +
                Math.sin(rayAngle) *
                distance;


            const tx =
                Math.floor(rx);


            const ty =
                Math.floor(ry);


            if (
                tx < 0 ||
                tx >= MAP_SIZE ||
                ty < 0 ||
                ty >= MAP_SIZE
            ) {

                hit = true;

                hitType = 1;

            }

            else if (
                houseMap[ty][tx] > 0
            ) {

                hit = true;

                hitType =
                    houseMap[ty][tx];


                wallX =
                    (
                        rx - tx +
                        ry - ty
                    );

                wallX =
                    (
                        wallX -
                        Math.floor(wallX)
                    ) * 64;
            }
        }


        const correctedDist =
            distance *
            Math.cos(
                rayAngle - angle
            );


        zBuffer[i] =
            correctedDist;


        const h =
            Math.min(
                canvas.height,
                projDist /
                (correctedDist + 0.0001)
            );


        const shade =
            Math.max(
                0.15,
                1 -
                correctedDist /
                curFlashRange
            );


        if (
            hitType === 3
        ) {

            ctx.fillStyle =
                `rgba(230,190,60,${shade})`;

            ctx.fillRect(
                i * w,
                (canvas.height - h) / 2,
                w + 1,
                h
            );

        }

        else if (
            hitType === 2
        ) {

            ctx.drawImage(
                doorTex,
                Math.floor(wallX),
                0,
                1,
                64,
                i * w,
                (canvas.height - h) / 2,
                w + 1,
                h
            );

            ctx.fillStyle =
                `rgba(0,0,0,${1-shade})`;

            ctx.fillRect(
                i * w,
                (canvas.height - h) / 2,
                w + 1,
                h
            );

        }

        else {

            ctx.drawImage(
                wallTex,
                Math.floor(wallX),
                0,
                1,
                64,
                i * w,
                (canvas.height - h) / 2,
                w + 1,
                h
            );

            ctx.fillStyle =
                `rgba(0,0,0,${1-shade})`;

            ctx.fillRect(
                i * w,
                (canvas.height - h) / 2,
                w + 1,
                h
            );
        }
    }


    /*
     * 가구
     */

    furnitureList.forEach(
        function(furn) {

            const idxX =
                furn.x - px;

            const idxY =
                furn.y - py;


            const dist =
                Math.sqrt(
                    idxX * idxX +
                    idxY * idxY
                );


            let fAngle =
                Math.atan2(
                    idxY,
                    idxX
                ) - angle;


            while (
                fAngle < -Math.PI
            ) {
                fAngle +=
                    2 * Math.PI;
            }


            while (
                fAngle > Math.PI
            ) {
                fAngle -=
                    2 * Math.PI;
            }


            if (
                Math.abs(fAngle) <
                    fov / 1.8 &&
                dist <
                    curFlashRange
            ) {

                const sx =
                    canvas.width / 2 +
                    Math.tan(fAngle) *
                    projDist;


                const rayIndex =
                    Math.floor(
                        sx /
                        canvas.width *
                        numRays
                    );


                if (
                    rayIndex >= 0 &&
                    rayIndex < numRays &&
                    dist <
                        zBuffer[rayIndex]
                ) {

                    const size =
                        Math.min(
                            180,
                            projDist *
                            0.55 /
                            dist
                        );


                    const centerY =
                        canvas.height / 2 +
                        size / 2;


                    drawFurniture(
                        furn.type,
                        sx,
                        centerY,
                        size
                    );
                }
            }
        }
    );


    /*
     * 아이템
     */

    worldItems.forEach(
        function(item) {

            const idxX =
                item.x - px;

            const idxY =
                item.y - py;


            const dist =
                Math.sqrt(
                    idxX * idxX +
                    idxY * idxY
                );


            let itemAngle =
                Math.atan2(
                    idxY,
                    idxX
                ) - angle;


            while (
                itemAngle < -Math.PI
            ) {
                itemAngle +=
                    2 * Math.PI;
            }


            while (
                itemAngle > Math.PI
            ) {
                itemAngle -=
                    2 * Math.PI;
            }


            if (
                Math.abs(itemAngle) <
                    fov / 1.8 &&
                dist <
                    curFlashRange
            ) {

                const sx =
                    canvas.width / 2 +
                    Math.tan(itemAngle) *
                    projDist;


                const rayIndex =
                    Math.floor(
                        sx /
                        canvas.width *
                        numRays
                    );


                if (
                    rayIndex >= 0 &&
                    rayIndex < numRays &&
                    dist <
                        zBuffer[rayIndex]
                ) {

                    const size =
                        Math.min(
                            120,
                            projDist *
                            0.45 /
                            dist
                        );


                    const floatY =
                        Math.sin(
                            animTimer * 2.5
                        ) * 5;


                    const centerY =
                        canvas.height / 2 +
                        size / 3 +
                        floatY;


                    draw3DItem(
                        item.type,
                        sx,
                        centerY,
                        size
                    );


                    ctx.save();

                    ctx.fillStyle =
                        "#fff";

                    ctx.font =
                        `bold ${Math.max(
                            11,
                            Math.floor(size / 2.2)
                        )}px sans-serif`;

                    ctx.textAlign =
                        "center";

                    ctx.shadowColor =
                        "#000";

                    ctx.shadowBlur = 6;

                    ctx.fillText(
                        item.name +
                        " [R]",
                        sx,
                        centerY -
                        size / 1.2
                    );

                    ctx.restore();
                }
            }
        }
    );


    /*
     * 유령
     */

    ghosts.forEach(
        function(g) {

            if (
                g.hp <= 0
            ) {
                return;
            }


            const gdx =
                g.x - px;

            const gdy =
                g.y - py;


            const gDist =
                Math.sqrt(
                    gdx * gdx +
                    gdy * gdy
                );


            let gAngle =
                Math.atan2(
                    gdy,
                    gdx
                ) - angle;


            while (
                gAngle < -Math.PI
            ) {
                gAngle +=
                    2 * Math.PI;
            }


            while (
                gAngle > Math.PI
            ) {
                gAngle -=
                    2 * Math.PI;
            }


            if (
                Math.abs(gAngle) <
                    fov / 1.8 &&
                gDist <
                    curFlashRange
            ) {

                const sx =
                    canvas.width / 2 +
                    Math.tan(gAngle) *
                    projDist;


                const rayIndex =
                    Math.floor(
                        sx /
                        canvas.width *
                        numRays
                    );


                if (
                    rayIndex >= 0 &&
                    rayIndex < numRays &&
                    gDist <
                        zBuffer[rayIndex]
                ) {

                    const size =
                        Math.min(
                            220,
                            projDist *
                            0.75 /
                            gDist
                        );


                    const centerY =
                        canvas.height / 2 +
                        size / 4;


                    drawGhost(
                        sx,
                        centerY,
                        size,
                        g.stun
                    );
                }
            }
        }
    );


    drawWeapon();


    ctx.restore();
}


/* =========================================================
   GAME LOOP
========================================================= */

function gameLoop() {

    update();

    render();

    requestAnimationFrame(
        gameLoop
    );
}


/* =========================================================
   START
========================================================= */

initGame();

gameLoop();

</script>

</div>

</body>
</html>
"""

components.html(
    horror_game_html,
    height=620,
    scrolling=False
)
```
