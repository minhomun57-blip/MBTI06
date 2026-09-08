import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🏚️ 저주받은 저택",
    layout="wide"
)

st.title("🏚️ 저주받은 저택")
st.caption(
    "W/A/S/D 이동 | ←/→ 시점 회전 | 마우스 드래그 시점 회전 | "
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
    background: #050505;
    overflow: hidden;
    font-family: "Courier New", monospace;
}

#canvas {
    width: 100%;
    height: 600px;
    display: block;
    background: #111;
    cursor: grab;
}

#canvas:active {
    cursor: grabbing;
}

#ui {
    position: absolute;
    top: 15px;
    left: 15px;
    z-index: 10;
    color: #fff;
    font-size: 14px;
    pointer-events: none;
    text-shadow: 2px 2px 5px #000;
    background: rgba(0,0,0,0.45);
    padding: 12px;
    border-radius: 8px;
    min-width: 245px;
}

.bar {
    width: 230px;
    height: 18px;
    background: #111;
    border: 2px solid #aaa;
    margin-top: 5px;
    border-radius: 4px;
    overflow: hidden;
    box-shadow: 0 0 8px #000;
}

.fill {
    height: 100%;
    transition: width 0.1s linear;
}

#hp {
    background: linear-gradient(
        90deg,
        #650000,
        #ff1111,
        #ff5555
    );
    width: 100%;
}

#stamina {
    background: linear-gradient(
        90deg,
        #006633,
        #00cc66,
        #66ff99
    );
    width: 100%;
}

.statusText {
    font-weight: bold;
    margin-top: 2px;
}

#weapon {
    margin-top: 10px;
    color: #ffcc44;
    font-weight: bold;
}

#mapBox {
    position: absolute;
    right: 15px;
    top: 15px;
    width: 190px;
    height: 190px;
    background: rgba(0,0,0,0.82);
    border: 2px solid #777;
    z-index: 10;
    box-shadow: 0 0 15px #000;
}

#mapTitle {
    color: #fff;
    text-align: center;
    padding: 5px;
    font-size: 12px;
    border-bottom: 1px solid #555;
}

#minimap {
    width: 180px;
    height: 160px;
    display: block;
    margin: auto;
}

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
    border: 1px solid #666;
    color: #ddd;
    text-align: center;
    font-size: 10px;
    padding-top: 4px;
    border-radius: 5px;
}

.key {
    color: #ffbd2e;
    font-weight: bold;
}

#msg {
    position: absolute;
    left: 50%;
    top: 32%;
    transform: translate(-50%, -50%);
    color: #ff5555;
    font-size: 20px;
    font-weight: bold;
    z-index: 20;
    text-align: center;
    text-shadow: 0 0 12px #000;
    pointer-events: none;
    background: rgba(0,0,0,0.3);
    padding: 8px 15px;
    border-radius: 6px;
}

#glitch {
    position: absolute;
    inset: 0;
    background:
        repeating-linear-gradient(
            0deg,
            rgba(255,0,0,0.08),
            rgba(255,0,0,0.08) 2px,
            transparent 2px,
            transparent 5px
        );
    opacity: 0;
    pointer-events: none;
    z-index: 15;
}

#gameover {
    display: none;
    position: absolute;
    inset: 0;
    z-index: 100;
    background: rgba(8,0,0,0.97);
    color: red;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

#ghostFace {
    width: 300px;
    height: 360px;
    border-radius: 48%;
    background: radial-gradient(
        circle,
        #911 0%,
        #300 55%,
        #000 100%
    );
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
    <div class="statusText">❤️ 생명력 <span id="hpText">100 / 100</span></div>
    <div class="bar">
        <div id="hp" class="fill"></div>
    </div>

    <br>

    <div class="statusText">💨 스테미나 <span id="staminaText">100 / 100</span></div>
    <div class="bar">
        <div id="stamina" class="fill"></div>
    </div>

    <div id="weapon">
        무기: 맨손
    </div>
