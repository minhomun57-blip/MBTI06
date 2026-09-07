import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
page_title="🏚️ 저주받은 저택",
layout="wide"
)

st.title("🏚️ 저주받은 저택")
st.caption(
"W/A/S/D 이동 | ←/→ 시점 회전 | 마우스 드래그 시점 회전 | "
"E 달리기 | R 상호작용 | 1 회복약 | 2 배터리 | 3 퇴마부적 | 4 열쇠 확인 | 클릭 공격"
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
    background: #050505;
    overflow: hidden;
    font-family: "Courier New", monospace;
}

#canvas {
    width: 100%;
    height: 600px;
    display: block;
    background: #000;
    cursor: grab;
}

#canvas:active {
    cursor: grabbing;
}

/* ---------------- UI ---------------- */

#ui {
    position: absolute;
    top: 15px;
    left: 15px;
    z-index: 10;
    color: #ddd;
    font-size: 13px;
    pointer-events: none;
    text-shadow: 2px 2px 5px #000;
}

.bar {
    width: 220px;
    height: 12px;
    background: #111;
    border: 1px solid #555;
    margin-top: 3px;
}

.fill {
    height: 100%;
}

#hp {
    background: linear-gradient(90deg, #600, #f00);
}

#stamina {
    background: linear-gradient(90deg, #063, #0f5);
}

#weapon {
    margin-top: 8px;
    color: #ffcc44;
}

/* ---------------- 미니맵 ---------------- */

#mapBox {
    position: absolute;
    right: 15px;
    top: 15px;
    width: 190px;
    height: 190px;
    background: rgba(0,0,0,0.82);
    border: 2px solid #555;
    z-index: 10;
    box-shadow: 0 0 15px #000;
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
    height: 160px;
    display: block;
    margin: auto;
}

/* ---------------- 아이템 ---------------- */

#inventory {
    position: absolute;
    bottom: 15px;
    right: 15px;
    z-index: 10;
    display: flex;
    gap: 7px;
    pointer-events: none;
}

.slot {
    width: 67px;
    height: 65px;
    background: rgba(5,5,5,0.9);
    border: 1px solid #444;
    color: #aaa;
    text-align: center;
    font-size: 10px;
    padding-top: 4px;
}

.key {
    color: #ffbd2e;
    font-weight: bold;
}

/* ---------------- 메시지 ---------------- */

#msg {
    position: absolute;
    left: 50%;
    top: 32%;
    transform: translate(-50%, -50%);
    color: #ff3333;
    font-size: 20px;
    font-weight: bold;
    z-index: 20;
    text-align: center;
    text-shadow: 0 0 12px #000;
    pointer-events: none;
}

/* ---------------- 글리치 ---------------- */

#glitch {
    position: absolute;
    inset: 0;
    background:
        repeating-linear-gradient(
            0deg,
            rgba(255,0,0,0.15),
            rgba(255,0,0,0.15) 2px,
            transparent 2px,
            transparent 5px
        );
    opacity: 0;
    pointer-events: none;
    z-index: 15;
}

/* ---------------- 게임오버 ---------------- */

#gameover {
    display: none;
    position: absolute;
    inset: 0;
    z-index: 100;
    background: #080000;
    color: red;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

#ghostFace {
    width: 300px;
    height: 360px;
    border-radius: 48%;
    background: radial-gradient(circle, #911 0%, #300 55%, #000 100%);
    box-shadow: 0 0 100px red;
    position: relative;
    animation: shake 0.02s infinite alternate;
}

.eye {
    position: absolute;
    top: 25%;
    width: 55px;
    height: 75px;
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
    width: 14px;
    height: 14px;
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
    height: 120px;
    background: black;
    border: 3px solid #a00;
    border-radius: 20px 20px 60px 60px;
}

.teeth {
    height: 28px;
    background:
        repeating-linear-gradient(
            90deg,
            white,
            white 13px,
            #300 13px,
            #300 18px
        );
}

#gameoverText {
    margin-top: 25px;
    font-size: 25px;
    font-weight: bold;
}

#restart {
    margin-top: 20px;
    background: #080808;
    border: 1px solid red;
    color: red;
    padding: 12px 30px;
    cursor: pointer;
}

@keyframes shake {
    from {
        transform: translate(5px,-5px) scale(1.05);
    }
    to {
        transform: translate(-5px,5px) scale(1.1);
    }
}
</style>

</head>

<body>

