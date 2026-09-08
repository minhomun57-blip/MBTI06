import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🏚️ 저주받은 저택",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🏚️ 저주받은 저택")

st.caption(
    "W/A/S/D 이동 | ←/→ 회전 | 마우스 드래그 시점 회전 | "
    "E 달리기 | R 상호작용 | 1 회복약 | 2 배터리 | "
    "3 퇴마부적 | 4 열쇠 확인 | 클릭 공격"
)

horror_game_html = r"""
<!DOCTYPE html>
<html lang="ko">

<head>
<meta charset="UTF-8">

<style>

html, body {
    margin: 0;
    padding: 0;
    background: #020202;
    overflow: hidden;
    font-family: "Courier New", monospace;
    user-select: none;
}

#gameWrapper {
    position: relative;
    width: 100%;
    height: 640px;
    overflow: hidden;
    background: #000;
}

#canvas {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 640px;
    display: block;
    background: #000;
    cursor: grab;
}

#canvas:active {
    cursor: grabbing;
}

/* =========================
   HUD
========================= */

#ui {
    position: absolute;
    top: 15px;
    left: 15px;
    z-index: 20;
    color: #ddd;
    font-size: 13px;
    pointer-events: none;
    text-shadow: 2px 2px 6px #000;
}

.bar {
    width: 220px;
    height: 12px;
    background: #090909;
    border: 1px solid #555;
    margin-top: 4px;
    box-shadow: 0 0 8px #000;
}

.fill {
    height: 100%;
    transition: width 0.1s;
}

#hp {
    background: linear-gradient(
        90deg,
        #350000,
        #ff0000
    );
}

#stamina {
    background: linear-gradient(
        90deg,
        #003c22,
        #00ff77
    );
}

#flashlight {
    background: linear-gradient(
        90deg,
        #554500,
        #ffee55
    );
}

#weapon {
    margin-top: 8px;
    color: #ffcc44;
    font-weight: bold;
}

#objective {
    margin-top: 10px;
    color: #aaa;
    max-width: 280px;
    line-height: 1.5;
}

/* =========================
   중앙 조준점
========================= */

#crosshair {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 16px;
    height: 16px;
    transform: translate(-50%, -50%);
    z-index: 18;
    pointer-events: none;
}

#crosshair::before,
#crosshair::after {
    content: "";
    position: absolute;
    background: rgba(255,255,255,0.75);
}

#crosshair::before {
    width: 2px;
    height: 16px;
    left: 7px;
    top: 0;
}

#crosshair::after {
    width: 16px;
    height: 2px;
    left: 0;
    top: 7px;
}

/* =========================
   미니맵
========================= */

#mapBox {
    position: absolute;
    right: 15px;
    top: 15px;
    width: 190px;
    height: 205px;
    background: rgba(0,0,0,0.88);
    border: 2px solid #555;
    z-index: 20;
    box-shadow: 0 0 20px #000;
}

#mapTitle {
    color: #ddd;
    text-align: center;
    padding: 5px;
    font-size: 12px;
    border-bottom: 1px solid #333;
}

#minimap {
    width: 180px;
    height: 180px;
    display: block;
    margin: auto;
}

/* =========================
   인벤토리
========================= */

#inventory {
    position: absolute;
    bottom: 15px;
    right: 15px;
    z-index: 20;
    display: flex;
    gap: 7px;
    pointer-events: none;
}

.slot {
    width: 67px;
    height: 65px;
    background: rgba(5,5,5,0.92);
    border: 1px solid #444;
    color: #aaa;
    text-align: center;
    font-size: 10px;
    padding-top: 4px;
    box-shadow: 0 0 8px #000;
}

.key {
    color: #ffbd2e;
    font-weight: bold;
}

/* =========================
   메시지
========================= */

#msg {
    position: absolute;
    left: 50%;
    top: 30%;
    transform: translate(-50%, -50%);
    color: #ff3333;
    font-size: 20px;
    font-weight: bold;
    z-index: 30;
    text-align: center;
    text-shadow: 0 0 12px #000;
    pointer-events: none;
    width: 80%;
}

/* =========================
   공포 효과
========================= */

#glitch {
    position: absolute;
    inset: 0;
    background:
        repeating-linear-gradient(
            0deg,
            rgba(255,0,0,0.13),
            rgba(255,0,0,0.13) 2px,
            transparent 2px,
            transparent 5px
        );
    opacity: 0;
    pointer-events: none;
    z-index: 25;
    mix-blend-mode: screen;
}

#vignette {
    position: absolute;
    inset: 0;
    z-index: 17;
    pointer-events: none;
    background:
        radial-gradient(
            ellipse at center,
            transparent 35%,
            rgba(0,0,0,0.25) 60%,
            rgba(0,0,0,0.9) 100%
        );
}

#blood {
    position: absolute;
    inset: 0;
    z-index: 26;
    pointer-events: none;
    background:
        radial-gradient(
            circle,
            transparent 35%,
            rgba(150,0,0,0.4)
        );
    opacity: 0;
}

/* =========================
   시작 화면
========================= */

#startScreen {
    position: absolute;
    inset: 0;
    z-index: 90;
    background:
        radial-gradient(
            circle at center,
            #241111,
            #030303 65%
        );
    color: #ddd;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
}

#startScreen h1 {
    font-size: 38px;
    color: #eee;
    text-shadow:
        0 0 10px red,
        0 0 30px #600;
}

#startScreen p {
    color: #aaa;
    line-height: 1.8;
}

#startButton {
    margin-top: 20px;
    background: #080808;
    color: #ddd;
    border: 1px solid #777;
    padding: 14px 40px;
    cursor: pointer;
    font-family: inherit;
}

#startButton:hover {
    color: red;
    border-color: red;
}

/* =========================
   게임오버 / 승리
========================= */

#gameover,
#victory {
    display: none;
    position: absolute;
    inset: 0;
    z-index: 100;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
}

#gameover {
    background:
        radial-gradient(
            circle,
            #350000,
            #050000 70%
        );
    color: red;
}

#victory {
    background:
        radial-gradient(
            circle,
            #303018,
            #030303 70%
        );
    color: #ffe66b;
}

#ghostFace {
    width: 270px;
    height: 330px;
    border-radius: 48%;
    background:
        radial-gradient(
            circle,
            #a00000 0%,
            #350000 55%,
            #000 100%
        );
    box-shadow: 0 0 100px red;
    position: relative;
    animation: shake 0.025s infinite alternate;
}

.eye {
    position: absolute;
    top: 25%;
    width: 52px;
    height: 72px;
    background: white;
    border-radius: 50%;
    box-shadow: 0 0 20px red;
}

.eye.left {
    left: 18%;
}

.eye.right {
    right: 18%;
}

.pupil {
    width: 15px;
    height: 15px;
    background: black;
    border-radius: 50%;
    position: absolute;
    top: 35%;
    left: 35%;
}

.mouth {
    position: absolute;
    left: 10%;
    bottom: 10%;
    width: 80%;
    height: 115px;
    background: black;
    border: 3px solid #a00;
    border-radius: 20px 20px 60px 60px;
    overflow: hidden;
}

.teeth {
    height: 30px;
    background:
        repeating-linear-gradient(
            90deg,
            white,
            white 13px,
            #300 13px,
            #300 18px
        );
}

.overlayText {
    margin-top: 25px;
    font-size: 25px;
    font-weight: bold;
}

.restart {
    margin-top: 20px;
    background: #080808;
    border: 1px solid currentColor;
    color: inherit;
    padding: 12px 30px;
    cursor: pointer;
    font-family: inherit;
}

@keyframes shake {
    from {
        transform:
            translate(5px,-5px)
            scale(1.05);
    }

    to {
        transform:
            translate(-5px,5px)
            scale(1.1);
    }
}

</style>
</head>

<body>

<div id="gameWrapper">

<div id="startScreen">

    <h1>🏚️ 저주받은 저택</h1>

    <p>
        오래된 저택에서 이상한 소리가 들려온다.<br>
        열쇠를 찾아 탈출하라.<br>
        하지만 저택에는 당신 혼자가 아니다...
    </p>

    <p>
        <b>W/A/S/D</b> 이동<br>
        <b>E</b> 달리기<br>
        <b>R</b> 상호작용<br>
        <b>마우스</b> 시점<br>
        <b>클릭</b> 공격
    </p>

    <button id="startButton">
        저택에 들어가기
    </button>

</div>

<div id="ui">

    <div>❤️ 생명력</div>

    <div class="bar">
        <div id="hp" class="fill"></div>
    </div>

    <br>

    <div>💨 스테미나</div>

    <div class="bar">
        <div id="stamina" class="fill"></div>
    </div>

    <br>

    <div>🔦 손전등</div>

    <div class="bar">
        <div id="flashlight" class="fill"></div>
    </div>

    <div id="weapon">
        무기: 맨손
    </div>

    <div id="objective">
        목표: 저택을 탐색하세요.
    </div>

</div>

<div id="mapBox">

    <div id="mapTitle">
        🗺️ 저택 지도
    </div>

    <canvas id="minimap"></canvas>

</div>

<div id="inventory">

    <div class="slot">
        <div class="key">[1]</div>
        💊 회복약
        <br>
        <span id="potion">0</span>
    </div>

    <div class="slot">
        <div class="key">[2]</div>
        🔋 배터리
        <br>
        <span id="battery">0</span>
    </div>

    <div class="slot">
        <div class="key">[3]</div>
        📜 퇴마부적
        <br>
        <span id="talisman">1</span>
    </div>

    <div class="slot">
        <div class="key">[4]</div>
        🔑 열쇠
        <br>
        <span id="key">없음</span>
    </div>

</div>

<div id="crosshair"></div>

<div id="msg">
    저택에 들어가세요...
</div>

<div id="glitch"></div>

<div id="blood"></div>

<div id="vignette"></div>

<div id="gameover">

    <div id="ghostFace">

        <div class="eye left">
            <div class="pupil"></div>
        </div>

        <div class="eye right">
            <div class="pupil"></div>
        </div>

        <div class="mouth">
            <div class="teeth"></div>
        </div>

    </div>

    <div class="overlayText">
        당신의 영혼은 저택에 갇혔습니다...
    </div>

    <button class="restart" onclick="resetGame()">
        다시 도전
    </button>

</div>

<div id="victory">

    <div style="
        font-size:100px;
        text-shadow:0 0 30px #fff000;
    ">
        🔑
    </div>

    <div class="overlayText">
        저택에서 탈출했습니다.
    </div>

    <div style="margin-top:10px;color:#aaa;">
        하지만... 정말 끝난 것일까요?
    </div>

    <button class="restart" onclick="resetGame()">
        다시 플레이
    </button>

</div>

<canvas id="canvas" tabindex="0"></canvas>

</div>

<script>

/* =========================================================
   CANVAS
========================================================= */

const canvas =
    document.getElementById("canvas");

const ctx =
    canvas.getContext("2d");

let W = 1000;
let H = 640;

function resizeCanvas() {

    const rect =
        canvas.getBoundingClientRect();

    W = Math.max(700, Math.floor(rect.width));
    H = Math.max(500, Math.floor(rect.height));

    canvas.width = W;
    canvas.height = H;
}

resizeCanvas();

window.addEventListener(
    "resize",
    resizeCanvas
);


/* =========================================================
   AUDIO
========================================================= */

let audioCtx = null;

function initAudio() {

    if (!audioCtx) {

        audioCtx =
            new (
                window.AudioContext ||
                window.webkitAudioContext
            )();
    }

    if(audioCtx.state === "suspended") {
        audioCtx.resume();
    }
}

function sound(type) {

    initAudio();

    if(!audioCtx) return;

    const now =
        audioCtx.currentTime;

    const osc =
        audioCtx.createOscillator();

    const gain =
        audioCtx.createGain();

    let duration = 0.25;

    if(type === "door") {

        osc.type = "triangle";

        osc.frequency.setValueAtTime(
            110,
            now
        );

        osc.frequency.exponentialRampToValueAtTime(
            45,
            now + 0.4
        );

        duration = 0.4;
    }

    if(type === "item") {

        osc.type = "sine";

        osc.frequency.setValueAtTime(
            450,
            now
        );

        osc.frequency.exponentialRampToValueAtTime(
            1000,
            now + 0.2
        );
    }

    if(type === "attack") {

        osc.type = "sawtooth";

        osc.frequency.setValueAtTime(
            180,
            now
        );

        osc.frequency.exponentialRampToValueAtTime(
            35,
            now + 0.12
        );

        duration = 0.12;
    }

    if(type === "hit") {

        osc.type = "square";

        osc.frequency.setValueAtTime(
            80,
            now
        );

        osc.frequency.exponentialRampToValueAtTime(
            18,
            now + 0.25
        );

        duration = 0.25;
    }

    if(type === "scare") {

        osc.type = "sawtooth";

        osc.frequency.setValueAtTime(
            70,
            now
        );

        osc.frequency.exponentialRampToValueAtTime(
            1200,
            now + 0.6
        );

        duration = 0.6;
    }

    if(type === "heartbeat") {

        osc.type = "sine";

        osc.frequency.setValueAtTime(
            55,
            now
        );

        osc.frequency.exponentialRampToValueAtTime(
            35,
            now + 0.15
        );

        duration = 0.15;
    }

    if(type === "victory") {

        osc.type = "sine";

        osc.frequency.setValueAtTime(
            400,
            now
        );

        osc.frequency.exponentialRampToValueAtTime(
            900,
            now + 0.5
        );

        duration = 0.5;
    }

    gain.gain.setValueAtTime(
        0.22,
        now
    );

    gain.gain.exponentialRampToValueAtTime(
        0.01,
        now + duration
    );

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start(now);
    osc.stop(now + duration);
}


/* =========================================================
   WALL TEXTURE
========================================================= */

const wallTex =
    document.createElement("canvas");

wallTex.width = 128;
wallTex.height = 128;

const wallCtx =
    wallTex.getContext("2d");

wallCtx.fillStyle = "#30201b";

wallCtx.fillRect(
    0,0,128,128
);

for(let y=0;y<128;y+=20) {

    wallCtx.fillStyle =
        "#17100d";

    wallCtx.fillRect(
        0,y,
        128,
        3
    );

    for(let x=0;x<128;x+=32) {

        const offset =
            (y/20)%2 === 0 ? 0 : 16;

        wallCtx.fillRect(
            x+offset,
            y,
            3,
            20
        );
    }
}


/* =========================================================
   DOOR TEXTURE
========================================================= */

const doorTex =
    document.createElement("canvas");

doorTex.width = 128;
doorTex.height = 128;

const doorCtx =
    doorTex.getContext("2d");

doorCtx.fillStyle = "#24150d";

doorCtx.fillRect(
    0,0,128,128
);

doorCtx.fillStyle = "#55321b";

doorCtx.fillRect(
    7,4,114,120
);

for(let x=12;x<120;x+=10) {

    doorCtx.fillStyle =
        "#321b0e";

    doorCtx.fillRect(
        x,7,3,114
    );
}

function doorPanel(x,y,w,h) {

    doorCtx.fillStyle =
        "#2a160b";

    doorCtx.fillRect(
        x,y,w,h
    );

    doorCtx.strokeStyle =
        "#79502b";

    doorCtx.lineWidth = 4;

    doorCtx.strokeRect(
        x,y,w,h
    );
}

doorPanel(
    18,12,92,42
);

doorPanel(
    18,66,92,42
);

doorCtx.fillStyle = "#111";

doorCtx.beginPath();

doorCtx.arc(
    99,63,7,
    0,
    Math.PI*2
);

doorCtx.fill();

doorCtx.fillStyle = "#c08b25";

doorCtx.beginPath();

doorCtx.arc(
    97,61,3,
    0,
    Math.PI*2
);

doorCtx.fill();


/* =========================================================
   MAP
========================================================= */

const initialMap = [

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

[1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1],

[1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1],

[1,0,0,0,2,0,0,0,0,0,2,0,0,0,2,0,0,0,1],

[1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1],

[1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1],

[1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],

[1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],

[1,0,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,0,1],

[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],

[1,0,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,0,1],

[1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],

[1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],

[1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1],

[1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1],

[1,0,0,0,2,0,0,0,0,0,2,0,0,0,2,0,0,0,1],

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

];

const MAP_SIZE =
    initialMap.length;


/* =========================================================
   GAME STATE
========================================================= */

let houseMap;

let px = 9.5;
let py = 10.5;

let angle = 0;

let hp = 100;
let stamina = 100;

let flashlight = 100;

let gameOver = false;
let victory = false;
let started = false;

let fear = 0;
let shake = 0;

let timer = 0;

let attackTimer = 0;

let footstepTimer = 0;

let heartbeatTimer = 0;

let eventTimer = 0;

let items = {};

let ghost = {};

let worldItems = [];

let furniture = [];


/* =========================================================
   INIT
========================================================= */

function initGame() {

    houseMap =
        JSON.parse(
            JSON.stringify(initialMap)
        );

    px = 9.5;
    py = 10.5;

    angle = 0;

    hp = 100;

    stamina = 100;

    flashlight = 100;

    gameOver = false;
    victory = false;

    fear = 0;
    shake = 0;

    timer = 0;

    attackTimer = 0;

    footstepTimer = 0;

    heartbeatTimer = 0;

    eventTimer =
        600 + Math.random()*600;

    items = {

        potion: 0,

        battery: 0,

        talisman: 1,

        key: false,

        knife: false

    };

    ghost = {

        x: 17.5,

        y: 16.5,

        hp: 100,

        stun: 0,

        attackCooldown: 0,

        phase: Math.random()*10

    };

    worldItems = [

        {
            x: 2.5,
            y: 2.5,
            type: "knife",
            name: "녹슨 단검"
        },

        {
            x: 16.5,
            y: 2.5,
            type: "potion",
            name: "회복약"
        },

        {
            x: 2.5,
            y: 8.5,
            type: "battery",
            name: "배터리"
        },

        {
            x: 16.5,
            y: 8.5,
            type: "potion",
            name: "회복약"
        },

        {
            x: 2.5,
            y: 15.5,
            type: "battery",
            name: "배터리"
        },

        {
            x: 16.5,
            y: 16.5,
            type: "key",
            name: "피묻은 열쇠"
        }

    ];

    furniture = [

        {
            x: 1.5,
            y: 1.5,
            type: "bookshelf"
        },

        {
            x: 3.2,
            y: 1.5,
            type: "bookshelf"
        },

        {
            x: 1.5,
            y: 3.0,
            type: "desk"
        },

        {
            x: 3.0,
            y: 3.0,
            type: "chair"
        },

        {
            x: 2.5,
            y: 2.2,
            type: "table"
        },

        {
            x: 15.5,
            y: 1.5,
            type: "cabinet"
        },

        {
            x: 17.2,
            y: 1.5,
            type: "cabinet"
        },

        {
            x: 16.5,
            y: 3.0,
            type: "bed"
        },

        {
            x: 17.5,
            y: 3.0,
            type: "chair"
        },

        {
            x: 8.5,
            y: 9.0,
            type: "table"
        },

        {
            x: 10.5,
            y: 9.0,
            type: "chair"
        },

        {
            x: 8.5,
            y: 12.0,
            type: "cabinet"
        },

        {
            x: 11.0,
            y: 12.0,
            type: "chair"
        },

        {
            x: 9.5,
            y: 6.5,
            type: "clock"
        },

        {
            x: 9.5,
            y: 14.0,
            type: "candle"
        },

        {
            x: 1.5,
            y: 16.5,
            type: "bed"
        },

        {
            x: 3.0,
            y: 16.5,
            type: "table"
        },

        {
            x: 1.5,
            y: 17.8,
            type: "cabinet"
        },

        {
            x: 3.0,
            y: 17.8,
            type: "chair"
        },

        {
            x: 15.5,
            y: 16.5,
            type: "cabinet"
        },

        {
            x: 17.5,
            y: 17.8,
            type: "desk"
        },

        {
            x: 16.0,
            y: 17.8,
            type: "chair"
        },

        {
            x: 17.5,
            y: 15.0,
            type: "table"
        }

    ];

    document.getElementById(
        "gameover"
    ).style.display = "none";

    document.getElementById(
        "victory"
    ).style.display = "none";

    document.getElementById(
        "startScreen"
    ).style.display =
        started ? "none" : "flex";

    updateObjective();

    updateUI();
}


/* =========================================================
   INPUT
========================================================= */

const keys = {};

function normalizeKey(k) {

    if(k === "ArrowLeft")
        return "left";

    if(k === "ArrowRight")
        return "right";

    return k.toLowerCase();
}

window.addEventListener(
    "keydown",
    function(e) {

        const k =
            normalizeKey(e.key);

        keys[k] = true;

        if([
            "ArrowUp",
            "ArrowDown",
            "ArrowLeft",
            "ArrowRight",
            " "
        ].includes(e.key)) {

            e.preventDefault();
        }

        if(!started) return;

        if(gameOver || victory)
            return;

        if(k === "r")
            interact();

        if(e.key === "1")
            usePotion();

        if(e.key === "2")
            useBattery();

        if(e.key === "3")
            useTalisman();

        if(e.key === "4") {

            if(items.key) {

                showMessage(
                    "🔑 열쇠를 가지고 있습니다. " +
                    "황금색 탈출문을 찾으세요.",
                    "#ffd700"
                );

            } else {

                showMessage(
                    "🔒 탈출열쇠가 없습니다.",
                    "#aaa"
                );
            }
        }

    }
);

window.addEventListener(
    "keyup",
    function(e) {

        keys[
            normalizeKey(e.key)
        ] = false;

    }
);


/* =========================================================
   START
========================================================= */

document
.getElementById("startButton")
.addEventListener(
    "click",
    function() {

        started = true;

        document.getElementById(
            "startScreen"
        ).style.display = "none";

        initAudio();

        sound("door");

        showMessage(
            "🏚️ 저택에 들어왔습니다...",
            "#ff4444"
        );

        canvas.focus();

    }
);


/* =========================================================
   POTION
========================================================= */

function usePotion() {

    if(items.potion <= 0) {

        showMessage(
            "💊 회복약이 없습니다.",
            "#aaa"
        );

        return;
    }

    if(hp >= 100) {

        showMessage(
            "❤️ 체력이 가득합니다.",
            "#aaa"
        );

        return;
    }

    hp =
        Math.min(
            100,
            hp + 45
        );

    items.potion--;

    sound("item");

    showMessage(
        "💊 회복약을 사용했습니다.",
        "#66ff66"
    );

    updateUI();
}


/* =========================================================
   BATTERY
========================================================= */

function useBattery() {

    if(items.battery <= 0) {

        showMessage(
            "🔋 배터리가 없습니다.",
            "#aaa"
        );

        return;
    }

    flashlight =
        Math.min(
            100,
            flashlight + 55
        );

    items.battery--;

    sound("item");

    showMessage(
        "🔋 손전등 배터리를 교체했습니다.",
        "#ffff66"
    );

    updateUI();
}


/* =========================================================
   TALISMAN
========================================================= */

function useTalisman() {

    if(items.talisman <= 0) {

        showMessage(
            "📜 퇴마부적이 없습니다.",
            "#aaa"
        );

        return;
    }

    if(ghost.hp <= 0)
        return;

    const dx =
        ghost.x - px;

    const dy =
        ghost.y - py;

    const dist =
        Math.hypot(dx,dy);

    if(dist < 7) {

        ghost.stun = 300;

        const nx =
            dx / Math.max(dist,0.01);

        const ny =
            dy / Math.max(dist,0.01);

        ghost.x += nx * 1.2;
        ghost.y += ny * 1.2;

        ghost.x =
            Math.max(
                1.2,
                Math.min(
                    MAP_SIZE-1.2,
                    ghost.x
                )
            );

        ghost.y =
            Math.max(
                1.2,
                Math.min(
                    MAP_SIZE-1.2,
                    ghost.y
                )
            );

        items.talisman--;

        shake = 15;

        sound("scare");

        showMessage(
            "📜 퇴마부적이 귀신을 밀어냈습니다!",
            "#00ffff"
        );

    } else {

        showMessage(
            "📜 귀신이 너무 멀리 있습니다.",
            "#aaa"
        );
    }

    updateUI();
}


/* =========================================================
   INTERACTION
========================================================= */

function interact() {

    if(!started ||
       gameOver ||
       victory)
        return;

    initAudio();

    /* 바라보는 방향 */

    const checkDistance = 1.6;

    const tx =
        Math.floor(
            px +
            Math.cos(angle) *
            checkDistance
        );

    const ty =
        Math.floor(
            py +
            Math.sin(angle) *
            checkDistance
        );

    if(
        tx >= 0 &&
        tx < MAP_SIZE &&
        ty >= 0 &&
        ty < MAP_SIZE
    ) {

        const tile =
            houseMap[ty][tx];

        /* 일반 문 */

        if(tile === 2) {

            houseMap[ty][tx] = 0;

            sound("door");

            showMessage(
                "🚪 낡은 문이 열렸습니다.",
                "#ffcc66"
            );

            return;
        }
    }

    /* 아이템 */

    for(
        let i=worldItems.length-1;
        i>=0;
        i--
    ) {

        const item =
            worldItems[i];

        const dist =
            Math.hypot(
                px-item.x,
                py-item.y
            );

        if(dist < 1.5) {

            collectItem(item);

            worldItems.splice(
                i,
                1
            );

            sound("item");

            updateUI();

            return;
        }
    }

    /* 탈출문 */

    const exitX = 9.5;
    const exitY = 1.5;

    const exitDist =
        Math.hypot(
            px-exitX,
            py-exitY
        );

    if(exitDist < 2) {

        if(items.key) {

            winGame();

        } else {

            showMessage(
                "🚪 문이 잠겨 있습니다. 열쇠가 필요합니다.",
                "#ffcc44"
            );
        }

        return;
    }

    showMessage(
        "주변에 상호작용할 것이 없습니다.",
        "#aaa"
    );
}


/* =========================================================
   COLLECT
========================================================= */

function collectItem(item) {

    if(item.type === "knife") {

        items.knife = true;

        showMessage(
            "🗡️ 녹슨 단검을 얻었습니다!",
            "#ffcc44"
        );

    }

    if(item.type === "potion") {

        items.potion++;

        showMessage(
            "💊 회복약을 얻었습니다. [1]",
            "#ff6666"
        );
    }

    if(item.type === "battery") {

        items.battery++;

        showMessage(
            "🔋 배터리를 얻었습니다. [2]",
            "#ffff66"
        );
    }

    if(item.type === "key") {

        items.key = true;

        showMessage(
            "🔑 피묻은 열쇠를 얻었습니다!",
            "#ffd700"
        );

        updateObjective();
    }
}


/* =========================================================
   MOUSE
========================================================= */

let mouseDown = false;
let lastMouseX = 0;

canvas.addEventListener(
    "mousedown",
    function(e) {

        if(!started ||
           gameOver ||
           victory)
            return;

        initAudio();

        canvas.focus();

        mouseDown = true;

        lastMouseX =
            e.clientX;

        if(items.knife) {

            attackTimer = 12;

            sound("attack");

            attack();

        } else {

            showMessage(
                "맨손입니다. 단검을 찾아야 합니다.",
                "#aaa"
            );
        }
    }
);

window.addEventListener(
    "mouseup",
    function() {

        mouseDown = false;

    }
);

window.addEventListener(
    "mousemove",
    function(e) {

        if(!mouseDown ||
           !started ||
           gameOver ||
           victory)
            return;

        const dx =
            e.clientX -
            lastMouseX;

        angle += dx * 0.006;

        lastMouseX =
            e.clientX;

    }
);


/* =========================================================
   ATTACK
========================================================= */

function attack() {

    if(ghost.hp <= 0)
        return;

    const dx =
        ghost.x-px;

    const dy =
        ghost.y-py;

    const dist =
        Math.hypot(dx,dy);

    let a =
        Math.atan2(
            dy,
            dx
        ) - angle;

    while(a < -Math.PI)
        a += Math.PI*2;

    while(a > Math.PI)
        a -= Math.PI*2;

    if(
        dist < 2.5 &&
        Math.abs(a) < 0.8
    ) {

        ghost.hp -= 50;

        ghost.stun = 90;

        shake = 12;

        sound("hit");

        showMessage(
            ghost.hp <= 0
            ? "💀 귀신을 성불시켰습니다!"
            : "🗡️ 귀신에게 피해를 입혔습니다!",
            "#00ffff"
        );

        if(ghost.hp <= 0) {

            ghost.hp = 0;

            updateObjective();
        }
    }
}


/* =========================================================
   COLLISION
========================================================= */

function solid(x,y) {

    if(
        x < 0 ||
        y < 0 ||
        x >= MAP_SIZE ||
        y >= MAP_SIZE
    )
        return true;

    const tile =
        houseMap[
            Math.floor(y)
        ][
            Math.floor(x)
        ];

    if(tile === 1 ||
       tile === 2)
        return true;

    /* 가구 충돌 */

    for(const f of furniture) {

        const dx =
            x-f.x;

        const dy =
            y-f.y;

        const r =
            f.type === "bed"
            ? 0.65
            : 0.45;

        if(
            Math.abs(dx) < r &&
            Math.abs(dy) < r
        )
            return true;
    }

    return false;
}


/* =========================================================
   DISTANCE
========================================================= */

function distanceToGhost() {

    return Math.hypot(
        ghost.x-px,
        ghost.y-py
    );
}


/* =========================================================
   UPDATE
========================================================= */

function update() {

    if(!started ||
       gameOver ||
       victory)
        return;

    timer += 0.05;

    if(shake > 0)
        shake--;

    if(attackTimer > 0)
        attackTimer--;

    /* 회전 */

    if(keys["left"])
        angle -= 0.045;

    if(keys["right"])
        angle += 0.045;

    /* 이동 */

    const moving =
        keys["w"] ||
        keys["s"] ||
        keys["a"] ||
        keys["d"];

    const running =
        keys["e"] &&
        stamina > 0 &&
        moving;

    let speed =
        running
        ? 0.075
        : 0.043;

    if(running) {

        stamina =
            Math.max(
                0,
                stamina - 0.75
            );

    } else {

        stamina =
            Math.min(
                100,
                stamina + 0.32
            );
    }

    let dx = 0;
    let dy = 0;

    if(keys["w"]) {

        dx +=
            Math.cos(angle)*speed;

        dy +=
            Math.sin(angle)*speed;
    }

    if(keys["s"]) {

        dx -=
            Math.cos(angle)*speed;

        dy -=
            Math.sin(angle)*speed;
    }

    if(keys["a"]) {

        dx +=
            Math.cos(
                angle-Math.PI/2
            )*speed;

        dy +=
            Math.sin(
                angle-Math.PI/2
            )*speed;
    }

    if(keys["d"]) {

        dx +=
            Math.cos(
                angle+Math.PI/2
            )*speed;

        dy +=
            Math.sin(
                angle+Math.PI/2
            )*speed;
    }

    const margin = 0.22;

    if(!solid(
        px+dx+Math.sign(dx)*margin,
        py
    )) {

        px += dx;
    }

    if(!solid(
        px,
        py+dy+Math.sign(dy)*margin
    )) {

        py += dy;
    }

    /* 발걸음 */

    if(moving) {

        footstepTimer--;

        if(
            footstepTimer <= 0
        ) {

            footstepTimer =
                running
                ? 16
                : 27;

            if(
                Math.random() < 0.25
            ) {
                sound("heartbeat");
            }
        }
    }

    /* 손전등 소모 */

    flashlight =
        Math.max(
            0,
            flashlight -
            0.006
        );

    /* =====================================================
       GHOST AI
    ===================================================== */

    if(ghost.hp > 0) {

        const gx =
            px-ghost.x;

        const gy =
            py-ghost.y;

        const dist =
            Math.hypot(gx,gy);

        if(ghost.stun > 0) {

            ghost.stun--;

        } else {

            /*
              멀리 있을 때는 느리게 배회.
              가까워지면 플레이어 추적.
            */

            if(dist < 15) {

                const speedGhost =
                    dist < 5
                    ? 0.023
                    : 0.014;

                const nx =
                    gx /
                    Math.max(dist,0.001);

                const ny =
                    gy /
                    Math.max(dist,0.001);

                let mx =
                    nx * speedGhost;

                let my =
                    ny * speedGhost;

                /*
                  아주 가까우면
                  플레이어를 적극적으로 추적
                */

                if(dist < 3) {

                    mx *= 1.35;
                    my *= 1.35;
                }

                if(!solid(
                    ghost.x+mx,
                    ghost.y
                )) {

                    ghost.x += mx;
                }

                if(!solid(
                    ghost.x,
                    ghost.y+my
                )) {

                    ghost.y += my;
                }

                /* 공격 */

                if(dist < 0.75) {

                    if(
                        ghost.attackCooldown <= 0
                    ) {

                        hp -=
                            dist < 0.4
                            ? 12
                            : 7;

                        ghost.attackCooldown =
                            45;

                        shake = 12;

                        document.getElementById(
                            "blood"
                        ).style.opacity =
                            0.8;

                        sound("hit");

                        if(hp <= 0) {

                            hp = 0;

                            triggerGameOver();
                        }
                    }
                }
            }

            if(
                ghost.attackCooldown > 0
            ) {

                ghost.attackCooldown--;
            }
        }

        /* 공포 */

        if(dist < 8) {

            fear =
                Math.min(
                    1,
                    (8-dist)/8
                );

        } else {

            fear *= 0.94;
        }

        document.getElementById(
            "glitch"
        ).style.opacity =
            fear * 0.65;

        document.getElementById(
            "blood"
        ).style.opacity =
            Math.max(
                0,
                parseFloat(
                    document.getElementById(
                        "blood"
                    ).style.opacity || 0
                ) - 0.025
            );

        /* 심장 */

        if(
            dist < 5 &&
            heartbeatTimer <= 0
        ) {

            heartbeatTimer =
                Math.max(
                    12,
                    Math.floor(
                        55*dist/5
                    )
                );

            sound("heartbeat");
        }

        heartbeatTimer--;

    } else {

        fear *= 0.95;

        document.getElementById(
            "glitch"
        ).style.opacity = 0;
    }

    /* 랜덤 공포 이벤트 */

    eventTimer--;

    if(eventTimer <= 0) {

        eventTimer =
            700 +
            Math.random()*900;

        if(
            Math.random() < 0.55 &&
            distanceToGhost() > 4
        ) {

            randomScare();
        }
    }

    updateUI();
}


/* =========================================================
   RANDOM SCARE
========================================================= */

function randomScare() {

    const messages = [

        "어딘가에서 문이 닫히는 소리가 들립니다...",

        "방금 뒤에서 무언가 움직였습니다.",

        "누군가 당신의 이름을 속삭였습니다.",

        "차가운 바람이 스쳐 지나갑니다.",

        "벽 너머에서 긁는 소리가 들립니다."

    ];

    const text =
        messages[
            Math.floor(
                Math.random()*messages.length
            )
        ];

    showMessage(
        text,
        "#bbbbbb"
    );

    shake = 3;

    sound("heartbeat");
}


/* =========================================================
   OBJECTIVE
========================================================= */

function updateObjective() {

    const el =
        document.getElementById(
            "objective"
        );

    if(!items.key) {

        el.innerText =
            "목표: 🔑 탈출열쇠를 찾으세요.";

    } else {

        el.innerText =
            "목표: 🚪 황금색 탈출문을 찾아 탈출하세요.";

    }
}


/* =========================================================
   UI
========================================================= */

function updateUI() {

    document.getElementById(
        "hp"
    ).style.width =
        Math.max(
            0,
            hp
        ) + "%";

    document.getElementById(
        "stamina"
    ).style.width =
        Math.max(
            0,
            stamina
        ) + "%";

    document.getElementById(
        "flashlight"
    ).style.width =
        Math.max(
            0,
            flashlight
        ) + "%";

    document.getElementById(
        "weapon"
    ).innerText =
        items.knife
        ? "무기: 🗡️ 녹슨 단검"
        : "무기: 맨손";

    document.getElementById(
        "potion"
    ).innerText =
        items.potion;

    document.getElementById(
        "battery"
    ).innerText =
        items.battery;

    document.getElementById(
        "talisman"
    ).innerText =
        items.talisman;

    document.getElementById(
        "key"
    ).innerText =
        items.key
        ? "획득"
        : "없음";
}


/* =========================================================
   MESSAGE
========================================================= */

function showMessage(
    text,
    color="#ff3333"
) {

    const el =
        document.getElementById(
            "msg"
        );

    el.innerText = text;

    el.style.color = color;

    clearTimeout(
        window.messageTimer
    );

    window.messageTimer =
        setTimeout(
            function() {

                if(
                    !gameOver &&
                    !victory
                ) {

                    el.innerText = "";
                }

            },
            3200
        );
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

    if(type === "bookshelf") {

        ctx.fillStyle =
            "#3b2110";

        ctx.fillRect(
            -size/2,
            -size,
            size,
            size*1.2
        );

        ctx.fillStyle =
            "#111";

        ctx.fillRect(
            -size/2.3,
            -size/1.2,
            size/1.15,
            size
        );

        ctx.fillStyle =
            "#663";

        for(
            let y=-size/1.1;
            y<size/3;
            y+=size/3
        ) {

            ctx.fillRect(
                -size/2.3,
                y,
                size/1.15,
                size/12
            );
        }

        ctx.fillStyle =
            "#a33";

        ctx.fillRect(
            -size/3,
            -size/1.1,
            size/8,
            size/3
        );

        ctx.fillStyle =
            "#268";

        ctx.fillRect(
            -size/10,
            -size/1.1,
            size/8,
            size/3
        );

    } else if(type === "desk") {

        ctx.fillStyle =
            "#4b2b17";

        ctx.fillRect(
            -size/1.2,
            -size/5,
            size*1.4,
            size/6
        );

        ctx.fillStyle =
            "#281508";

        ctx.fillRect(
            -size/1.1,
            -size/10,
            size/9,
            size/1.5
        );

        ctx.fillRect(
            size/1.1-size/9,
            -size/10,
            size/9,
            size/1.5
        );

    } else if(type === "chair") {

        ctx.fillStyle =
            "#4a2915";

        ctx.fillRect(
            -size/4,
            -size/1.1,
            size/2,
            size/2
        );

        ctx.fillRect(
            -size/3,
            -size/3,
            size/1.5,
            size/8
        );

    } else if(type === "table") {

        ctx.fillStyle =
            "#573218";

        ctx.fillRect(
            -size/2,
            -size/8,
            size,
            size/7
        );

        ctx.fillStyle =
            "#2b170b";

        ctx.fillRect(
            -size/3,
            0,
            size/10,
            size/1.5
        );

        ctx.fillRect(
            size/3-size/10,
            0,
            size/10,
            size/1.5
        );

    } else if(type === "bed") {

        ctx.fillStyle =
            "#4b2a17";

        ctx.fillRect(
            -size/1.1,
            -size/4,
            size*1.4,
            size/2
        );

        ctx.fillStyle =
            "#aaa";

        ctx.fillRect(
            -size,
            -size/3,
            size*1.2,
            size/4
        );

        ctx.fillStyle =
            "#ddd";

        ctx.fillRect(
            -size/1.1,
            -size/2.7,
            size/2.7,
            size/5
        );

    } else if(type === "cabinet") {

        ctx.fillStyle =
            "#333";

        ctx.fillRect(
            -size/3,
            -size,
            size*0.7,
            size
        );

        ctx.fillStyle =
            "#777";

        ctx.fillRect(
            -size/20,
            -size/2,
            size/10,
            size/12
        );

        ctx.fillRect(
            -size/20,
            -size/5,
            size/10,
            size/12
        );

    } else if(type === "clock") {

        ctx.fillStyle =
            "#3b210f";

        ctx.fillRect(
            -size/5,
            -size,
            size/2.5,
            size*1.2
        );

        ctx.fillStyle =
            "#eee";

        ctx.beginPath();

        ctx.arc(
            0,
            -size/1.3,
            size/6,
            0,
            Math.PI*2
        );

        ctx.fill();

        ctx.strokeStyle =
            "#111";

        ctx.beginPath();

        ctx.moveTo(
            0,
            -size/1.3
        );

        ctx.lineTo(
            size/10,
            -size/1.45
        );

        ctx.stroke();

    } else if(type === "candle") {

        ctx.fillStyle =
            "#866";

        ctx.fillRect(
            -size/15,
            -size/2,
            size/7,
            size/2
        );

        ctx.fillStyle =
            "#ffb000";

        ctx.beginPath();

        ctx.arc(
            0,
            -size/1.8,
            size/9,
            0,
            Math.PI*2
        );

        ctx.fill();
    }

    ctx.restore();
}


/* =========================================================
   ITEM DRAW
========================================================= */

function drawItem(
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

    if(type === "key") {

        ctx.strokeStyle =
            "#ffd700";

        ctx.lineWidth =
            Math.max(
                2,
                size/7
            );

        ctx.beginPath();

        ctx.arc(
            0,
            -size/3,
            size/4,
            0,
            Math.PI*2
        );

        ctx.stroke();

        ctx.fillStyle =
            "#ffd700";

        ctx.fillRect(
            0,
            -size/3+size/8,
            size/1.4,
            size/9
        );

        ctx.fillRect(
            size/2.2,
            -size/3+size/8,
            size/8,
            size/5
        );

    } else if(type === "knife") {

        ctx.fillStyle =
            "#ccc";

        ctx.beginPath();

        ctx.moveTo(
            0,
            -size
        );

        ctx.lineTo(
            size/6,
            size/4
        );

        ctx.lineTo(
            -size/6,
            size/4
        );

        ctx.closePath();

        ctx.fill();

        ctx.fillStyle =
            "#542811";

        ctx.fillRect(
            -size/5,
            size/4,
            size/2.5,
            size/2
        );

    } else if(type === "potion") {

        ctx.fillStyle =
            "#e22";

        ctx.beginPath();

        ctx.arc(
            0,
            size/5,
            size/2.5,
            0,
            Math.PI*2
        );

        ctx.fill();

        ctx.fillStyle =
            "#865";

        ctx.fillRect(
            -size/6,
            -size/3,
            size/3,
            size/5
        );

    } else if(type === "battery") {

        ctx.fillStyle =
            "#222";

        ctx.fillRect(
            -size/3,
            -size/3,
            size/1.5,
            size
        );

        ctx.fillStyle =
            "#f60";

        ctx.fillRect(
            -size/3,
            0,
            size/1.5,
            size/2
        );

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
    stunned
) {

    ctx.save();

    ctx.translate(
        sx,
        sy
    );

    const alpha =
        stunned
        ? 0.35
        : 0.92;

    /* 몸 */

    ctx.fillStyle =
        `rgba(205,220,235,${alpha})`;

    ctx.beginPath();

    ctx.arc(
        0,
        -size/2,
        size/3,
        Math.PI,
        0
    );

    ctx.lineTo(
        size/3,
        size/2
    );

    ctx.lineTo(
        size/5,
        size/3
    );

    ctx.lineTo(
        0,
        size/2
    );

    ctx.lineTo(
        -size/5,
        size/3
    );

    ctx.lineTo(
        -size/3,
        size/2
    );

    ctx.closePath();

    ctx.fill();

    /* 눈 */

    ctx.fillStyle =
        stunned
        ? "#00ffff"
        : "#ff0000";

    ctx.shadowColor =
        ctx.fillStyle;

    ctx.shadowBlur = 15;

    ctx.beginPath();

    ctx.arc(
        -size/8,
        -size/1.8,
        size/12,
        0,
        Math.PI*2
    );

    ctx.fill();

    ctx.beginPath();

    ctx.arc(
        size/8,
        -size/1.8,
        size/12,
        0,
        Math.PI*2
    );

    ctx.fill();

    ctx.restore();
}


/* =========================================================
   EXIT DRAW
========================================================= */

function drawExit(
    sx,
    sy,
    size
) {

    ctx.save();

    ctx.translate(
        sx,
        sy
    );

    ctx.shadowColor =
        "#ffd700";

    ctx.shadowBlur =
        20;

    ctx.fillStyle =
        "#8a6b12";

    ctx.fillRect(
        -size/2,
        -size,
        size,
        size*1.4
    );

    ctx.fillStyle =
        "#ffd700";

    ctx.strokeStyle =
        "#fff0a0";

    ctx.lineWidth = 3;

    ctx.strokeRect(
        -size/2,
        -size,
        size,
        size*1.4
    );

    ctx.fillStyle =
        "#221900";

    ctx.fillRect(
        -size/3,
        -size*0.85,
        size*0.66,
        size*1.1
    );

    ctx.fillStyle =
        "#fff0a0";

    ctx.font =
        Math.floor(size/4) +
        "px Arial";

    ctx.textAlign =
        "center";

    ctx.fillText(
        "EXIT",
        0,
        0
    );

    ctx.restore();
}


/* =========================================================
   RENDER
========================================================= */

function render() {

    ctx.save();

    if(shake > 0) {

        ctx.translate(
            (Math.random()-0.5)*shake,
            (Math.random()-0.5)*shake
        );
    }

    /* 천장 */

    const ceiling =
        ctx.createLinearGradient(
            0,
            0,
            0,
            H/2
        );

    ceiling.addColorStop(
        0,
        "#040404"
    );

    ceiling.addColorStop(
        1,
        "#281818"
    );

    ctx.fillStyle =
        ceiling;

    ctx.fillRect(
        0,
        0,
        W,
        H/2
    );

    /* 바닥 */

    const floor =
        ctx.createLinearGradient(
            0,
            H/2,
            0,
            H
        );

    floor.addColorStop(
        0,
        "#291515"
    );

    floor.addColorStop(
        1,
        "#020202"
    );

    ctx.fillStyle =
        floor;

    ctx.fillRect(
        0,
        H/2,
        W,
        H/2
    );

    const rays =
        Math.max(
            180,
            Math.floor(W/5)
        );

    const fov =
        Math.PI*0.43;

    const proj =
        (W/2) /
        Math.tan(fov/2);

    const zBuffer =
        new Array(rays)
        .fill(999);

    /*
      배터리가 낮아질수록
      시야가 어두워짐
    */

    const lightRange =
        5 +
        flashlight*0.10;

    const range =
        lightRange +
        (Math.random()-0.5)*0.08;

    const column =
        W/rays;

    /* 벽 */

    for(
        let i=0;
        i<rays;
        i++
    ) {

        const rayAngle =
            angle -
            fov/2 +
            (i/rays)*fov;

        let distance = 0;

        let hitType = 1;

        let wallX = 0;

        while(
            distance < range
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

            if(
                tx < 0 ||
                ty < 0 ||
                tx >= MAP_SIZE ||
                ty >= MAP_SIZE
            ) {

                break;
            }

            if(
                houseMap[ty][tx] > 0
            ) {

                hitType =
                    houseMap[ty][tx];

                const hitX =
                    rx-tx;

                const hitY =
                    ry-ty;

                wallX =
                    Math.abs(
                        hitX > hitY
                        ? hitY
                        : hitX
                    );

                wallX =
                    wallX*128;

                break;
            }
        }

        const corrected =
            distance *
            Math.cos(
                rayAngle-angle
            );

        zBuffer[i] =
            corrected;

        const height =
            Math.min(
                H*1.5,
                proj /
                Math.max(
                    corrected,
                    0.0001
                )
            );

        let brightness =
            1 -
            corrected/range;

        brightness =
            Math.max(
                0.08,
                brightness
            );

        if(
            flashlight < 20
        ) {

            brightness *=
                0.45 +
                flashlight/100;
        }

        if(hitType === 2) {

            ctx.drawImage(
                doorTex,
                Math.floor(
                    wallX
                ) % 128,
                0,
                1,
                128,
                i*column,
                (H-height)/2,
                column+1,
                height
            );

        } else {

            ctx.drawImage(
                wallTex,
                Math.floor(
                    wallX
                ) % 128,
                0,
                1,
                128,
                i*column,
                (H-height)/2,
                column+1,
                height
            );
        }

        ctx.fillStyle =
            `rgba(0,0,0,${1-brightness})`;

        ctx.fillRect(
            i*column,
            (H-height)/2,
            column+1,
            height
        );
    }


    /* =====================================================
       OBJECTS
    ===================================================== */

    const objects = [];


    /* Furniture */

    furniture.forEach(
        f => {

            const dx =
                f.x-px;

            const dy =
                f.y-py;

            const dist =
                Math.hypot(
                    dx,
                    dy
                );

            let a =
                Math.atan2(
                    dy,
                    dx
                )-angle;

            while(
                a < -Math.PI
            )
                a += Math.PI*2;

            while(
                a > Math.PI
            )
                a -= Math.PI*2;

            if(
                Math.abs(a) <
                    fov/1.8 &&
                dist < range
            ) {

                objects.push({
                    type:
                        "furniture",
                    data: f,
                    dist: dist,
                    angle: a
                });
            }
        }
    );


    /* Items */

    worldItems.forEach(
        item => {

            const dx =
                item.x-px;

            const dy =
                item.y-py;

            const dist =
                Math.hypot(
                    dx,
                    dy
                );

            let a =
                Math.atan2(
                    dy,
                    dx
                )-angle;

            while(
                a < -Math.PI
            )
                a += Math.PI*2;

            while(
                a > Math.PI
            )
                a -= Math.PI*2;

            if(
                Math.abs(a) <
                    fov/1.8 &&
                dist < range
            ) {

                objects.push({
                    type: "item",
                    data: item,
                    dist: dist,
                    angle: a
                });
            }
        }
    );


    /* Ghost */

    if(ghost.hp > 0) {

        const dx =
            ghost.x-px;

        const dy =
            ghost.y-py;

        const dist =
            Math.hypot(
                dx,
                dy
            );

        let a =
            Math.atan2(
                dy,
                dx
            )-angle;

        while(
            a < -Math.PI
        )
            a += Math.PI*2;

        while(
            a > Math.PI
        )
            a -= Math.PI*2;

        if(
            Math.abs(a) <
                fov/1.8 &&
            dist < range
        ) {

            objects.push({
                type: "ghost",
                data: ghost,
                dist: dist,
                angle: a
            });
        }
    }


    /* Exit */

    const exitX = 9.5;
    const exitY = 1.5;

    const exitDist =
        Math.hypot(
            exitX-px,
            exitY-py
        );

    if(exitDist < range) {

        let a =
            Math.atan2(
                exitY-py,
                exitX-px
            )-angle;

        while(
            a < -Math.PI
        )
            a += Math.PI*2;

        while(
            a > Math.PI
        )
            a -= Math.PI*2;

        if(
            Math.abs(a) <
            fov/1.8
        ) {

            objects.push({
                type: "exit",
                data: {
                    x: exitX,
                    y: exitY
                },
                dist: exitDist,
                angle: a
            });
        }
    }


    /* 먼 것부터 */

    objects.sort(
        (a,b) =>
            b.dist-a.dist
    );


    objects.forEach(
        obj => {

            const sx =
                W/2 +
                Math.tan(
                    obj.angle
                ) *
                proj;

            const ray =
                Math.floor(
                    (sx/W)*rays
                );

            if(
                ray < 0 ||
                ray >= rays
            )
                return;

            if(
                obj.dist >
                zBuffer[ray]+0.3
            )
                return;


            if(
                obj.type ===
                "furniture"
            ) {

                const size =
                    Math.min(
                        180,
                        proj *
                        0.55 /
                        obj.dist
                    );

                drawFurniture(
                    obj.data.type,
                    sx,
                    H/2+size/3,
                    size
                );
            }


            if(
                obj.type ===
                "item"
            ) {

                const size =
                    Math.min(
                        100,
                        proj *
                        0.4 /
                        obj.dist
                    );

                const floating =
                    Math.sin(
                        timer*3
                    )*4;

                drawItem(
                    obj.data.type,
                    sx,
                    H/2+
                    size/3+
                    floating,
                    size
                );

                ctx.save();

                ctx.fillStyle =
                    "white";

                ctx.font =
                    "bold " +
                    Math.max(
                        10,
                        Math.floor(
                            size/3
                        )
                    ) +
                    "px Arial";

                ctx.textAlign =
                    "center";

                ctx.shadowColor =
                    "black";

                ctx.shadowBlur = 5;

                ctx.fillText(
                    obj.data.name+
                    " [R]",
                    sx,
                    H/2-
                    size/1.1
                );

                ctx.restore();
            }


            if(
                obj.type ===
                "ghost"
            ) {

                const size =
                    Math.min(
                        230,
                        proj *
                        0.72 /
                        obj.dist
                    );

                drawGhost(
                    sx,
                    H/2+
                    size/4,
                    size,
                    obj.data.stun > 0
                );
            }


            if(
                obj.type ===
                "exit"
            ) {

                const size =
                    Math.min(
                        190,
                        proj *
                        0.7 /
                        obj.dist
                    );

                drawExit(
                    sx,
                    H/2+
                    size/4,
                    size
                );
            }

        }
    );


    /* 칼 */

    if(items.knife) {

        ctx.save();

        const swing =
            attackTimer > 0
            ? (12-attackTimer)*12
            : 0;

        ctx.translate(
            W-130-swing,
            H-80+swing
        );

        ctx.rotate(-0.6);

        ctx.fillStyle =
            "#aaa";

        ctx.fillRect(
            -8,
            -100,
            16,
            80
        );

        ctx.fillStyle =
            "#fff";

        ctx.fillRect(
            0,
            -100,
            8,
            80
        );

        ctx.fillStyle =
            "#542811";

        ctx.fillRect(
            -18,
            -20,
            36,
            12
        );

        ctx.fillRect(
            -7,
            -8,
            14,
            35
        );

        ctx.restore();
    }


    /* 배터리 부족 효과 */

    if(
        flashlight < 15
    ) {

        ctx.fillStyle =
            `rgba(
                0,
                0,
                0,
                ${0.15+
                Math.random()*0.15}
            )`;

        ctx.fillRect(
            0,
            0,
            W,
            H
        );
    }

    ctx.restore();

    drawMinimap();
}


/* =========================================================
   MINIMAP
========================================================= */

const mapCanvas =
    document.getElementById(
        "minimap"
    );

const mapCtx =
    mapCanvas.getContext("2d");

mapCanvas.width = 180;
mapCanvas.height = 180;

function drawMinimap() {

    const mw = 180;
    const mh = 180;

    mapCtx.fillStyle =
        "#070707";

    mapCtx.fillRect(
        0,
        0,
        mw,
        mh
    );

    const cell =
        Math.min(
            mw/MAP_SIZE,
            mh/MAP_SIZE
        );

    for(
        let y=0;
        y<MAP_SIZE;
        y++
    ) {

        for(
            let x=0;
            x<MAP_SIZE;
            x++
        ) {

            const tile =
                houseMap[y][x];

            if(tile === 1) {

                mapCtx.fillStyle =
                    "#292929";

            } else if(tile === 2) {

                mapCtx.fillStyle =
                    "#70451d";

            } else {

                mapCtx.fillStyle =
                    "#0c0c0c";
            }

            mapCtx.fillRect(
                x*cell,
                y*cell,
                cell-1,
                cell-1
            );
        }
    }


    /* 탈출문 */

    mapCtx.fillStyle =
        "#ffd700";

    mapCtx.fillRect(
        9.5*cell-3,
        1.5*cell-3,
        6,
        6
    );


    /* 아이템 */

    worldItems.forEach(
        item => {

            mapCtx.fillStyle =
                item.type === "key"
                ? "#ffd700"
                : "#66ff66";

            mapCtx.beginPath();

            mapCtx.arc(
                item.x*cell,
                item.y*cell,
                3,
                0,
                Math.PI*2
            );

            mapCtx.fill();
        }
    );


    /* 귀신 */

    if(ghost.hp > 0) {

        mapCtx.fillStyle =
            "#ff2222";

        mapCtx.beginPath();

        mapCtx.arc(
            ghost.x*cell,
            ghost.y*cell,
            4,
            0,
            Math.PI*2
        );

        mapCtx.fill();
    }


    /* 플레이어 */

    mapCtx.fillStyle =
        "#00ffff";

    mapCtx.beginPath();

    mapCtx.arc(
        px*cell,
        py*cell,
        4,
        0,
        Math.PI*2
    );

    mapCtx.fill();


    /* 방향 */

    mapCtx.strokeStyle =
        "#00ffff";

    mapCtx.lineWidth = 2;

    mapCtx.beginPath();

    mapCtx.moveTo(
        px*cell,
        py*cell
    );

    mapCtx.lineTo(
        (
            px+
            Math.cos(angle)*1.4
        )*cell,
        (
            py+
            Math.sin(angle)*1.4
        )*cell
    );

    mapCtx.stroke();
}


/* =========================================================
   GAME OVER
========================================================= */

function triggerGameOver() {

    if(gameOver)
        return;

    gameOver = true;

    sound("scare");

    document.getElementById(
        "gameover"
    ).style.display =
        "flex";
}


/* =========================================================
   VICTORY
========================================================= */

function winGame() {

    if(victory)
        return;

    victory = true;

    sound("victory");

    document.getElementById(
        "victory"
    ).style.display =
        "flex";
}


/* =========================================================
   RESET
========================================================= */

function resetGame() {

    started = true;

    initGame();

    document.getElementById(
        "startScreen"
    ).style.display =
        "none";

    showMessage(
        "🏚️ 다시 저택으로 돌아왔습니다...",
        "#ff4444"
    );

    canvas.focus();
}


/* =========================================================
   LOOP
========================================================= */

function loop() {

    update();

    render();

    requestAnimationFrame(
        loop
    );
}


initGame();

loop();

</script>

</body>
</html>
"""

components.html(
    horror_game_html,
    height=650,
    scrolling=False
)
