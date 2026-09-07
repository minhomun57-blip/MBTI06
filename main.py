import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🏚️ 저주받은 저택 - 공포 탐험",
    layout="wide"
)

st.title("🏚️ 저주받은 저택")
st.caption(
    "W/A/S/D: 이동 | ←/→: 회전 | E: 달리기 | "
    "R: 문 열기/아이템 획득 | 1: 회복 | 2: 손전등 강화 | "
    "3: 퇴마부적 | 마우스 드래그: 시점 회전 | 클릭: 공격"
)

horror_game_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">

<style>
body {
    margin: 0;
    overflow: hidden;
    background: #000;
    font-family: 'Courier New', monospace;
    user-select: none;
}

#canvas {
    width: 100%;
    height: 580px;
    display: block;
    cursor: grab;
    background: #000;
}

#canvas:active {
    cursor: grabbing;
}

#ui {
    position: absolute;
    top: 15px;
    left: 15px;
    color: #ddd;
    text-shadow: 2px 2px 5px #000;
    font-size: 13px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 5;
    pointer-events: none;
}

.bar-container {
    width: 220px;
    height: 12px;
    background: rgba(0,0,0,.9);
    border: 1px solid #444;
    border-radius: 2px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    width: 100%;
    transition: width .05s linear;
}

#hp-bar {
    background: linear-gradient(90deg,#500,#f00);
}

#stamina-bar {
    background: linear-gradient(90deg,#050,#00ff44);
}

#inventory {
    position: absolute;
    bottom: 15px;
    right: 15px;
    display: flex;
    gap: 8px;
    z-index: 5;
    pointer-events: none;
}

.slot {
    width: 65px;
    height: 65px;
    border: 1px solid #333;
    background: rgba(5,5,5,.9);
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
    transform: translate(-50%,-50%);
    color: #ff2222;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
    text-shadow: 0 0 10px #000;
    z-index: 5;
    pointer-events: none;
    letter-spacing: 1px;
}

#room-info {
    position: absolute;
    top: 15px;
    right: 15px;
    color: #aaa;
    font-size: 11px;
    text-align: right;
    z-index: 5;
    pointer-events: none;
}

#glitch-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 4;
    opacity: 0;
    background:
        repeating-linear-gradient(
            0deg,
            rgba(255,0,0,.18),
            rgba(255,0,0,.18) 2px,
            transparent 2px,
            transparent 4px
        );
}

#jumpscare {
    display: none;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #050000;
    z-index: 99;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    animation: flash-red .08s infinite alternate;
}

@keyframes flash-red {
    0% { background:#000; }
    100% { background:#200000; }
}

#scare-face {
    width: 340px;
    height: 400px;
    background:
        radial-gradient(
            circle,
            #800 0%,
            #200 50%,
            #000 100%
        );
    border-radius: 45% 45% 50% 50%;
    position: relative;
    box-shadow: 0 0 150px #f00;
    animation: violent-shake .015s infinite alternate;
}

.eye {
    position: absolute;
    top: 25%;
    width: 65px;
    height: 85px;
    background: white;
    border-radius: 50%;
    box-shadow:
        inset 0 0 30px #f00,
        0 0 20px #f00;
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
            rgba(150,0,0,.6),
            transparent 80%
        );
}

#scare-text {
    color: red;
    font-size: 30px;
    font-weight: 900;
    margin-top: 30px;
    text-shadow: 0 0 25px red;
    letter-spacing: 3px;
}

#restart-btn {
    margin-top: 25px;
    padding: 12px 32px;
    font-size: 15px;
    background: #050505;
    color: #f33;
    border: 1px solid red;
    cursor: pointer;
    font-weight: bold;
}

#restart-btn:hover {
    background: #400;
    color: white;
}

@keyframes violent-shake {
    0% {
        transform: translate(10px,-10px) scale(1.1);
    }
    100% {
        transform: translate(-10px,10px) scale(1.22);
    }
}
</style>
</head>

<body>

<div id="glitch-overlay"></div>

<div id="ui">

    <div>
        <span>생명력</span>
        <div class="bar-container">
            <div id="hp-bar" class="bar-fill"></div>
        </div>
    </div>

    <div>
        <span>스테미나 (E: 달리기)</span>
        <div class="bar-container">
            <div id="stamina-bar" class="bar-fill"></div>
        </div>
    </div>

    <div>
        무기:
        <span id="weapon" style="color:#ffcc00;">
            맨손
        </span>
    </div>

</div>

<div id="room-info">
    <div
        id="current-room-name"
        style="color:#ff3333;font-weight:bold;"
    >
        현재 위치: 중앙 홀
    </div>

    <div>
        화면을 클릭하여 조작하세요
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

<div id="msg">
    🏚️ 저주받은 저택에 들어왔습니다...
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

    <button id="restart-btn" onclick="resetGame()">
        다시 도전하기
    </button>

</div>

<canvas id="canvas" tabindex="0"></canvas>

<script>

const AudioContext =
    window.AudioContext ||
    window.webkitAudioContext;

let audioCtx = null;

function initAudio() {

    if (!audioCtx) {
        audioCtx = new AudioContext();
    }

}