<div id="ui">

```
<div>❤️ 생명력</div>
<div class="bar">
    <div id="hp" class="fill"></div>
</div>

<br>

<div>💨 스테미나</div>
<div class="bar">
    <div id="stamina" class="fill"></div>
</div>

<div id="weapon">
    무기: 맨손
</div>
```

</div>

<div id="mapBox">
    <div id="mapTitle">🗺️ 저택 지도</div>
    <canvas id="minimap"></canvas>
</div>

<div id="inventory">

```
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
    🔑 탈출열쇠
    <br>
    <span id="key">없음</span>
</div>
```

</div>

<div id="msg">
    R키: 문 열기 / 아이템 획득
</div>

<div id="glitch"></div>

<div id="gameover">

```
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

<div id="gameoverText">
    당신의 영혼은 저택에 갇혔습니다...
</div>

<button id="restart" onclick="resetGame()">
    다시 도전
</button>
```

</div>

<canvas id="canvas" tabindex="0"></canvas>

<script>

/* =========================================================
   기본 설정
========================================================= */

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

canvas.width = 900;
canvas.height = 600;

const mapCanvas = document.getElementById("minimap");
const mapCtx = mapCanvas.getContext("2d");

mapCanvas.width = 180;
mapCanvas.height = 160;

/* =========================================================
   사운드
========================================================= */

let audioCtx = null;

function initAudio() {

    if (!audioCtx) {
        audioCtx =
            new (window.AudioContext ||
            window.webkitAudioContext)();
    }
}

function sound(type) {

    if (!audioCtx) return;

    const now = audioCtx.currentTime;

    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();

    if (type === "door") {

        osc.type = "triangle";
        osc.frequency.setValueAtTime(110, now);
        osc.frequency.linearRampToValueAtTime(55, now + 0.3);

    }

    if (type === "item") {

        osc.type = "sine";
        osc.frequency.setValueAtTime(500, now);
        osc.frequency.exponentialRampToValueAtTime(
            1000,
            now + 0.2
        );

    }

    if (type === "attack") {

        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(160, now);
        osc.frequency.exponentialRampToValueAtTime(
            30,
            now + 0.15
        );

    }

    if (type === "hit") {

        osc.type = "square";
        osc.frequency.setValueAtTime(80, now);
        osc.frequency.exponentialRampToValueAtTime(
            15,
            now + 0.2
        );

    }

    if (type === "scare") {

        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(100, now);
        osc.frequency.exponentialRampToValueAtTime(
            1000,
            now + 0.5
        );

    }

    gain.gain.setValueAtTime(0.3, now);
    gain.gain.exponentialRampToValueAtTime(
        0.01,
        now + 0.3
    );

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start();
    osc.stop(now + 0.3);
}

/* =========================================================
   벽 텍스처
========================================================= */

const wallTex = document.createElement("canvas");

wallTex.width = 64;
wallTex.height = 64;

const wallCtx = wallTex.getContext("2d");

wallCtx.fillStyle = "#30201b";
wallCtx.fillRect(0,0,64,64);

wallCtx.fillStyle = "#17100d";

for(let y=0; y<64; y+=16) {

    wallCtx.fillRect(0,y,64,2);

    for(let x=0; x<64; x+=16) {

        let off = (y/16)%2 === 0 ? 0 : 8;

        wallCtx.fillRect(
            x + off,
            y,
            2,
            16
        );
    }
}

/* =========================================================
   낡은 일반 나무문 텍스처
========================================================= */

const doorTex = document.createElement("canvas");

doorTex.width = 128;
doorTex.height = 128;

const doorCtx = doorTex.getContext("2d");

/* 문 전체 */

doorCtx.fillStyle = "#24150d";
doorCtx.fillRect(0,0,128,128);

/* 나무판 */

doorCtx.fillStyle = "#55321b";
doorCtx.fillRect(7,4,114,120);

/* 세로 나뭇결 */

doorCtx.fillStyle = "#321b0e";

for(let x=12; x<120; x+=10) {
    doorCtx.fillRect(x,7,3,114);
}

/* 문 패널 */

function panel(x,y,w,h) {

    doorCtx.fillStyle = "#2a160b";
    doorCtx.fillRect(x,y,w,h);

    doorCtx.strokeStyle = "#79502b";
    doorCtx.lineWidth = 4;
    doorCtx.strokeRect(x,y,w,h);

    doorCtx.fillStyle = "#452817";
    doorCtx.fillRect(
        x+6,
        y+6,
        w-12,
        h-12
    );
}