</div>

<div id="mapBox">
    <div id="mapTitle">🗺️ 저택 지도</div>
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
        🔑 탈출열쇠
        <br>
        <span id="key">없음</span>
    </div>
</div>

<div id="msg">
    R키: 문 열기 / 아이템 획득
</div>

<div id="glitch"></div>

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

    <div id="gameoverText">
        당신의 영혼은 저택에 갇혔습니다...
    </div>

    <button id="restart" onclick="resetGame()">
        다시 도전
    </button>
</div>

<canvas id="canvas" tabindex="0"></canvas>

<script>

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
        audioCtx = new (
            window.AudioContext ||
            window.webkitAudioContext
        )();
    }

    if (audioCtx.state === "suspended") {
        audioCtx.resume();
    }
}

function sound(type) {

    initAudio();

    if (!audioCtx) return;

    const now = audioCtx.currentTime;

    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();

    if (type === "door") {
        osc.type = "triangle";
        osc.frequency.setValueAtTime(110, now);
        osc.frequency.linearRampToValueAtTime(
            55,
            now + 0.3
        );
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

    gain.gain.setValueAtTime(0.25, now);
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

wallCtx.fillStyle = "#61483d";
wallCtx.fillRect(0,0,64,64);

wallCtx.fillStyle = "#38251f";

for(let y=0; y<64; y+=16) {

    wallCtx.fillRect(0,y,64,2);

    for(let x=0; x<64; x+=16) {

        let off =
            (y/16)%2 === 0
            ? 0
            : 8;

        wallCtx.fillRect(
            x + off,
            y,
            2,
            16
        );
    }
}

/* =========================================================
   문 텍스처
========================================================= */

const doorTex = document.createElement("canvas");

doorTex.width = 128;
doorTex.height = 128;

const doorCtx = doorTex.getContext("2d");

doorCtx.fillStyle = "#422a1a";
doorCtx.fillRect(0,0,128,128);

doorCtx.fillStyle = "#704625";
doorCtx.fillRect(7,4,114,120);

doorCtx.fillStyle = "#3d2414";

for(let x=12; x<120; x+=10) {
    doorCtx.fillRect(x,7,3,114);
}

function panel(x,y,w,h) {

    doorCtx.fillStyle = "#2a160b";
    doorCtx.fillRect(x,y,w,h);

    doorCtx.strokeStyle = "#926438";
    doorCtx.lineWidth = 4;
    doorCtx.strokeRect(x,y,w,h);

    doorCtx.fillStyle = "#54351f";
    doorCtx.fillRect(
        x+6,
        y+6,
        w-12,
        h-12
    );
}

panel(18,12,92,42);
panel(18,66,92,42);

doorCtx.fillStyle = "#181818";

doorCtx.fillRect(8,18,8,15);
doorCtx.fillRect(8,91,8,15);

doorCtx.fillStyle = "#c49b4c";

doorCtx.beginPath();
doorCtx.arc(97,61,4,0,Math.PI*2);
doorCtx.fill();

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
   맵
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

let px = 9.5;
let py = 10.5;

let angle = 0;

let hp = 100;
let stamina = 100;

let flashlight = 16;

let gameOver = false;

let items = {
    potion: 0,
    battery: 0,
    talisman: 1,
    key: false,
    knife: false
};

let ghost;

let worldItems = [];
let furniture = [];

let attackTimer = 0;
let shake = 0;
let timer = 0;

/* =========================================================
   가구 충돌 반경
========================================================= */

const furnitureCollision = {
    bookshelf: 0.55,
    desk: 0.65,
    chair: 0.45,
    table: 0.65,
    bed: 0.75,
    cabinet: 0.55,
    clock: 0.35,
    candle: 0.25
};

function furnitureSolid(x, y, radius = 0.2) {

    for(const f of furniture) {

        const r =
            (furnitureCollision[f.type] || 0.4) +
            radius;

        const dx = x - f.x;
        const dy = y - f.y;

        if(dx*dx + dy*dy < r*r) {
            return true;
        }
    }

    return false;
}

/* =========================================================
   초기화
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

    flashlight = 16;

    gameOver = false;

    items = {
        potion: 0,
        battery: 0,
        talisman: 1,
        key: false,
        knife: false
    };

    /*
       귀신 시작 위치를 플레이어와 멀리 떨어진
       남동쪽 방으로 설정.
    */

    ghost = {
        x: 17.5,
        y: 16.5,
        hp: 100,
        stun: 0,
        pathTimer: 0,
        path: []
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

    showMessage(
        "🏚️ 저택에 들어왔습니다. 열쇠를 찾아 탈출하세요.",
        "#ff5555"
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

    initAudio();

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
   아이템
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

    hp = Math.min(
        100,
        hp + 50
    );

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

    flashlight = 20;

    items.battery--;

    sound("item");

    showMessage(
        "🔋 손전등이 밝아졌습니다.",
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

        const len = Math.max(dist, 0.01);

        const nx = dx / len;
        const ny = dy / len;

        /*
           부적으로 밀어낼 때도 벽 안으로 들어가지 않도록
           안전한 위치를 검사한다.
        */

        moveGhostSafely(
            nx * 1.0,
            ny * 1.0
        );

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

    const dx = ghost.x - px;
    const dy = ghost.y - py;

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
   기본 벽 충돌
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
   전체 충돌
========================================================= */

function playerBlocked(x, y) {

    const margin = 0.22;

    if(
        solid(x + margin, y) ||
        solid(x - margin, y) ||
        solid(x, y + margin) ||
        solid(x, y - margin)
    ) {
        return true;
    }

    if(furnitureSolid(x, y, 0.22)) {
        return true;
    }

    return false;
}

function ghostBlocked(x, y) {

    const margin = 0.25;

    if(
        solid(x + margin, y) ||
        solid(x - margin, y) ||
        solid(x, y + margin) ||
        solid(x, y - margin)
    ) {
        return true;
    }

    /*
       귀신도 가구를 통과하지 못하게 함.
    */

    if(furnitureSolid(x, y, 0.25)) {
        return true;
    }

    return false;
}

/* =========================================================
   귀신 안전 이동
========================================================= */

function moveGhostSafely(dx, dy) {

    const nx = ghost.x + dx;
    const ny = ghost.y + dy;

    if(!ghostBlocked(nx, ghost.y)) {
        ghost.x = nx;
    }

    if(!ghostBlocked(ghost.x, ny)) {
        ghost.y = ny;
    }
}

/* =========================================================
   BFS 길찾기
========================================================= */

function isWalkableCell(x, y) {

    if(
        x < 0 ||
        y < 0 ||
        x >= MAP_SIZE ||
        y >= MAP_SIZE
    ) {
        return false;
    }

    if(houseMap[y][x] !== 0) {
        return false;
    }

    /*
       귀신 길찾기에서 가구도 장애물로 취급.
    */

    for(const f of furniture) {

        const fx = Math.floor(f.x);
        const fy = Math.floor(f.y);

        if(
            fx === x &&
            fy === y
        ) {
            return false;
        }
    }

    return true;
}

function findGhostPath() {

    const startX =
        Math.floor(ghost.x);

    const startY =
        Math.floor(ghost.y);

    const targetX =
        Math.floor(px);

    const targetY =
        Math.floor(py);

    if(
        startX === targetX &&
        startY === targetY
    ) {
        return [];
    }

    const queue = [];

    const visited =
        Array.from(
            {length: MAP_SIZE},
            () => Array(MAP_SIZE).fill(false)
        );

    const parent =
        Array.from(
            {length: MAP_SIZE},
            () => Array(MAP_SIZE).fill(null)
        );

    queue.push({
        x: startX,
        y: startY
    });

    if(
        startX >= 0 &&
        startX < MAP_SIZE &&
        startY >= 0 &&
        startY < MAP_SIZE
    ) {
        visited[startY][startX] = true;
    }

    const dirs = [
        {x:1,y:0},
        {x:-1,y:0},
        {x:0,y:1},
        {x:0,y:-1}
    ];

    let found = false;

    while(queue.length > 0) {

        const current =
            queue.shift();

        for(const d of dirs) {

            const nx =
                current.x + d.x;

            const ny =
                current.y + d.y;

            if(
                nx < 0 ||
                ny < 0 ||
                nx >= MAP_SIZE ||
                ny >= MAP_SIZE
            ) {
                continue;
            }

            if(visited[ny][nx]) {
                continue;
            }

            if(!isWalkableCell(nx,ny)) {
                continue;
            }

            visited[ny][nx] = true;

            parent[ny][nx] = current;

            queue.push({
                x:nx,
                y:ny
            });

            if(
                nx === targetX &&
                ny === targetY
            ) {

                found = true;
                queue.length = 0;
                break;
            }
        }
    }

    if(!found) {
        return [];
    }

    const path = [];

    let current = {
        x: targetX,
        y: targetY
    };

    while(
        current.x !== startX ||
        current.y !== startY
    ) {

        path.push(current);

        const p =
            parent[current.y][current.x];

        if(!p) {
            return [];
        }

        current = p;
    }

    path.reverse();

    return path;
}

/* =========================================================
   업데이트
========================================================= */

function update() {

    if(gameOver) return;

    timer += 0.05;

    if(shake > 0) {
        shake--;
    }

    if(attackTimer > 0) {
        attackTimer--;
    }

    if(keys["left"]) {
        angle -= 0.045;
    }

    if(keys["right"]) {
        angle += 0.045;
    }

    const running =
        keys["e"] &&
        stamina > 0;

    let speed =
        running
        ? 0.065
        : 0.038;

    if(
        running &&
        (
            keys["w"] ||
            keys["s"] ||
            keys["a"] ||
            keys["d"]
        )
    ) {

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

    /*
       플레이어가 벽과 가구를 통과하지 못하도록
       X/Y 축을 각각 따로 검사.
    */

    if(dx !== 0) {

        if(
            !playerBlocked(
                px + dx,
                py
            )
        ) {
            px += dx;
        }
    }

    if(dy !== 0) {

        if(
            !playerBlocked(
                px,
                py + dy
            )
        ) {
            py += dy;
        }
    }

    /* =====================================================
       귀신 AI
    ===================================================== */

    if(ghost.hp > 0) {

        const gx = px - ghost.x;
        const gy = py - ghost.y;

        const dist =
            Math.sqrt(
                gx*gx +
                gy*gy
            );

        if(ghost.stun > 0) {

            ghost.stun--;

        } else {

            /*
               일정 거리마다 BFS로 새 경로 계산.
               이제 귀신은 직선으로 벽을 뚫고 오는 것이 아니라
               실제 맵의 통로를 따라 이동한다.
            */

            ghost.pathTimer--;

            if(
                ghost.pathTimer <= 0 ||
                ghost.path.length === 0
            ) {

                ghost.path =
                    findGhostPath();

                ghost.pathTimer = 25;
            }

            if(
                ghost.path.length > 0 &&
                dist < 14
            ) {

                const target =
                    ghost.path[0];

                const tx =
                    target.x + 0.5;

                const ty =
                    target.y + 0.5;

                const vx =
                    tx - ghost.x;

                const vy =
                    ty - ghost.y;

                const vdist =
                    Math.sqrt(
                        vx*vx +
                        vy*vy
                    );

                if(vdist < 0.12) {

                    ghost.path.shift();

                } else {

                    const ghostSpeed = 0.014;

                    const mx =
                        vx / vdist *
                        ghostSpeed;

                    const my =
                        vy / vdist *
                        ghostSpeed;

                    /*
                       이동 전후 모두 충돌 검사.
                    */

                    if(
                        !ghostBlocked(
                            ghost.x + mx,
                            ghost.y
                        )
                    ) {
                        ghost.x += mx;
                    }

                    if(
                        !ghostBlocked(
                            ghost.x,
                            ghost.y + my
                        )
                    ) {
                        ghost.y += my;
                    }
                }
            }

            if(dist < 0.65) {

                hp -= 1.8;

                shake = 5;

                if(hp <= 0) {

                    hp = 0;

                    triggerGameOver();
                }
            }
        }

        if(dist < 5.5) {

            document.getElementById(
                "glitch"
            ).style.opacity =
                (
                    (5.5-dist) /
                    5.5
                ) * 0.45;

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

    const hpPercent =
        Math.max(
            0,
            Math.min(100, hp)
        );

    const staminaPercent =
        Math.max(
            0,
            Math.min(100, stamina)
        );

    document.getElementById(
        "hp"
    ).style.width =
        hpPercent + "%";

    document.getElementById(
        "stamina"
    ).style.width =
        staminaPercent + "%";

    document.getElementById(
        "hpText"
    ).innerText =
        Math.ceil(hp) +
        " / 100";

    document.getElementById(
        "staminaText"
    ).innerText =
        Math.ceil(stamina) +
        " / 100";

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

            if(!gameOver) {
                el.innerText = "";
            }

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
        `rgba(220,235,255,${alpha})`;

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

    ctx.fillStyle =
        stunned
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

        ctx.fillStyle = "#4d2d15";

        ctx.fillRect(
            -size/2,
            -size,
            size,
            size*1.2
        );

        ctx.fillStyle = "#17100c";

        ctx.fillRect(
            -size/2.3,
            -size/1.2,
            size/1.15,
            size
        );

        ctx.fillStyle = "#8a6235";

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

        ctx.fillStyle = "#b33";

        ctx.fillRect(
            -size/3,
            -size/1.1,
            size/8,
            size/3
        );

        ctx.fillStyle = "#368";

        ctx.fillRect(
            -size/10,
            -size/1.1,
            size/8,
            size/3
        );

    } else if(type === "desk") {

        ctx.fillStyle = "#633b20";

        ctx.fillRect(
            -size/1.2,
            -size/5,
            size*1.4,
            size/6
        );

        ctx.fillStyle = "#321b0d";

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

        ctx.fillStyle = "#60381e";

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

        ctx.fillStyle = "#704522";

        ctx.fillRect(
            -size/2,
            -size/8,
            size,
            size/7
        );

        ctx.fillStyle = "#321b0d";

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

        ctx.fillStyle = "#63391d";

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

        ctx.fillStyle = "#444";

        ctx.fillRect(
            -size/3,
            -size,
            size*0.7,
            size
        );

        ctx.fillStyle = "#aaa";

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

        ctx.fillStyle = "#4a2912";

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

        ctx.fillStyle = "#987";

        ctx.fillRect(
            -size/15,
            -size/2,
            size/7,
            size/2
        );

        ctx.fillStyle = "#ffcc22";

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
            Math.floor(size/3) +
            "px Arial";

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

    /*
       밝은 천장
    */

    const ceiling =
        ctx.createLinearGradient(
            0,
            0,
            0,
            canvas.height/2
        );

    ceiling.addColorStop(
        0,
        "#181818"
    );

    ceiling.addColorStop(
        0.5,
        "#382c2c"
    );

    ceiling.addColorStop(
        1,
        "#5a4242"
    );

    ctx.fillStyle = ceiling;

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height/2
    );

    /*
       밝은 바닥
    */

    const floor =
        ctx.createLinearGradient(
            0,
            canvas.height/2,
            0,
            canvas.height
        );

    floor.addColorStop(
        0,
        "#634444"
    );

    floor.addColorStop(
        0.45,
        "#3c2929"
    );

    floor.addColorStop(
        1,
        "#171111"
    );

    ctx.fillStyle = floor;

    ctx.fillRect(
        0,
        canvas.height/2,
        canvas.width,
        canvas.height/2
    );

    /*
       중앙 조명 효과
    */

    const light =
        ctx.createRadialGradient(
            canvas.width/2,
            canvas.height/2,
            20,
            canvas.width/2,
            canvas.height/2,
            450
        );

    light.addColorStop(
        0,
        "rgba(255,220,180,0.20)"
    );

    light.addColorStop(
        0.45,
        "rgba(255,190,150,0.10)"
    );

    light.addColorStop(
        1,
        "rgba(0,0,0,0)"
    );

    ctx.fillStyle = light;

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    const rays = 180;

    const fov =
        Math.PI * 0.43;

    const proj =
        (canvas.width/2) /
        Math.tan(fov/2);

    const zBuffer =
        new Array(rays).fill(999);

    /*
       손전등 범위를 기존보다 크게.
    */

    const range =
        flashlight +
        2 +
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

        /*
           기존보다 훨씬 밝게.
        */

        const brightness =
            Math.max(
                0.34,
                1.15 -
                corrected/(range*1.05)
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
            `rgba(0,0,0,${Math.max(
                0,
                0.55-brightness*0.45
            )})`;

        ctx.fillRect(
            i*column,
            (canvas.height-height)/2,
            column+1,
            height
        );
    }

    const objects = [];

    furniture.forEach(f => {

        const dx = f.x-px;
        const dy = f.y-py;

        const dist =
            Math.sqrt(
                dx*dx +
                dy*dy
            );

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

    worldItems.forEach(item => {

        const dx = item.x-px;
        const dy = item.y-py;

        const dist =
            Math.sqrt(
                dx*dx+
                dy*dy
            );

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

    if(ghost.hp > 0) {

        const dx = ghost.x-px;
        const dy = ghost.y-py;

        const dist =
            Math.sqrt(
                dx*dx+
                dy*dy
            );

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

    objects.sort(
        (a,b) =>
            b.dist-a.dist
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

        if(
            obj.dist >
            zBuffer[ray] + 0.1
        ) return;

        if(obj.type === "furniture") {

            const size =
                Math.min(
                    170,
                    proj*0.55/
                    obj.dist
                );

            drawFurniture(
                obj.data.type,
                sx,
                canvas.height/2+
                size/3,
                size
            );
        }

        if(obj.type === "item") {

            const size =
                Math.min(
                    100,
                    proj*0.4/
                    obj.dist
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
                    proj*0.7/
                    obj.dist
                );

            drawGhost(
                sx,
                canvas.height/2+
                size/4,
                size,
                obj.data.stun > 0
            );
        }
    });

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

    mapCtx.fillStyle = "#050505";

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
                    "#555";

            } else if(tile === 2) {

                mapCtx.fillStyle =
                    "#9a6325";

            } else {

                mapCtx.fillStyle =
                    "#1d1d1d";
            }

            mapCtx.fillRect(
                x*cell,
                y*cell,
                cell-1,
                cell-1
            );
        }
    }

    /*
       가구 표시
    */

    furniture.forEach(f => {

        mapCtx.fillStyle =
            "#6b5140";

        mapCtx.fillRect(
            (f.x-0.25)*cell,
            (f.y-0.25)*cell,
            cell*0.5,
            cell*0.5
        );
    });

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

    mapCtx.strokeStyle = "#00ffff";

    mapCtx.beginPath();

    mapCtx.moveTo(
        px*cell,
        py*cell
    );

    mapCtx.lineTo(
        (
            px+
            Math.cos(angle)*1.2
        )*cell,
        (
            py+
            Math.sin(angle)*1.2
        )*cell
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