function playSound(type) {

    if (!audioCtx) return;

    const now = audioCtx.currentTime;

    let osc =
        audioCtx.createOscillator();

    let gain =
        audioCtx.createGain();

    if (type === "attack") {

        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(140, now);
        osc.frequency.exponentialRampToValueAtTime(
            30,
            now + .15
        );

        gain.gain.setValueAtTime(.4, now);
        gain.gain.exponentialRampToValueAtTime(
            .01,
            now + .15
        );

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(now + .15);

    }

    else if (type === "hit") {

        osc.type = "square";
        osc.frequency.setValueAtTime(80, now);
        osc.frequency.exponentialRampToValueAtTime(
            15,
            now + .2
        );

        gain.gain.setValueAtTime(.5, now);
        gain.gain.exponentialRampToValueAtTime(
            .01,
            now + .2
        );

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(now + .2);

    }

    else if (type === "item") {

        osc.type = "sine";
        osc.frequency.setValueAtTime(520, now);
        osc.frequency.exponentialRampToValueAtTime(
            1040,
            now + .18
        );

        gain.gain.setValueAtTime(.3, now);
        gain.gain.exponentialRampToValueAtTime(
            .01,
            now + .18
        );

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(now + .18);

    }

    else if (type === "door") {

        osc.type = "triangle";
        osc.frequency.setValueAtTime(120, now);
        osc.frequency.linearRampToValueAtTime(
            60,
            now + .3
        );

        gain.gain.setValueAtTime(.4, now);
        gain.gain.exponentialRampToValueAtTime(
            .01,
            now + .3
        );

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(now + .3);

    }

    else if (type === "jumpscare") {

        osc.type = "sawtooth";

        osc.frequency.setValueAtTime(
            180,
            now
        );

        osc.frequency.linearRampToValueAtTime(
            1100,
            now + .08
        );

        osc.frequency.linearRampToValueAtTime(
            60,
            now + 1.2
        );

        gain.gain.setValueAtTime(1, now);

        gain.gain.exponentialRampToValueAtTime(
            .01,
            now + 1.2
        );

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(now + 1.2);

    }

}


/* =========================
   CANVAS
========================= */

const canvas =
    document.getElementById("canvas");

const ctx =
    canvas.getContext("2d");

canvas.width = 800;
canvas.height = 580;


/* =========================
   TEXTURES
========================= */

const wallTex =
    document.createElement("canvas");

wallTex.width = 64;
wallTex.height = 64;

const wCtx =
    wallTex.getContext("2d");

wCtx.fillStyle = "#2d1d1a";
wCtx.fillRect(0,0,64,64);

wCtx.fillStyle = "#140a08";

for (let i=0;i<64;i+=16) {

    wCtx.fillRect(
        0,
        i,
        64,
        2
    );

    for (let j=0;j<64;j+=16) {

        let offset =
            (i/16)%2 === 0
            ? 0
            : 8;

        wCtx.fillRect(
            j+offset,
            i,
            2,
            16
        );

    }

}


/* =========================
   DOOR TEXTURE
========================= */

const doorTex =
    document.createElement("canvas");

doorTex.width = 64;
doorTex.height = 64;

const dCtx =
    doorTex.getContext("2d");

dCtx.fillStyle = "#221108";
dCtx.fillRect(0,0,64,64);

dCtx.fillStyle = "#4a2b16";
dCtx.fillRect(3,3,58,58);

dCtx.fillStyle = "#3a200f";

for(let x=4;x<60;x+=6) {

    dCtx.fillRect(
        x,
        4,
        2,
        56
    );

}

function drawPanel(
    px,
    py,
    pw,
    ph
) {

    dCtx.fillStyle = "#1e0d05";
    dCtx.fillRect(
        px,
        py,
        pw,
        ph
    );

    dCtx.fillStyle = "#5c381d";
    dCtx.fillRect(
        px+2,
        py+2,
        pw-4,
        ph-4
    );

    dCtx.fillStyle = "#361d0d";
    dCtx.fillRect(
        px+4,
        py+4,
        pw-8,
        ph-8
    );

}

drawPanel(8,8,21,22);
drawPanel(35,8,21,22);
drawPanel(8,34,21,22);
drawPanel(35,34,21,22);

dCtx.fillStyle = "#8a6818";
dCtx.fillRect(50,28,6,14);

dCtx.fillStyle = "#ffcc00";
dCtx.fillRect(51,29,4,12);

dCtx.fillStyle = "#ffe066";
dCtx.fillRect(44,32,8,4);

dCtx.beginPath();

dCtx.arc(
    53,
    31,
    3,
    0,
    Math.PI*2
);

dCtx.fill();


/* =========================
   GAME VARIABLES
========================= */

let houseMap = [];

const initialMap = [

    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],

    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],

    [1,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,1],

    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],

    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],

    [1,1,1,1,1,0,1,0,0,0,0,0,1,0,1,1,1],

    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],

    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],

    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],

    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],

    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],

    [1,0,1,1,1,0,1,0,0,0,0,0,1,0,1,1,1],

    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],

    [1,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,1],

    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],

    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],

    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

];

const MAP_SIZE = initialMap.length;

let px = 8.5;
let py = 9.5;

let angle = 0;

let hp = 100;

let stamina = 100;

let flashRange = 18;

let gameOver = false;

let isAttacking = 0;

let screenShake = 0;

let animTimer = 0;

let zBuffer =
    new Array(180).fill(0);

let items = {

    potion: 0,

    battery: 0,

    talisman: 1,

    key: false,

    knife: false

};

let ghosts = [];

let worldItems = [];