panel(18,12,92,42);
panel(18,66,92,42);

/* 경첩 */

doorCtx.fillStyle = "#181818";

doorCtx.fillRect(8,18,8,15);
doorCtx.fillRect(8,91,8,15);

/* 손잡이 */

doorCtx.fillStyle = "#111";
doorCtx.beginPath();
doorCtx.arc(99,63,7,0,Math.PI*2);
doorCtx.fill();

doorCtx.fillStyle = "#b08b43";
doorCtx.beginPath();
doorCtx.arc(97,61,3,0,Math.PI*2);
doorCtx.fill();

/* 금 */
doorCtx.strokeStyle = "rgba(10,5,3,0.7)";
doorCtx.lineWidth = 2;

doorCtx.beginPath();
doorCtx.moveTo(35,8);
doorCtx.lineTo(42,30);
doorCtx.lineTo(35,51);
doorCtx.stroke();

doorCtx.beginPath();
doorCtx.moveTo(80,70);
doorCtx.lineTo(75,95);
doorCtx.lineTo(84,120);
doorCtx.stroke();

/* =========================================================
   지도
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

let houseMap;
const MAP_SIZE = initialMap.length;

/* =========================================================
   게임 상태
========================================================= */

/*
   시작 위치를 중앙의 넓은 복도로 설정.
   기존처럼 벽 바로 앞에서 시작하지 않음.
*/

let px = 9.5;
let py = 10.5;

let angle = 0;

let hp = 100;
let stamina = 100;

let flashlight = 12;

let gameOver = false;

let items = {
    potion: 0,
    battery: 0,
    talisman: 1,
    key: false,
    knife: false
};

/* 귀신 한 마리 */

let ghost;

let worldItems = [];
let furniture = [];

let attackTimer = 0;
let shake = 0;
let timer = 0;

/* =========================================================
   게임 초기화
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

    flashlight = 12;

    gameOver = false;

    items = {
        potion: 0,
        battery: 0,
        talisman: 1,
        key: false,
        knife: false
    };

    /*
       귀신을 남동쪽 구석에 배치.
       플레이어 시작점과 멀리 떨어져 있음.
    */

    ghost = {
        x: 17.5,
        y: 16.5,
        hp: 100,
        stun: 0
    };

    /* 아이템 */

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

    /*
       방마다 가구를 많이 배치.
       플레이어 이동을 막지 않도록
       벽 가까이에 배치.
    */

    furniture = [

        /* 북서쪽 서재 */

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

        /* 북동쪽 응급실 */

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

        /* 중앙 */

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

        /* 남서쪽 침실 */

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

        /* 남동쪽 */

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

    document.getElementById("gameover").style.display = "none";

    showMessage(
        "🏚️ 저택에 들어왔습니다. 열쇠를 찾아 탈출하세요.",
        "#ff3333"
    );

    updateUI();
}

/* =========================================================
   키보드
========================================================= */

const keys = {};

function normalizeKey(k) {

    if(k === "ArrowLeft") return "left";
    if(k === "ArrowRight") return "right";

    k = k.toLowerCase();

    if(k === "ㅈ") return "w";
    if(k === "ㄴ") return "s";
    if(k === "ㅁ") return "a";
    if(k === "ㅇ") return "d";
    if(k === "ㄷ") return "e";
    if(k === "ㄱ") return "r";

    return k;
}

window.addEventListener("keydown", function(e) {

    const k = normalizeKey(e.key);

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

    if(gameOver) return;

    if(k === "r") {
        interact();
    }

    if(e.key === "1") {
        usePotion();
    }

    if(e.key === "2") {
        useBattery();
    }

    if(e.key === "3") {
        useTalisman();
    }

    if(e.key === "4") {

        if(items.key) {

            showMessage(
                "🔑 탈출열쇠를 가지고 있습니다. 황금색 탈출문을 찾으세요.",
                "gold"
            );

        } else {

            showMessage(
                "🔒 아직 탈출열쇠가 없습니다.",
                "#aaa"
            );
        }
    }

});

window.addEventListener("keyup", function(e) {

    keys[normalizeKey(e.key)] = false;

});