let furnitureList = [];


/* =========================
   INITIALIZE
========================= */

function initGame() {

    houseMap =
        JSON.parse(
            JSON.stringify(initialMap)
        );

    px = 8.5;
    py = 9.5;

    /*
       중앙 홀을 바라보도록 시작
    */
    angle = 0;

    hp = 100;

    stamina = 100;

    flashRange = 18;

    gameOver = false;

    isAttacking = 0;

    screenShake = 0;

    items = {

        potion: 0,

        battery: 0,

        talisman: 1,

        key: false,

        knife: false

    };


    /* =========================
       GHOSTS
    ========================= */

    ghosts = [

        {
            x: 2.5,
            y: 2.5,
            hp: 100,
            stun: 0
        },

        {
            x: 14.5,
            y: 2.5,
            hp: 100,
            stun: 0
        },

        {
            x: 2.5,
            y: 14.5,
            hp: 100,
            stun: 0
        },

        {
            x: 14.5,
            y: 14.5,
            hp: 100,
            stun: 0
        }

    ];


    /* =========================
       ITEMS
    ========================= */

    worldItems = [

        {
            x: 2.5,
            y: 1.5,
            type: "knife",
            name: "녹슨 단검"
        },

        {
            x: 14.5,
            y: 1.5,
            type: "potion",
            name: "의용 회복제"
        },

        {
            x: 2.5,
            y: 5.0,
            type: "battery",
            name: "고전압 배터리"
        },

        {
            x: 14.5,
            y: 5.0,
            type: "potion",
            name: "의용 회복제"
        },

        {
            x: 2.5,
            y: 15.5,
            type: "battery",
            name: "고전압 배터리"
        },

        {
            x: 14.5,
            y: 15.5,
            type: "key",
            name: "피묻은 열쇠"
        }

    ];


    /* =========================
       FURNITURE
    ========================= */

    furnitureList = [

        /* 왼쪽 위 방 */

        {
            x:1.5,
            y:1.8,
            type:"bookshelf",
            name:"낡은 책장"
        },

        {
            x:1.5,
            y:3.5,
            type:"bookshelf",
            name:"먼지 쌓인 책장"
        },

        {
            x:4.2,
            y:1.5,
            type:"desk",
            name:"오래된 책상"
        },

        {
            x:4.2,
            y:2.5,
            type:"chair",
            name:"낡은 의자"
        },

        {
            x:4.2,
            y:4.2,
            type:"cabinet",
            name:"나무 수납장"
        },

        /* 오른쪽 위 방 */

        {
            x:14.5,
            y:1.8,
            type:"bed",
            name:"낡은 침대"
        },

        {
            x:15.5,
            y:3.5,
            type:"cabinet",
            name:"약품 보관함"
        },

        {
            x:12.8,
            y:1.5,
            type:"desk",
            name:"작은 책상"
        },

        {
            x:12.8,
            y:2.5,
            type:"chair",
            name:"나무 의자"
        },

        {
            x:15.0,
            y:4.5,
            type:"bookshelf",
            name:"의문의 서가"
        },

        /* 중앙 홀 */

        {
            x:7.5,
            y:8.0,
            type:"chair",
            name:"복도 의자"
        },

        {
            x:10.0,
            y:8.0,
            type:"clock",
            name:"거대한 괘종시계"
        },

        {
            x:12.5,
            y:8.0,
            type:"chair",
            name:"낡은 의자"
        },

        {
            x:7.5,
            y:11.5,
            type:"chair",
            name:"부서진 의자"
        },

        {
            x:10.0,
            y:11.5,
            type:"candelabra",
            name:"촛대"
        },

        {
            x:12.5,
            y:11.5,
            type:"chair",
            name:"핏자국 의자"
        },

        {
            x:8.0,
            y:6.8,
            type:"candelabra",
            name:"벽 촛대"
        },

        {
            x:12.0,
            y:6.8,
            type:"candelabra",
            name:"벽 촛대"
        },

        /* 왼쪽 아래 */

        {
            x:1.5,
            y:13.5,
            type:"bed",
            name:"핏자국 침대"
        },

        {
            x:4.2,
            y:13.5,
            type:"bookshelf",
            name:"작은 책장"
        },

        {
            x:1.5,
            y:15.5,
            type:"cabinet",
            name:"낡은 보관함"
        },

        {
            x:4.2,
            y:15.5,
            type:"desk",
            name:"실험용 책상"
        },

        {
            x:4.2,
            y:16.3,
            type:"chair",
            name:"실험실 의자"
        },

        /* 오른쪽 아래 */

        {
            x:14.5,
            y:13.5,
            type:"cabinet",
            name:"철제 보관함"
        },

        {
            x:12.8,
            y:15.0,
            type:"desk",
            name:"연구 책상"
        },

        {
            x:12.8,
            y:15.8,
            type:"chair",
            name:"실험실 의자"
        },

        {
            x:15.0,
            y:15.5,
            type:"bookshelf",
            name:"금지된 서적"
        },

        {
            x:14.5,
            y:16.3,
            type:"cabinet",
            name:"잠긴 철제 캐비닛"
        }

    ];


    document
        .getElementById("jumpscare")
        .style.display = "none";

    document
        .getElementById("msg")
        .innerText =
        "🏚️ 저주받은 저택에 들어왔습니다. 주변을 탐색하세요.";

    document
        .getElementById("msg")
        .style.color = "#ff3333";

    updateUI();

}


/* =========================
   INPUT
========================= */

const keys = {};

function parseKey(k) {

    if (k === "ArrowLeft")
        return "left";

    if (k === "ArrowRight")
        return "right";

    k = k.toLowerCase();

    if (k === "ㅈ")
        return "w";

    if (k === "ㄴ")
        return "s";

    if (k === "ㅁ")
        return "a";

    if (k === "ㅇ")
        return "d";

    if (k === "ㄷ")
        return "e";

    if (k === "ㄱ")
        return "r";

    return k;

}


/* =========================
   INTERACTION
========================= */

function handleInteract() {

    if (gameOver)
        return;

    const checkDist = 1.3;

    const targetX =
        Math.floor(
            px +
            Math.cos(angle) *
            checkDist
        );

    const targetY =
        Math.floor(
            py +
            Math.sin(angle) *
            checkDist
        );


    if (
        targetX >= 0 &&
        targetX < MAP_SIZE &&
        targetY >= 0 &&
        targetY < MAP_SIZE
    ) {

        const tile =
            houseMap[targetY][targetX];


        /* 일반 문 */

        if (tile === 2) {

            houseMap[targetY][targetX] = 0;

            playSound("door");

            showTmpMsg(
                "🚪 문을 열었습니다."
            );

            return;

        }


        /* 탈출문 */

        if (tile === 3) {

            if (items.key) {

                gameOver = true;

                playSound("door");

                document
                    .getElementById("msg")
                    .innerText =
                    "🚪 탈출 성공! 저택에서 살아남았습니다!";

                document
                    .getElementById("msg")
                    .style.color =
                    "gold";

            }

            else {

                showTmpMsg(
                    "🔒 문이 잠겨 있습니다. 피묻은 열쇠가 필요합니다."
                );

            }

            return;

        }

    }


    let picked = false;

    for (
        let i = worldItems.length - 1;
        i >= 0;
        i--
    ) {

        const item =
            worldItems[i];

        const dist =
            Math.hypot(
                px - item.x,
                py - item.y
            );

        if (
            dist < 1.5 &&
            !picked
        ) {

            playSound("item");

            if (item.type === "key") {

                items.key = true;

                showTmpMsg(
                    "🔑 피묻은 열쇠를 획득했습니다!"
                );

            }

            else if (item.type === "knife") {

                items.knife = true;

                showTmpMsg(
                    "🗡️ 녹슨 단검을 획득했습니다!"
                );

            }

            else if (item.type === "potion") {

                items.potion++;

                showTmpMsg(
                    "💊 회복제를 획득했습니다!"
                );

            }

            else if (item.type === "battery") {

                items.battery++;

                showTmpMsg(
                    "🔋 배터리를 획득했습니다!"
                );

            }

            worldItems.splice(i,1);

            picked = true;

            updateUI();

        }

    }


    if (!picked) {

        showTmpMsg(
            "상호작용할 대상이 가까이에 없습니다."
        );

    }

}


/* =========================
   KEYBOARD
========================= */