/* =========================================================
   아이템 사용
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
            "❤️ 체력이 이미 가득합니다.",
            "#aaa"
        );

        return;
    }

    hp = Math.min(100, hp + 50);

    items.potion--;

    sound("item");

    showMessage(
        "💊 회복약을 사용했습니다.",
        "#66ff66"
    );

    updateUI();
}

function useBattery() {

    if(items.battery <= 0) {

        showMessage(
            "🔋 배터리가 없습니다.",
            "#aaa"
        );

        return;
    }

    flashlight = 18;

    items.battery--;

    sound("item");

    showMessage(
        "🔋 손전등의 밝기가 증가했습니다.",
        "#ffff66"
    );

    updateUI();
}

function useTalisman() {

    if(items.talisman <= 0) {

        showMessage(
            "📜 퇴마부적이 없습니다.",
            "#aaa"
        );

        return;
    }

    if(ghost.hp <= 0) return;

    const dx = ghost.x - px;
    const dy = ghost.y - py;

    const dist =
        Math.sqrt(dx*dx + dy*dy);

    if(dist < 7) {

        ghost.stun = 240;

        ghost.x += dx * 0.35;
        ghost.y += dy * 0.35;

        items.talisman--;

        shake = 10;

        sound("item");

        showMessage(
            "📜 퇴마부적으로 귀신을 밀어냈습니다!",
            "#00ffff"
        );

    } else {

        showMessage(
            "📜 주변에 귀신이 없습니다.",
            "#aaa"
        );
    }

    updateUI();
}

/* =========================================================
   상호작용
========================================================= */

function interact() {

    if(gameOver) return;

    let tx =
        Math.floor(
            px + Math.cos(angle) * 1.2
        );

    let ty =
        Math.floor(
            py + Math.sin(angle) * 1.2
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
                "🚪 낡은 문을 열었습니다.",
                "#ffcc66"
            );

            return;
        }
    }

    /* 아이템 */

    for(let i=worldItems.length-1; i>=0; i--) {

        const item = worldItems[i];

        const dx = px - item.x;
        const dy = py - item.y;

        const dist =
            Math.sqrt(dx*dx + dy*dy);

        if(dist < 1.4) {

            if(item.type === "knife") {

                items.knife = true;

                showMessage(
                    "🗡️ 녹슨 단검을 얻었습니다! 클릭해서 공격하세요.",
                    "#ffcc44"
                );

            }

            if(item.type === "potion") {

                items.potion++;

                showMessage(
                    "💊 회복약을 얻었습니다. [1] 사용",
                    "#ff6666"
                );

            }

            if(item.type === "battery") {

                items.battery++;

                showMessage(
                    "🔋 배터리를 얻었습니다. [2] 사용",
                    "#ffff66"
                );

            }

            if(item.type === "key") {

                items.key = true;

                showMessage(
                    "🔑 피묻은 열쇠를 얻었습니다! 탈출문을 찾으세요.",
                    "gold"
                );
            }

            worldItems.splice(i,1);

            sound("item");

            updateUI();

            return;
        }
    }

    showMessage(
        "주변에 상호작용할 것이 없습니다.",
        "#aaa"
    );
}

/* =========================================================
   마우스
========================================================= */

let mouseDown = false;
let lastMouseX = 0;

canvas.addEventListener("mousedown", function(e) {

    initAudio();

    canvas.focus();

    mouseDown = true;

    lastMouseX = e.clientX;

    if(items.knife && !gameOver) {

        attackTimer = 10;

        sound("attack");

        attack();
    }

});

window.addEventListener("mouseup", function() {

    mouseDown = false;

});

window.addEventListener("mousemove", function(e) {

    if(!mouseDown) return;

    const dx =
        e.clientX - lastMouseX;

    angle += dx * 0.006;

    lastMouseX = e.clientX;

});

/* =========================================================
   공격
========================================================= */

function attack() {

    if(ghost.hp <= 0) return;

    const dx =
        ghost.x - px;

    const dy =
        ghost.y - py;

    const dist =
        Math.sqrt(dx*dx + dy*dy);

    let a =
        Math.atan2(dy,dx) - angle;

    while(a < -Math.PI)
        a += Math.PI*2;

    while(a > Math.PI)
        a -= Math.PI*2;

    if(
        dist < 2.3 &&
        Math.abs(a) < 0.7
    ) {

        ghost.hp -= 50;

        ghost.stun = 60;

        shake = 8;

        sound("hit");

        if(ghost.hp <= 0) {

            showMessage(
                "💀 귀신을 성불시켰습니다!",
                "#00ffff"
            );
        }
    }
}