window.addEventListener(
    "keydown",
    e => {

        const k =
            parseKey(e.key);

        keys[k] = true;

        if (
            [
                "ArrowUp",
                "ArrowDown",
                "ArrowLeft",
                "ArrowRight",
                " "
            ].includes(e.key)
        ) {

            e.preventDefault();

        }


        if (gameOver)
            return;


        if (k === "r")
            handleInteract();


        /* 회복약 */

        if (
            e.key === "1" &&
            items.potion > 0
        ) {

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


        /* 배터리 */

        if (
            e.key === "2" &&
            items.battery > 0
        ) {

            flashRange = 24;

            items.battery--;

            playSound("item");

            showTmpMsg(
                "🔋 손전등 출력이 강화되었습니다."
            );

            updateUI();

        }


        /* 부적 */

        if (
            e.key === "3" &&
            items.talisman > 0
        ) {

            ghosts.forEach(
                g => {

                    if (g.hp <= 0)
                        return;

                    g.stun = 200;

                    const dx =
                        g.x - px;

                    const dy =
                        g.y - py;

                    g.x += dx * .5;
                    g.y += dy * .5;

                }
            );

            items.talisman--;

            playSound("item");

            screenShake = 12;

            showTmpMsg(
                "📜 퇴마부적으로 원혼을 밀어냈습니다!"
            );

            updateUI();

        }

    }
);


window.addEventListener(
    "keyup",
    e => {

        keys[
            parseKey(e.key)
        ] = false;

    }
);


/* =========================
   MOUSE
========================= */

let isMouseDown = false;

let lastMouseX = 0;

canvas.addEventListener(
    "mousedown",
    e => {

        initAudio();

        canvas.focus();

        isMouseDown = true;

        lastMouseX =
            e.clientX;


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
    () => {

        isMouseDown = false;

    }
);

window.addEventListener(
    "mousemove",
    e => {

        if (!isMouseDown)
            return;

        const dx =
            e.clientX -
            lastMouseX;

        angle += dx * .006;

        lastMouseX =
            e.clientX;

    }
);


/* =========================
   MESSAGE
========================= */

function showTmpMsg(txt) {

    const msg =
        document.getElementById("msg");

    msg.innerText = txt;

    setTimeout(
        () => {

            if (
                !gameOver &&
                msg.innerText === txt
            ) {

                msg.innerText = "";

            }

        },
        2500
    );

}


/* =========================
   ATTACK
========================= */

function checkAttackHit() {

    ghosts.forEach(
        g => {

            if (g.hp <= 0)
                return;

            const dx =
                g.x - px;

            const dy =
                g.y - py;

            const dist =
                Math.hypot(dx,dy);

            let a =
                Math.atan2(
                    dy,
                    dx
                ) - angle;

            while (a < -Math.PI)
                a += Math.PI * 2;

            while (a > Math.PI)
                a -= Math.PI * 2;


            if (
                dist < 2.2 &&
                Math.abs(a) < .7
            ) {

                g.hp -= 50;

                g.stun = 50;

                playSound("hit");

                screenShake = 8;

                if (g.hp <= 0) {

                    showTmpMsg(
                        "💀 원혼을 성불시켰습니다!"
                    );

                }

            }

        }
    );

}


/* =========================
   UI
========================= */

function updateUI() {

    document
        .getElementById("hp-bar")
        .style.width =
        Math.max(0,hp) + "%";

    document
        .getElementById("stamina-bar")
        .style.width =
        Math.max(0,stamina) + "%";


    document
        .getElementById("weapon")
        .innerText =
        items.knife
        ? "녹슨 단검"
        : "맨손";


    document
        .getElementById("cnt-potion")
        .innerText =
        items.potion;

    document
        .getElementById("cnt-battery")
        .innerText =
        items.battery;

    document
        .getElementById("cnt-talisman")
        .innerText =
        items.talisman;

    document
        .getElementById("cnt-key")
        .innerText =
        items.key
        ? "획득완료"
        : "미획득";

}


/* =========================
   COLLISION
========================= */

function isSolid(x,y) {

    if (
        x < 0 ||
        x >= MAP_SIZE ||
        y < 0 ||
        y >= MAP_SIZE
    )
        return true;

    const tile =
        houseMap[
            Math.floor(y)
        ][
            Math.floor(x)
        ];

    /*
       1 = 벽
       2 = 닫힌 문
       3 = 탈출문
    */

    return (
        tile === 1 ||
        tile === 2 ||
        tile === 3
    );

}


/* =========================
   JUMPSCARE
========================= */

function triggerJumpscare() {

    gameOver = true;

    playSound("jumpscare");

    document
        .getElementById("jumpscare")
        .style.display =
        "flex";

}


function resetGame() {

    initGame();

}


/* =========================
   UPDATE
========================= */

function update() {

    if (gameOver)
        return;

    animTimer += .05;


    if (screenShake > 0)
        screenShake--;


    /* 회전 */

    if (
        keys["left"] ||
        keys["a"]
    )
        angle -= .045;

    if (
        keys["right"] ||
        keys["d"]
    )
        angle += .045;


    /* 이동속도 */

    const moving =
        keys["w"] ||
        keys["s"];


    let running =
        keys["e"] &&
        moving &&
        stamina > 0;


    const speed =
        running
        ? .065
        : .038;


    if (running) {

        stamina =
            Math.max(
                0,
                stamina - .45
            );

    }

    else {

        stamina =
            Math.min(
                100,
                stamina + .22
            );

    }


    let dx = 0;
    let dy = 0;


    if (keys["w"]) {

        dx +=
            Math.cos(angle) *
            speed;

        dy +=
            Math.sin(angle) *
            speed;

    }


    if (keys["s"]) {

        dx -=
            Math.cos(angle) *
            speed;

        dy -=
            Math.sin(angle) *
            speed;

    }


    /* 충돌 */

    const margin = .22;


    if (
        !isSolid(
            px + dx +
            Math.sign(dx) * margin,
            py
        )
    ) {

        px += dx;

    }


    if (
        !isSolid(
            px,
            py + dy +
            Math.sign(dy) * margin
        )
    ) {

        py += dy;

    }


    /* =========================
       ROOM NAME
    ========================= */

    const curX =
        Math.floor(px);

    const curY =
        Math.floor(py);

    let roomTxt =
        "중앙 홀";


    if (
        curX < 6 &&
        curY < 6
    ) {

        roomTxt =
            "북서쪽 서재";

    }

    else if (
        curX > 12 &&
        curY < 6
    ) {

        roomTxt =
            "북동쪽 침실";

    }

    else if (
        curX < 6 &&
        curY > 12
    ) {

        roomTxt =
            "남서쪽 연구실";

    }

    else if (
        curX > 12 &&
        curY > 12
    ) {

        roomTxt =
            "남동쪽 밀실";

    }


    document
        .getElementById(
            "current-room-name"
        )
        .innerText =
        "현재 위치: " +
        roomTxt;


    /* =========================
       GHOST AI
    ========================= */

    let minDist = 999;


    ghosts.forEach(
        g => {

            if (g.hp <= 0)
                return;


            const dx =
                px - g.x;

            const dy =
                py - g.y;

            const dist =
                Math.hypot(dx,dy);


            minDist =
                Math.min(
                    minDist,
                    dist
                );


            if (g.stun > 0) {

                g.stun--;

            }

            else {

                if (dist > .1) {

                    const moveX =
                        dx / dist * .018;

                    const moveY =
                        dy / dist * .018;


                    if (
                        !isSolid(
                            g.x + moveX,
                            g.y
                        )
                    )
                        g.x += moveX;


                    if (
                        !isSolid(
                            g.x,
                            g.y + moveY
                        )
                    )
                        g.y += moveY;

                }


                if (dist < .6) {

                    hp -= 2;

                    screenShake = 5;

                    if (hp <= 0) {

                        triggerJumpscare();

                    }

                }

            }

        }
    );


    /* =========================
       GLITCH
    ========================= */

    if (minDist < 5.5) {

        document
            .getElementById(
                "glitch-overlay"
            )
            .style.opacity =
            (
                (5.5 - minDist) /
                5.5
            ) * .75;

    }

    else {

        document
            .getElementById(
                "glitch-overlay"
            )
            .style.opacity = 0;

    }


    if (isAttacking > 0)
        isAttacking--;

    updateUI();

}


/* =========================
   ITEM DRAW
========================= */

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
            -size/3,
            size/3.2,
            0,
            Math.PI*2
        );

        ctx.fill();


        ctx.fillStyle =
            "#1a1100";

        ctx.beginPath();

        ctx.arc(
            0,
            -size/3,
            size/6,
            0,
            Math.PI*2
        );

        ctx.fill();


        ctx.fillStyle =
            "#ffd700";

        ctx.fillRect(
            -size/12,
            -size/6,
            size/6,
            size/1.2
        );

        ctx.fillRect(
            size/12,
            size/4,
            size/4,
            size/8
        );

        ctx.fillRect(
            size/12,
            size/2.2,
            size/4,
            size/8
        );

    }


    else if (type === "knife") {

        ctx.fillStyle =
            "#888";

        ctx.beginPath();

        ctx.moveTo(
            0,
            -size/1.5
        );

        ctx.lineTo(
            size/6,
            size/6
        );

        ctx.lineTo(
            -size/6,
            size/6
        );

        ctx.closePath();

        ctx.fill();


        ctx.fillStyle =
            "#fff";

        ctx.beginPath();

        ctx.moveTo(
            0,
            -size/1.5
        );

        ctx.lineTo(
            0,
            size/6
        );

        ctx.lineTo(
            -size/6,
            size/6
        );

        ctx.closePath();

        ctx.fill();


        ctx.fillStyle =
            "#4a2511";

        ctx.fillRect(
            -size/4,
            size/6,
            size/2,
            size/10
        );


        ctx.fillStyle =
            "#2b1408";

        ctx.fillRect(
            -size/8,
            size/6 + size/10,
            size/4,
            size/2.5
        );

    }


    else if (type === "potion") {

        ctx.fillStyle =
            "rgba(200,200,255,.4)";

        ctx.beginPath();

        ctx.arc(
            0,
            size/4,
            size/2.2,
            0,
            Math.PI*2
        );

        ctx.fill();


        ctx.fillStyle =
            "#ff1133";

        ctx.beginPath();

        ctx.arc(
            0,
            size/4,
            size/2.6,
            0,
            Math.PI*2
        );

        ctx.fill();


        ctx.fillStyle =
            "rgba(255,255,255,.6)";

        ctx.beginPath();

        ctx.arc(
            -size/6,
            size/6,
            size/8,
            0,
            Math.PI*2
        );

        ctx.fill();


        ctx.fillStyle =
            "#8b5a2b";

        ctx.fillRect(
            -size/6,
            -size/3,
            size/3,
            size/6
        );

    }


    else if (type === "battery") {

        ctx.fillStyle =
            "#222";

        ctx.fillRect(
            -size/3,
            -size/3,
            size/1.5,
            size/1.2
        );


        ctx.fillStyle =
            "#ff6600";

        ctx.fillRect(
            -size/3,
            0,
            size/1.5,
            size/2.4
        );


        ctx.fillStyle =
            "#aaa";

        ctx.fillRect(
            -size/8,
            -size/2,
            size/4,
            size/6
        );


        ctx.fillStyle =
            "#fff";

        ctx.font =
            `bold ${Math.max(
                10,
                Math.floor(size/3)
            )}px sans-serif`;

        ctx.textAlign =
            "center";

        ctx.textBaseline =
            "middle";

        ctx.fillText(
            "⚡",
            0,
            size/5
        );

    }


    ctx.restore();

}


/* =========================
   FURNITURE DRAW
========================= */

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


    if (type === "bookshelf") {

        ctx.fillStyle =
            "#3a200d";

        ctx.fillRect(
            -size/2,
            -size/1.2,
            size,
            size*1.2
        );


        ctx.fillStyle =
            "#1e0f06";

        ctx.fillRect(
            -size/2.3,
            -size/1.3,
            size/1.15,
            size*1.1
        );


        ctx.fillStyle =
            "#4a2c16";

        ctx.fillRect(
            -size/2.3,
            -size/2,
            size/1.15,
            size/12
        );

        ctx.fillRect(
            -size/2.3,
            0,
            size/1.15,
            size/12
        );


        ctx.fillStyle =
            "#aa2222";

        ctx.fillRect(
            -size/2.6,
            -size/1.25,
            size/8,
            size/3
        );


        ctx.fillStyle =
            "#2288aa";

        ctx.fillRect(
            -size/4,
            -size/1.25,
            size/7,
            size/3.2
        );


        ctx.fillStyle =
            "#ccaa22";

        ctx.fillRect(
            0,
            -size/2.3,
            size/6,
            size/3
        );

    }


    else if (type === "desk") {

        ctx.fillStyle =
            "#422817";

        ctx.fillRect(
            -size/1.3,
            -size/4,
            size*1.5,
            size/6
        );


        ctx.fillStyle =
            "#2b180d";

        ctx.fillRect(
            -size/1.4,
            -size/8,
            size/8,
            size/1.5
        );

        ctx.fillRect(
            size/1.6,
            -size/8,
            size/8,
            size/1.5
        );

    }


    else if (type === "chair") {

        ctx.fillStyle =
            "#3a200d";

        ctx.fillRect(
            -size/4,
            -size/1.2,
            size/2,
            size/1.8
        );


        ctx.fillStyle =
            "#543118";

        ctx.fillRect(
            -size/3,
            -size/3,
            size/1.5,
            size/8
        );


        ctx.fillStyle =
            "#221207";

        ctx.fillRect(
            -size/3,
            -size/4,
            size/10,
            size/2
        );

        ctx.fillRect(
            size/3-size/10,
            -size/4,
            size/10,
            size/2
        );

    }


    else if (type === "bed") {

        ctx.fillStyle =
            "#4a2e1b";

        ctx.fillRect(
            -size/1.2,
            -size/6,
            size*1.6,
            size/2
        );


        ctx.fillStyle =
            "#aaa";

        ctx.fillRect(
            -size/1.1,
            -size/4,
            size*1.4,
            size/4
        );


        ctx.fillStyle =
            "#e6e6e6";

        ctx.fillRect(
            -size/1.1,
            -size/3,
            size/2.5,
            size/5
        );

    }


    else if (type === "cabinet") {

        ctx.fillStyle =
            "#333b42";

        ctx.fillRect(
            -size/3,
            -size/1.1,
            size/1.5,
            size*1.1
        );


        ctx.fillStyle =
            "#1e2327";

        ctx.fillRect(
            -size/3.5,
            -size/1.15,
            size/1.8,
            size/12
        );


        ctx.fillStyle =
            "#777";

        ctx.fillRect(
            0,
            -size/2,
            size/12,
            size/8
        );

    }


    else if (type === "clock") {

        ctx.fillStyle =
            "#2d1a0e";

        ctx.fillRect(
            -size/4,
            -size,
            size/2,
            size*1.3
        );


        ctx.fillStyle =
            "#ffeecc";

        ctx.beginPath();

        ctx.arc(
            0,
            -size/1.3,
            size/6,
            0,
            Math.PI*2
        );

        ctx.fill();


        ctx.fillStyle =
            "#ffaa00";

        ctx.beginPath();

        ctx.arc(
            0,
            -size/3,
            size/12,
            0,
            Math.PI*2
        );

        ctx.fill();

    }


    else if (type === "candelabra") {

        ctx.fillStyle =
            "#887711";

        ctx.fillRect(
            -size/16,
            -size/2,
            size/8,
            size/1.2
        );


        ctx.fillStyle =
            "#ffaa00";

        ctx.beginPath();

        ctx.arc(
            0,
            -size/1.8,
            size/8,
            0,
            Math.PI*2
        );

        ctx.fill();


        ctx.fillStyle =
            "#ffff66";

        const flicker =
            Math.sin(animTimer*10)*2;

        ctx.beginPath();

        ctx.arc(
            0,
            -size/1.4 + flicker,
            size/12,
            0,
            Math.PI*2
        );

        ctx.fill();

    }


    ctx.restore();

}