/* =========================================================
   충돌
========================================================= */

function solid(x,y) {

    if(
        x < 0 ||
        y < 0 ||
        x >= MAP_SIZE ||
        y >= MAP_SIZE
    ) return true;

    const tile =
        houseMap[
            Math.floor(y)
        ][
            Math.floor(x)
        ];

    return tile === 1 || tile === 2;
}

/* =========================================================
   업데이트
========================================================= */

function update() {

    if(gameOver) return;

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

    const running =
        keys["e"] && stamina > 0;

    let speed =
        running ? 0.065 : 0.038;

    if(running &&
       (keys["w"] ||
        keys["s"] ||
        keys["a"] ||
        keys["d"])) {

        stamina =
            Math.max(
                0,
                stamina - 0.5
            );

    } else {

        stamina =
            Math.min(
                100,
                stamina + 0.25
            );
    }

    let dx = 0;
    let dy = 0;

    if(keys["w"]) {

        dx +=
            Math.cos(angle) * speed;

        dy +=
            Math.sin(angle) * speed;
    }

    if(keys["s"]) {

        dx -=
            Math.cos(angle) * speed;

        dy -=
            Math.sin(angle) * speed;
    }

    if(keys["a"]) {

        dx +=
            Math.cos(angle - Math.PI/2) *
            speed;

        dy +=
            Math.sin(angle - Math.PI/2) *
            speed;
    }

    if(keys["d"]) {

        dx +=
            Math.cos(angle + Math.PI/2) *
            speed;

        dy +=
            Math.sin(angle + Math.PI/2) *
            speed;
    }

    const margin = 0.22;

    if(!solid(
        px + dx + Math.sign(dx)*margin,
        py
    )) {

        px += dx;
    }

    if(!solid(
        px,
        py + dy + Math.sign(dy)*margin
    )) {

        py += dy;
    }

    /* =====================================================
       귀신 AI
    ===================================================== */

    if(ghost.hp > 0) {

        const gx =
            px - ghost.x;

        const gy =
            py - ghost.y;

        const dist =
            Math.sqrt(gx*gx + gy*gy);

        if(ghost.stun > 0) {

            ghost.stun--;

        } else {

            /*
              플레이어와 너무 가까워지면 추적.
              하지만 시작 위치에서는 먼 곳에 있음.
            */

            if(dist < 12) {

                const mx =
                    (gx / dist) * 0.014;

                const my =
                    (gy / dist) * 0.014;

                if(!solid(
                    ghost.x + mx,
                    ghost.y
                )) {

                    ghost.x += mx;
                }

                if(!solid(
                    ghost.x,
                    ghost.y + my
                )) {

                    ghost.y += my;
                }
            }

            if(dist < 0.65) {

                hp -= 1.8;

                shake = 5;

                if(hp <= 0) {

                    triggerGameOver();
                }
            }
        }

        if(dist < 5.5) {

            document.getElementById(
                "glitch"
            ).style.opacity =
                ((5.5-dist)/5.5)*0.7;

        } else {

            document.getElementById(
                "glitch"
            ).style.opacity = 0;
        }

    } else {

        document.getElementById(
            "glitch"
        ).style.opacity = 0;
    }

    updateUI();
}

/* =========================================================
   UI
========================================================= */

function updateUI() {

    document.getElementById("hp").style.width =
        Math.max(0,hp) + "%";

    document.getElementById("stamina").style.width =
        Math.max(0,stamina) + "%";

    document.getElementById("weapon").innerText =
        items.knife
        ? "무기: 🗡️ 녹슨 단검"
        : "무기: 맨손";

    document.getElementById("potion").innerText =
        items.potion;

    document.getElementById("battery").innerText =
        items.battery;

    document.getElementById("talisman").innerText =
        items.talisman;

    document.getElementById("key").innerText =
        items.key ? "획득" : "없음";
}

function showMessage(text,color) {

    const el =
        document.getElementById("msg");

    el.innerText = text;

    el.style.color =
        color || "#ff3333";

    clearTimeout(
        window.msgTimer
    );

    window.msgTimer =
        setTimeout(function() {

            if(!gameOver)
                el.innerText = "";

        },3000);
}

/* =========================================================
   귀신 그래픽
========================================================= */