/* =========================
   GHOST
========================= */

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
        ? .4
        : .85;


    ctx.fillStyle =
        `rgba(
            200,
            220,
            255,
            ${alpha}
        )`;


    ctx.beginPath();

    ctx.arc(
        0,
        -size/2,
        size/3,
        Math.PI,
        0,
        false
    );

    ctx.lineTo(
        size/3,
        size/2
    );

    ctx.lineTo(
        -size/3,
        size/2
    );

    ctx.closePath();

    ctx.fill();


    ctx.fillStyle =
        stun > 0
        ? "#00ffff"
        : "#ff0000";


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


/* =========================
   WEAPON
========================= */

function drawWeapon() {

    if (!items.knife)
        return;


    ctx.save();


    const swing =
        isAttacking > 0
        ? (10-isAttacking)*8
        : 0;


    const weaponX =
        canvas.width -
        150 -
        swing;


    const weaponY =
        canvas.height -
        100 +
        swing;


    ctx.translate(
        weaponX,
        weaponY
    );


    ctx.rotate(
        -Math.PI/4 +
        swing*.05
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


/* =========================
   RENDER
========================= */

function render() {

    ctx.save();


    if (screenShake > 0) {

        ctx.translate(
            (Math.random()-.5) *
            screenShake,

            (Math.random()-.5) *
            screenShake
        );

    }


    /* 천장 */

    const ceil =
        ctx.createLinearGradient(
            0,
            0,
            0,
            canvas.height/2
        );

    ceil.addColorStop(
        0,
        "#080808"
    );

    ceil.addColorStop(
        1,
        "#221515"
    );

    ctx.fillStyle =
        ceil;

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height/2
    );


    /* 바닥 */

    const floor =
        ctx.createLinearGradient(
            0,
            canvas.height/2,
            0,
            canvas.height
        );

    floor.addColorStop(
        0,
        "#1c1010"
    );

    floor.addColorStop(
        1,
        "#050505"
    );

    ctx.fillStyle =
        floor;

    ctx.fillRect(
        0,
        canvas.height/2,
        canvas.width,
        canvas.height/2
    );


    const numRays = 180;

    const w =
        canvas.width /
        numRays;

    const curFlashRange =
        flashRange +
        (Math.random()-.5)*.25;


    const fov =
        Math.PI*.46;


    const projDist =
        (canvas.width/2) /
        Math.tan(fov/2);


    /* =========================
       RAYCASTING
    ========================= */

    for (
        let i=0;
        i<numRays;
        i++
    ) {

        const rayAngle =
            angle -
            fov/2 +
            (i/numRays)*fov;


        let distance = 0;

        let hit = false;

        let hitType = 1;

        let wallX = 0;


        while (
            !hit &&
            distance <
            curFlashRange
        ) {

            distance += .025;


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


                const fracX =
                    rx - tx;

                const fracY =
                    ry - ty;


                /*
                   벽면 좌표를 조금 더
                   안정적으로 계산
                */

                if (
                    Math.abs(
                        Math.cos(rayAngle)
                    ) >
                    Math.abs(
                        Math.sin(rayAngle)
                    )
                ) {

                    wallX =
                        fracY * 64;

                }

                else {

                    wallX =
                        fracX * 64;

                }

            }

        }


        const correctedDist =
            distance *
            Math.cos(
                rayAngle-angle
            );


        zBuffer[i] =
            correctedDist;


        const h =
            Math.min(
                canvas.height,
                projDist /
                (correctedDist+.0001)
            );


        const shade =
            Math.max(
                .12,
                1 -
                correctedDist /
                curFlashRange
            );


        const top =
            (canvas.height-h)/2;


        if (hitType === 3) {

            ctx.fillStyle =
                `rgba(
                    230,
                    190,
                    60,
                    ${shade}
                )`;

            ctx.fillRect(
                i*w,
                top,
                w+1,
                h
            );

        }

        else if (hitType === 2) {

            ctx.drawImage(
                doorTex,
                Math.floor(wallX),
                0,
                1,
                64,
                i*w,
                top,
                w+1,
                h
            );

            ctx.fillStyle =
                `rgba(
                    0,
                    0,
                    0,
                    ${1-shade}
                )`;

            ctx.fillRect(
                i*w,
                top,
                w+1,
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
                i*w,
                top,
                w+1,
                h
            );

            ctx.fillStyle =
                `rgba(
                    0,
                    0,
                    0,
                    ${1-shade}
                )`;

            ctx.fillRect(
                i*w,
                top,
                w+1,
                h
            );

        }

    }


    /* =========================
       FURNITURE
    ========================= */

    furnitureList.forEach(
        furn => {

            const dx =
                furn.x-px;

            const dy =
                furn.y-py;

            const dist =
                Math.hypot(dx,dy);


            let a =
                Math.atan2(
                    dy,
                    dx
                ) - angle;


            while (a < -Math.PI)
                a += Math.PI*2;

            while (a > Math.PI)
                a -= Math.PI*2;


            if (
                Math.abs(a) <
                fov/1.8 &&
                dist < curFlashRange
            ) {

                const sx =
                    canvas.width/2 +
                    Math.tan(a) *
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
                            projDist*.55/dist
                        );


                    const centerY =
                        canvas.height/2 +
                        size/2;


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


    /* =========================
       ITEMS
    ========================= */

    worldItems.forEach(
        item => {

            const dx =
                item.x-px;

            const dy =
                item.y-py;

            const dist =
                Math.hypot(dx,dy);


            let a =
                Math.atan2(
                    dy,
                    dx
                ) - angle;


            while (a < -Math.PI)
                a += Math.PI*2;

            while (a > Math.PI)
                a -= Math.PI*2;


            if (
                Math.abs(a) <
                fov/1.8 &&
                dist < curFlashRange
            ) {

                const sx =
                    canvas.width/2 +
                    Math.tan(a) *
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
                            projDist*.45/dist
                        );


                    const floatY =
                        Math.sin(
                            animTimer*2.5
                        )*5;


                    const centerY =
                        canvas.height/2 +
                        size/3 +
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
                        `bold ${
                            Math.max(
                                11,
                                Math.floor(
                                    size/2.2
                                )
                            )
                        }px sans-serif`;

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
                        size/1.2
                    );


                    ctx.restore();

                }

            }

        }
    );


    /* =========================
       GHOSTS
    ========================= */

    ghosts.forEach(
        g => {

            if (g.hp <= 0)
                return;


            const dx =
                g.x-px;

            const dy =
                g.y-py;

            const dist =
                Math.hypot(dx,dy);


            let a =
                Math.atan2(
                    dy,
                    dx
                ) - angle;


            while (a < -Math.PI)
                a += Math.PI*2;

            while (a > Math.PI)
                a -= Math.PI*2;


            if (
                Math.abs(a) <
                fov/1.8 &&
                dist < curFlashRange
            ) {

                const sx =
                    canvas.width/2 +
                    Math.tan(a) *
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
                            220,
                            projDist*.75/dist
                        );


                    const centerY =
                        canvas.height/2 +
                        size/4;


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


/* =========================
   GAME LOOP
========================= */

function gameLoop() {

    update();

    render();

    requestAnimationFrame(
        gameLoop
    );

}


initGame();

gameLoop();

</script>

</body>
</html>
"""

components.html(
    horror_game_html,
    height=620,
    scrolling=False
)