function drawGhost(
    sx,
    sy,
    size,
    stunned
) {

    ctx.save();

    ctx.translate(sx,sy);

    const alpha =
        stunned ? 0.35 : 0.9;

    ctx.fillStyle =
        `rgba(210,225,255,${alpha})`;

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
        -size/3,
        size/2
    );

    ctx.closePath();

    ctx.fill();

    /* 눈 */

    ctx.fillStyle =
        stunned ? "#00ffff" : "#ff0000";

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
   가구
========================================================= */

function drawFurniture(
    type,
    sx,
    sy,
    size
) {

    ctx.save();

    ctx.translate(sx,sy);

    if(type === "bookshelf") {

        ctx.fillStyle = "#3b2110";

        ctx.fillRect(
            -size/2,
            -size,
            size,
            size*1.2
        );

        ctx.fillStyle = "#111";

        ctx.fillRect(
            -size/2.3,
            -size/1.2,
            size/1.15,
            size
        );

        ctx.fillStyle = "#663";

        for(let y=-size/1.1;
            y<size/3;
            y+=size/3) {

            ctx.fillRect(
                -size/2.3,
                y,
                size/1.15,
                size/12
            );
        }

        ctx.fillStyle = "#933";

        ctx.fillRect(
            -size/3,
            -size/1.1,
            size/8,
            size/3
        );

        ctx.fillStyle = "#268";

        ctx.fillRect(
            -size/10,
            -size/1.1,
            size/8,
            size/3
        );

    } else if(type === "desk") {

        ctx.fillStyle = "#4b2b17";

        ctx.fillRect(
            -size/1.2,
            -size/5,
            size*1.4,
            size/6
        );

        ctx.fillStyle = "#281508";

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

        ctx.fillStyle = "#4a2915";

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

        ctx.fillStyle = "#573218";

        ctx.fillRect(
            -size/2,
            -size/8,
            size,
            size/7
        );

        ctx.fillStyle = "#2b170b";

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

        ctx.fillStyle = "#4b2a17";

        ctx.fillRect(
            -size/1.1,
            -size/4,
            size*1.4,
            size/2
        );

        ctx.fillStyle = "#aaa";

        ctx.fillRect(
            -size,
            -size/3,
            size*1.2,
            size/4
        );

        ctx.fillStyle = "#ddd";

        ctx.fillRect(
            -size/1.1,
            -size/2.7,
            size/2.7,
            size/5
        );

    } else if(type === "cabinet") {

        ctx.fillStyle = "#333";

        ctx.fillRect(
            -size/3,
            -size,
            size*0.7,
            size
        );

        ctx.fillStyle = "#777";

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

        ctx.fillStyle = "#3b210f";

        ctx.fillRect(
            -size/5,
            -size,
            size/2.5,
            size*1.2
        );

        ctx.fillStyle = "#eee";

        ctx.beginPath();

        ctx.arc(
            0,
            -size/1.3,
            size/6,
            0,
            Math.PI*2
        );

        ctx.fill();

    } else if(type === "candle") {

        ctx.fillStyle = "#866";

        ctx.fillRect(
            -size/15,
            -size/2,
            size/7,
            size/2
        );

        ctx.fillStyle = "#ffb000";

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
   아이템
========================================================= */

function drawItem(
    type,
    sx,
    sy,
    size
) {

    ctx.save();

    ctx.translate(sx,sy);

    if(type === "key") {

        ctx.strokeStyle = "#ffd700";
        ctx.lineWidth = size/7;

        ctx.beginPath();

        ctx.arc(
            0,
            -size/3,
            size/4,
            0,
            Math.PI*2
        );

        ctx.stroke();

        ctx.fillStyle = "#ffd700";

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

        ctx.fillStyle = "#ccc";

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

        ctx.fillStyle = "#542811";

        ctx.fillRect(
            -size/5,
            size/4,
            size/2.5,
            size/2
        );

    } else if(type === "potion") {

        ctx.fillStyle = "#e22";

        ctx.beginPath();

        ctx.arc(
            0,
            size/5,
            size/2.5,
            0,
            Math.PI*2
        );

        ctx.fill();

        ctx.fillStyle = "#865";

        ctx.fillRect(
            -size/6,
            -size/3,
            size/3,
            size/5
        );

    } else if(type === "battery") {

        ctx.fillStyle = "#222";

        ctx.fillRect(
            -size/3,
            -size/3,
            size/1.5,
            size
        );

        ctx.fillStyle = "#f60";

        ctx.fillRect(
            -size/3,
            0,
            size/1.5,
            size/2
        );

        ctx.fillStyle = "white";

        ctx.font =
            Math.floor(size/3) + "px Arial";

        ctx.textAlign = "center";

        ctx.fillText(
            "⚡",
            0,
            size/4
        );
    }

    ctx.restore();
}

/* =========================================================
   3D 렌더링
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
            canvas.height/2
        );

    ceiling.addColorStop(
        0,
        "#070707"
    );

    ceiling.addColorStop(
        1,
        "#241717"
    );

    ctx.fillStyle = ceiling;

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
        "#251515"
    );

    floor.addColorStop(
        1,
        "#030303"
    );

    ctx.fillStyle = floor;

    ctx.fillRect(
        0,
        canvas.height/2,
        canvas.width,
        canvas.height/2
    );

    const rays = 180;

    const fov =
        Math.PI * 0.43;

    const proj =
        (canvas.width/2) /
        Math.tan(fov/2);

    const zBuffer =
        new Array(rays).fill(999);

    const range =
        flashlight +
        (Math.random()-0.5)*0.15;

    const column =
        canvas.width/rays;

    /* 벽 */

    for(let i=0;i<rays;i++) {

        const rayAngle =
            angle -
            fov/2 +
            (i/rays)*fov;

        let distance = 0;

        let hitType = 1;

        let wallX = 0;

        while(distance < range) {

            distance += 0.025;

            const rx =
                px +
                Math.cos(rayAngle)*
                distance;

            const ry =
                py +
                Math.sin(rayAngle)*
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

                hitType = 1;
                break;
            }

            if(houseMap[ty][tx] > 0) {

                hitType =
                    houseMap[ty][tx];

                wallX =
                    (
                        (rx-tx) +
                        (ry-ty)
                    );

                wallX =
                    (
                        wallX -
                        Math.floor(wallX)
                    ) * 128;

                break;
            }
        }

        const corrected =
            distance *
            Math.cos(
                rayAngle-angle
            );

        zBuffer[i] = corrected;

        const height =
            Math.min(
                canvas.height,
                proj /
                (corrected+0.0001)
            );

        const brightness =
            Math.max(
                0.12,
                1 - corrected/range
            );

        if(hitType === 2) {

            ctx.drawImage(
                doorTex,
                Math.floor(wallX),
                0,
                1,
                128,
                i*column,
                (canvas.height-height)/2,
                column+1,
                height
            );

        } else {

            ctx.drawImage(
                wallTex,
                Math.floor(
                    wallX % 64
                ),
                0,
                1,
                64,
                i*column,
                (canvas.height-height)/2,
                column+1,
                height
            );
        }

        ctx.fillStyle =
            `rgba(0,0,0,${1-brightness})`;

        ctx.fillRect(
            i*column,
            (canvas.height-height)/2,
            column+1,
            height
        );
    }

    /* 가구 */

    const objects = [];

    furniture.forEach(f => {

        const dx = f.x-px;
        const dy = f.y-py;

        const dist =
            Math.sqrt(dx*dx+dy*dy);

        let a =
            Math.atan2(dy,dx)-angle;

        while(a < -Math.PI)
            a += Math.PI*2;

        while(a > Math.PI)
            a -= Math.PI*2;

        if(
            Math.abs(a) < fov/1.8 &&
            dist < range
        ) {

            objects.push({
                type: "furniture",
                data: f,
                dist: dist,
                angle: a
            });
        }
    });

    /* 아이템 */

    worldItems.forEach(item => {

        const dx = item.x-px;
        const dy = item.y-py;

        const dist =
            Math.sqrt(dx*dx+dy*dy);

        let a =
            Math.atan2(dy,dx)-angle;

        while(a < -Math.PI)
            a += Math.PI*2;

        while(a > Math.PI)
            a -= Math.PI*2;

        if(
            Math.abs(a) < fov/1.8 &&
            dist < range
        ) {

            objects.push({
                type: "item",
                data: item,
                dist: dist,
                angle: a
            });
        }
    });

    /* 귀신 */

    if(ghost.hp > 0) {

        const dx = ghost.x-px;
        const dy = ghost.y-py;

        const dist =
            Math.sqrt(dx*dx+dy*dy);

        let a =
            Math.atan2(dy,dx)-angle;

        while(a < -Math.PI)
            a += Math.PI*2;

        while(a > Math.PI)
            a -= Math.PI*2;

        if(
            Math.abs(a) < fov/1.8 &&
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

    /* 먼 것부터 */

    objects.sort(
        (a,b) => b.dist-a.dist
    );

    objects.forEach(obj => {

        const sx =
            canvas.width/2 +
            Math.tan(obj.angle)*proj;

        const ray =
            Math.floor(
                (sx/canvas.width)*rays
            );

        if(
            ray < 0 ||
            ray >= rays
        ) return;

        if(obj.dist > zBuffer[ray])
            return;

        if(obj.type === "furniture") {

            const size =
                Math.min(
                    170,
                    proj*0.55/obj.dist
                );

            drawFurniture(
                obj.data.type,
                sx,
                canvas.height/2+size/3,
                size
            );
        }

        if(obj.type === "item") {

            const size =
                Math.min(
                    100,
                    proj*0.4/obj.dist
                );

            const floating =
                Math.sin(timer*3)*4;

            drawItem(
                obj.data.type,
                sx,
                canvas.height/2+
                size/3+
                floating,
                size
            );

            ctx.save();

            ctx.fillStyle = "white";

            ctx.font =
                "bold " +
                Math.max(
                    10,
                    Math.floor(size/3)
                ) +
                "px Arial";

            ctx.textAlign = "center";

            ctx.shadowColor = "black";
            ctx.shadowBlur = 5;

            ctx.fillText(
                obj.data.name +
                " [R]",
                sx,
                canvas.height/2-
                size/1.1
            );

            ctx.restore();
        }

        if(obj.type === "ghost") {

            const size =
                Math.min(
                    220,
                    proj*0.7/obj.dist
                );

            drawGhost(
                sx,
                canvas.height/2+size/4,
                size,
                obj.data.stun > 0
            );
        }
    });

    /* 칼 */

    if(items.knife) {

        ctx.save();

        const swing =
            attackTimer > 0
            ? (10-attackTimer)*10
            : 0;

        ctx.translate(
            canvas.width-120-swing,
            canvas.height-80+swing
        );

        ctx.rotate(-0.6);

        ctx.fillStyle = "#aaa";

        ctx.fillRect(
            -8,
            -100,
            16,
            80
        );

        ctx.fillStyle = "#fff";

        ctx.fillRect(
            0,
            -100,
            8,
            80
        );

        ctx.fillStyle = "#542811";

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

    ctx.restore();

    drawMinimap();
}

/* =========================================================
   미니맵
========================================================= */

function drawMinimap() {

    const mw = 180;
    const mh = 160;

    mapCtx.fillStyle = "#080808";

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

    for(let y=0;y<MAP_SIZE;y++) {

        for(let x=0;x<MAP_SIZE;x++) {

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
                    "#0d0d0d";
            }

            mapCtx.fillRect(
                x*cell,
                y*cell,
                cell-1,
                cell-1
            );
        }
    }

    /* 아이템 */

    worldItems.forEach(item => {

        mapCtx.fillStyle =
            item.type === "key"
            ? "#ffd700"
            : "#66ff66";

        mapCtx.beginPath();

        mapCtx.arc(
            item.x*cell,
            item.y*cell,
            2.5,
            0,
            Math.PI*2
        );

        mapCtx.fill();
    });

    /* 귀신 */

    if(ghost.hp > 0) {

        mapCtx.fillStyle = "#ff2222";

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

    mapCtx.fillStyle = "#00ffff";

    mapCtx.beginPath();

    mapCtx.arc(
        px*cell,
        py*cell,
        4,
        0,
        Math.PI*2
    );

    mapCtx.fill();

    /* 플레이어 방향 */

    mapCtx.strokeStyle = "#00ffff";

    mapCtx.beginPath();

    mapCtx.moveTo(
        px*cell,
        py*cell
    );

    mapCtx.lineTo(
        (px+
        Math.cos(angle)*1.2)*cell,
        (py+
        Math.sin(angle)*1.2)*cell
    );

    mapCtx.stroke();
}

/* =========================================================
   게임오버
========================================================= */

function triggerGameOver() {

    gameOver = true;

    sound("scare");

    document.getElementById(
        "gameover"
    ).style.display = "flex";
}

function resetGame() {

    initGame();
}

/* =========================================================
   게임 루프
========================================================= */

function loop() {

    update();

    render();

    requestAnimationFrame(loop);
}

initGame();

loop();

</script>

</body>
</html>
"""

components.html(
horror_game_html,
height=640,
scrolling=False
)
