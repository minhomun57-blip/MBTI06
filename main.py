```python
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🏚️ 저주받은 저택",
    layout="wide"
)

st.title("🏚️ 저주받은 저택")

st.caption(
    "W/A/S/D 이동 | ←/→ 시점 회전 | 마우스 드래그 시점 회전 | "
    "E 달리기 | R 상호작용 | 1 회복약 | 2 배터리 | 3 퇴마부적 | "
    "4 열쇠 확인 | 클릭 공격"
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
    background: #111;
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

/* =====================================================
   UI
===================================================== */

#ui {
    position: absolute;
    top: 15px;
    left: 15px;
    z-index: 30;

    width: 250px;

    color: #fff;
    font-size: 14px;

    pointer-events: none;

    text-shadow:
        2px 2px 4px #000,
        0 0 8px #000;

    background: rgba(0,0,0,0.55);

    padding: 12px;

    border: 1px solid rgba(255,255,255,0.25);

    border-radius: 6px;
}

/* 체력 제목 */

.statusTitle {
    font-weight: bold;
    margin-bottom: 4px;
}

/* =====================================================
   체력 / 스테미나 바
===================================================== */

.bar {
    width: 230px;
    height: 18px;

    background: #080808;

    border: 2px solid #aaa;

    border-radius: 4px;

    overflow: hidden;

    margin-top: 4px;
    margin-bottom: 12px;

    box-shadow:
        inset 0 0 5px #000,
        0 0 5px rgba(255,255,255,0.15);
}

.fill {
    height: 100%;

    transition:
        width 0.15s linear;
}

#hp {
    width: 100%;

    background:
        linear-gradient(
            90deg,
            #550000,
            #ff0000,
            #ff5555
        );

    box-shadow:
        0 0 8px red;
}

#stamina {
    width: 100%;

    background:
        linear-gradient(
            90deg,
            #004422,
            #00cc66,
            #66ff99
        );

    box-shadow:
        0 0 8px #00ff66;
}

/* 숫자 */

.barText {
    position: relative;

    top: -31px;

    text-align: center;

    color: white;

    font-size: 12px;

    font-weight: bold;

    height: 0;

    text-shadow:
        2px 2px 3px #000;
}

#weapon {
    margin-top: 2px;

    color: #ffd34d;

    font-weight: bold;

    font-size: 14px;
}

/* =====================================================
   미니맵
===================================================== */

#mapBox {
    position: absolute;

    right: 15px;
    top: 15px;

    width: 200px;
    height: 200px;

    background:
        rgba(0,0,0,0.88);

    border:
        2px solid #777;

    z-index: 30;

    box-shadow:
        0 0 20px #000;
}

#mapTitle {
    color: white;

    text-align: center;

    padding: 6px;

    font-size: 12px;

    border-bottom:
        1px solid #444;
}

#minimap {
    width: 190px;
    height: 170px;

    display: block;

    margin: auto;
}

/* =====================================================
   인벤토리
===================================================== */

#inventory {
    position: absolute;

    bottom: 15px;
    right: 15px;

    z-index: 30;

    display: flex;

    gap: 7px;

    pointer-events: none;
}

.slot {
    width: 67px;
    height: 65px;

    background:
        rgba(5,5,5,0.92);

    border:
        1px solid #555;

    color: #ddd;

    text-align: center;

    font-size: 10px;

    padding-top: 5px;

    border-radius: 4px;

    box-shadow:
        0 0 8px #000;
}

.key {
    color: #ffcc33;

    font-weight: bold;
}

/* =====================================================
   메시지
===================================================== */

#msg {
    position: absolute;

    left: 50%;
    top: 32%;

    transform:
        translate(-50%, -50%);

    color: #ff3333;

    font-size: 20px;

    font-weight: bold;

    z-index: 40;

    text-align: center;

    text-shadow:
        0 0 10px #000,
        2px 2px 4px #000;

    pointer-events: none;

    padding: 10px 18px;

    background:
        rgba(0,0,0,0.25);

    border-radius: 5px;
}

/* =====================================================
   화면 글리치
===================================================== */

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

    z-index: 35;
}

/* =====================================================
   게임오버
===================================================== */

#gameover {
    display: none;

    position: absolute;

    inset: 0;

    z-index: 100;

    background:
        radial-gradient(
            circle,
            #350000,
            #080000 70%
        );

    color: red;

    align-items: center;

    justify-content: center;

    flex-direction: column;
}

#ghostFace {
    width: 300px;
    height: 360px;

    border-radius: 48%;

    background:
        radial-gradient(
            circle,
            #911 0%,
            #300 55%,
            #000 100%
        );

    box-shadow:
        0 0 100px red;

    position: relative;

    animation:
        shake 0.02s infinite alternate;
}

.eye {
    position: absolute;

    top: 25%;

    width: 55px;
    height: 75px;

    background: white;

    border-radius: 50%;

    box-shadow:
        0 0 20px red;
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

    border-radius:
        20px 20px 60px 60px;
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

<div id="ui">

    <div class="statusTitle">
        ❤️ 생명력
    </div>

    <div class="bar">
        <div id="hp" class="fill"></div>
    </div>

    <div class="barText">
        <span id="hpText">100 / 100</span>
    </div>

    <div class="statusTitle">
        💨 스테미나
    </div>

    <div class="bar">
        <div id="stamina" class="fill"></div>
    </div>

    <div class="barText">
        <span id="staminaText">100 / 100</span>
    </div>

    <div id="weapon">
        무기: 맨손
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

/* =====================================================
   기본 설정
===================================================== */

const canvas =
    document.getElementById("canvas");

const ctx =
    canvas.getContext("2d");

canvas.width = 900;
canvas.height = 600;


const mapCanvas =
    document.getElementById("minimap");

const mapCtx =
    mapCanvas.getContext("2d");

mapCanvas.width = 190;
mapCanvas.height = 170;


/* =====================================================
   사운드
===================================================== */

let audioCtx = null;

function initAudio() {

    if(!audioCtx) {

        audioCtx =
            new (
                window.AudioContext ||
                window.webkitAudioContext
            )();
    }
}


function sound(type) {

    if(!audioCtx) return;

    const now =
        audioCtx.currentTime;

    const osc =
        audioCtx.createOscillator();

    const gain =
        audioCtx.createGain();


    if(type === "door") {

        osc.type = "triangle";

        osc.frequency.setValueAtTime(
            110,
            now
        );

        osc.frequency.linearRampToValueAtTime(
            55,
            now + 0.3
        );
    }


    if(type === "item") {

        osc.type = "sine";

        osc.frequency.setValueAtTime(
            500,
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
            160,
            now
        );

        osc.frequency.exponentialRampToValueAtTime(
            30,
            now + 0.15
        );
    }


    if(type === "hit") {

        osc.type = "square";

        osc.frequency.setValueAtTime(
            80,
            now
        );

        osc.frequency.exponentialRampToValueAtTime(
            15,
            now + 0.2
        );
    }


    if(type === "scare") {

        osc.type = "sawtooth";

        osc.frequency.setValueAtTime(
            100,
            now
        );

        osc.frequency.exponentialRampToValueAtTime(
            1000,
            now + 0.5
        );
    }


    gain.gain.setValueAtTime(
        0.3,
        now
    );

    gain.gain.exponentialRampToValueAtTime(
        0.01,
        now + 0.3
    );


    osc.connect(gain);

    gain.connect(
        audioCtx.destination
    );

    osc.start();

    osc.stop(
        now + 0.3
    );
}


/* =====================================================
   벽 텍스처
===================================================== */

const wallTex =
    document.createElement("canvas");

wallTex.width = 64;
wallTex.height = 64;

const wallCtx =
    wallTex.getContext("2d");


wallCtx.fillStyle =
    "#4a332b";

wallCtx.fillRect(
    0,
    0,
    64,
    64
);


wallCtx.fillStyle =
    "#241713";


for(
    let y = 0;
    y < 64;
    y += 16
) {

    wallCtx.fillRect(
        0,
        y,
        64,
        2
    );

    for(
        let x = 0;
        x < 64;
        x += 16
    ) {

        const off =
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


/* =====================================================
   문 텍스처
===================================================== */

const doorTex =
    document.createElement("canvas");

doorTex.width = 128;
doorTex.height = 128;

const doorCtx =
    doorTex.getContext("2d");


doorCtx.fillStyle =
    "#3b2414";

doorCtx.fillRect(
    0,
    0,
    128,
    128
);


doorCtx.fillStyle =
    "#704522";

doorCtx.fillRect(
    7,
    4,
    114,
    120
);


doorCtx.fillStyle =
    "#39200f";


for(
    let x = 12;
    x < 120;
    x += 10
) {

    doorCtx.fillRect(
        x,
        7,
        3,
        114
    );
}


function panel(x,y,w,h) {

    doorCtx.fillStyle =
        "#29160b";

    doorCtx.fillRect(
        x,
        y,
        w,
        h
    );

    doorCtx.strokeStyle =
        "#9a6738";

    doorCtx.lineWidth = 4;

    doorCtx.strokeRect(
        x,
        y,
        w,
        h
    );

    doorCtx.fillStyle =
        "#54321b";

    doorCtx.fillRect(
        x+6,
        y+6,
        w-12,
        h-12
    );
}


panel(
    18,
    12,
    92,
    42
);

panel(
    18,
    66,
    92,
    42
);


doorCtx.fillStyle =
    "#111";

doorCtx.beginPath();

doorCtx.arc(
    99,
    63,
    7,
    0,
    Math.PI*2
);

doorCtx.fill();


doorCtx.fillStyle =
    "#d0a34a";

doorCtx.beginPath();

doorCtx.arc(
    97,
    61,
    3,
    0,
    Math.PI*2
);

doorCtx.fill();


/* =====================================================
   맵
===================================================== */

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

const MAP_SIZE =
    initialMap.length;


/* =====================================================
   게임 상태
===================================================== */

let px = 9.5;
let py = 10.5;

let angle = 0;

let hp = 100;

let stamina = 100;

let flashlight = 18;

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


/* =====================================================
   귀신 초기화
===================================================== */

function createGhost() {

    return {

        x: 17.5,

        y: 16.5,

        hp: 100,

        stun: 0,

        pathTimer: 0,

        path: []

    };
}


/* =====================================================
   게임 초기화
===================================================== */

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

    flashlight = 18;

    gameOver = false;


    items = {

        potion: 0,

        battery: 0,

        talisman: 1,

        key: false,

        knife: false

    };


    ghost = createGhost();


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


/* =====================================================
   충돌
===================================================== */

function solid(x,y) {

    if(
        x < 0 ||
        y < 0 ||
        x >= MAP_SIZE ||
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


    return tile === 1 ||
           tile === 2;
}


/* =====================================================
   귀신용 통과 가능 타일
===================================================== */

function ghostWalkable(x,y) {

    if(
        x < 0 ||
        y < 0 ||
        x >= MAP_SIZE ||
        y >= MAP_SIZE
    ) {

        return false;
    }


    const tile =
        houseMap[y][x];


    /*
       귀신도 문을 벽으로 취급.
       즉 플레이어처럼 실제로 열린 문을
       지나가야 한다.
    */

    return tile === 0;
}


/* =====================================================
   BFS 경로 탐색
===================================================== */

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
        new Set();

    const parent =
        new Map();


    const startKey =
        startX + "," + startY;


    queue.push([
        startX,
        startY
    ]);

    visited.add(startKey);


    const dirs = [

        [1,0],

        [-1,0],

        [0,1],

        [0,-1]

    ];


    while(queue.length > 0) {

        const current =
            queue.shift();

        const cx = current[0];
        const cy = current[1];


        if(
            cx === targetX &&
            cy === targetY
        ) {

            break;
        }


        for(
            const dir of dirs
        ) {

            const nx =
                cx + dir[0];

            const ny =
                cy + dir[1];


            if(
                !ghostWalkable(
                    nx,
                    ny
                )
            ) {

                continue;
            }


            const key =
                nx + "," + ny;


            if(
                visited.has(key)
            ) {

                continue;
            }


            visited.add(key);

            parent.set(
                key,
                cx + "," + cy
            );

            queue.push([
                nx,
                ny
            ]);
        }
    }


    const targetKey =
        targetX + "," + targetY;


    if(
        !visited.has(targetKey)
    ) {

        return [];
    }


    const path = [];

    let current =
        targetKey;


    while(current !== startKey) {

        const parts =
            current.split(",");

        path.unshift([
            Number(parts[0]) + 0.5,
            Number(parts[1]) + 0.5
        ]);

        current =
            parent.get(current);

        if(!current) break;
    }


    return path;
}


/* =====================================================
   귀신 업데이트
===================================================== */

function updateGhost() {

    if(ghost.hp <= 0) return;


    if(ghost.stun > 0) {

        ghost.stun--;

        return;
    }


    /*
       일정 시간마다 경로를 다시 계산.
    */

    ghost.pathTimer--;


    if(
        ghost.pathTimer <= 0
    ) {

        ghost.path =
            findGhostPath();

        ghost.pathTimer = 20;
    }


    if(
        ghost.path.length === 0
    ) {

        return;
    }


    const target =
        ghost.path[0];


    const dx =
        target[0] - ghost.x;

    const dy =
        target[1] - ghost.y;


    const dist =
        Math.sqrt(
            dx*dx + dy*dy
        );


    if(dist < 0.08) {

        ghost.path.shift();

        return;
    }


    const speed = 0.018;


    const mx =
        dx / dist * speed;

    const my =
        dy / dist * speed;


    /*
       ★ 핵심 수정 ★

       귀신도 X/Y 각각 충돌 검사.

       벽에 막힌 상태에서는
       절대로 벽 내부로 이동하지 않는다.
    */

    if(
        !solid(
            ghost.x + mx,
            ghost.y
        )
    ) {

        ghost.x += mx;
    }


    if(
        !solid(
            ghost.x,
            ghost.y + my
        )
    ) {

        ghost.y += my;
    }


    /*
       플레이어와 접촉하면 공격.
    */

    const pdx =
        px - ghost.x;

    const pdy =
        py - ghost.y;

    const playerDist =
        Math.sqrt(
            pdx*pdx +
            pdy*pdy
        );


    if(
        playerDist < 0.7
    ) {

        hp -= 0.7;

        shake = 4;


        if(hp <= 0) {

            hp = 0;

            triggerGameOver();
        }
    }


    /*
       가까워지면 화면 글리치
    */

    if(
        playerDist < 6
    ) {

        document.getElementById(
            "glitch"
        ).style.opacity =
            (
                (6-playerDist)/6
            ) * 0.45;

    } else {

        document.getElementById(
            "glitch"
        ).style.opacity = 0;
    }
}


/* =====================================================
   키보드
===================================================== */

const keys = {};


function normalizeKey(k) {

    if(k === "ArrowLeft")
        return "left";

    if(k === "ArrowRight")
        return "right";


    k = k.toLowerCase();


    if(k === "ㅈ")
        return "w";

    if(k === "ㄴ")
        return "s";

    if(k === "ㅁ")
        return "a";

    if(k === "ㅇ")
        return "d";

    if(k === "ㄷ")
        return "e";

    if(k === "ㄱ")
        return "r";


    return k;
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


/* =====================================================
   아이템
===================================================== */

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


    hp =
        Math.min(
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


    flashlight = 25;


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


    if(ghost.hp <= 0)
        return;


    const dx =
        ghost.x - px;

    const dy =
        ghost.y - py;


    const dist =
        Math.sqrt(
            dx*dx +
            dy*dy
        );


    if(dist < 7) {

        ghost.stun = 240;

        const safeDist =
            Math.max(
                dist,
                0.01
            );


        ghost.x -=
            dx / safeDist * 2;


        ghost.y -=
            dy / safeDist * 2;


        /*
           부적 밀어내기 후에도
           벽 안으로 들어가지 않도록 보정.
        */

        if(
            solid(
                ghost.x,
                ghost.y
            )
        ) {

            ghost.x +=
                dx / safeDist * 2;

            ghost.y +=
                dy / safeDist * 2;
        }


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


/* =====================================================
   상호작용
===================================================== */

function interact() {

    if(gameOver)
        return;


    let tx =
        Math.floor(
            px +
            Math.cos(angle)*1.2
        );


    let ty =
        Math.floor(
            py +
            Math.sin(angle)*1.2
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


    for(
        let i =
            worldItems.length-1;
        i >= 0;
        i--
    ) {

        const item =
            worldItems[i];


        const dx =
            px - item.x;

        const dy =
            py - item.y;


        const dist =
            Math.sqrt(
                dx*dx +
                dy*dy
            );


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
                    "💊 회복약을 얻었습니다.",
                    "#ff6666"
                );
            }


            if(item.type === "battery") {

                items.battery++;


                showMessage(
                    "🔋 배터리를 얻었습니다.",
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


            worldItems.splice(
                i,
                1
            );


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


/* =====================================================
   마우스
===================================================== */

let mouseDown = false;

let lastMouseX = 0;


canvas.addEventListener(
    "mousedown",
    function(e) {

        initAudio();

        canvas.focus();

        mouseDown = true;

        lastMouseX =
            e.clientX;


        if(
            items.knife &&
            !gameOver
        ) {

            attackTimer = 10;

            sound("attack");

            attack();
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

        if(!mouseDown)
            return;


        const dx =
            e.clientX -
            lastMouseX;


        angle +=
            dx * 0.006;


        lastMouseX =
            e.clientX;
    }
);


/* =====================================================
   공격
===================================================== */

function attack() {

    if(ghost.hp <= 0)
        return;


    const dx =
        ghost.x - px;

    const dy =
        ghost.y - py;


    const dist =
        Math.sqrt(
            dx*dx +
            dy*dy
        );


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
        dist < 2.3 &&
        Math.abs(a) < 0.7
    ) {

        ghost.hp -= 50;

        ghost.stun = 60;

        shake = 8;

        sound("hit");


        if(
            ghost.hp <= 0
        ) {

            ghost.hp = 0;


            showMessage(
                "💀 귀신을 성불시켰습니다!",
                "#00ffff"
            );
        }
    }
}


/* =====================================================
   플레이어 이동
===================================================== */

function updatePlayer() {

    if(gameOver)
        return;


    if(keys["left"])
        angle -= 0.045;


    if(keys["right"])
        angle += 0.045;


    const running =
        keys["e"] &&
        stamina > 0;


    const speed =
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
                stamina + 0.3
            );
    }


    let dx = 0;
    let dy = 0;


    if(keys["w"]) {

        dx +=
            Math.cos(angle) *
            speed;

        dy +=
            Math.sin(angle) *
            speed;
    }


    if(keys["s"]) {

        dx -=
            Math.cos(angle) *
            speed;

        dy -=
            Math.sin(angle) *
            speed;
    }


    if(keys["a"]) {

        dx +=
            Math.cos(
                angle - Math.PI/2
            ) *
            speed;

        dy +=
            Math.sin(
                angle - Math.PI/2
            ) *
            speed;
    }


    if(keys["d"]) {

        dx +=
            Math.cos(
                angle + Math.PI/2
            ) *
            speed;

        dy +=
            Math.sin(
                angle + Math.PI/2
            ) *
            speed;
    }


    const margin = 0.22;


    if(
        !solid(
            px + dx +
            Math.sign(dx)*margin,
            py
        )
    ) {

        px += dx;
    }


    if(
        !solid(
            px,
            py + dy +
            Math.sign(dy)*margin
        )
    ) {

        py += dy;
    }
}


/* =====================================================
   업데이트
===================================================== */

function update() {

    if(gameOver)
        return;


    timer += 0.05;


    if(shake > 0)
        shake--;


    if(attackTimer > 0)
        attackTimer--;


    updatePlayer();

    updateGhost();


    updateUI();
}


/* =====================================================
   UI
===================================================== */

function updateUI() {

    const hpValue =
        Math.max(
            0,
            Math.min(
                100,
                hp
            )
        );


    const staminaValue =
        Math.max(
            0,
            Math.min(
                100,
                stamina
            )
        );


    document.getElementById(
        "hp"
    ).style.width =
        hpValue + "%";


    document.getElementById(
        "stamina"
    ).style.width =
        staminaValue + "%";


    document.getElementById(
        "hpText"
    ).innerText =
        Math.ceil(hpValue) +
        " / 100";


    document.getElementById(
        "staminaText"
    ).innerText =
        Math.ceil(staminaValue) +
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


/* =====================================================
   메시지
===================================================== */

function showMessage(
    text,
    color
) {

    const el =
        document.getElementById(
            "msg"
        );


    el.innerText =
        text;


    el.style.color =
        color ||
        "#ff3333";


    clearTimeout(
        window.msgTimer
    );


    window.msgTimer =
        setTimeout(
            function() {

                if(!gameOver)
                    el.innerText = "";

            },
            3000
        );
}


/* =====================================================
   귀신 그래픽
===================================================== */

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
        ? 0.4
        : 0.95;


    ctx.shadowColor =
        stunned
        ? "#00ffff"
        : "#ff0000";


    ctx.shadowBlur = 20;


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


/* =====================================================
   가구
===================================================== */

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


    } else if(type === "desk") {

        ctx.fillStyle =
            "#5a351d";

        ctx.fillRect(
            -size/1.2,
            -size/5,
            size*1.4,
            size/6
        );


    } else if(type === "chair") {

        ctx.fillStyle =
            "#58341d";

        ctx.fillRect(
            -size/4,
            -size/1.1,
            size/2,
            size/2
        );


    } else if(type === "table") {

        ctx.fillStyle =
            "#69401f";

        ctx.fillRect(
            -size/2,
            -size/8,
            size,
            size/7
        );


    } else if(type === "bed") {

        ctx.fillStyle =
            "#57321b";

        ctx.fillRect(
            -size/1.1,
            -size/4,
            size*1.4,
            size/2
        );

        ctx.fillStyle =
            "#b9b9b9";

        ctx.fillRect(
            -size,
            -size/3,
            size*1.2,
            size/4
        );


    } else if(type === "cabinet") {

        ctx.fillStyle =
            "#444";

        ctx.fillRect(
            -size/3,
            -size,
            size*0.7,
            size
        );


    } else if(type === "clock") {

        ctx.fillStyle =
            "#57351d";

        ctx.fillRect(
            -size/5,
            -size,
            size/2.5,
            size*1.2
        );


        ctx.fillStyle =
            "#fff";

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

        ctx.fillStyle =
            "#aaa";

        ctx.fillRect(
            -size/15,
            -size/2,
            size/7,
            size/2
        );


        ctx.fillStyle =
            "#ffb000";

        ctx.shadowColor =
            "#ff8800";

        ctx.shadowBlur = 20;


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


/* =====================================================
   아이템 그래픽
===================================================== */

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
            size/7;


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


    } else if(type === "knife") {

        ctx.fillStyle =
            "#ddd";


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

        ctx.shadowColor =
            "#ff0000";

        ctx.shadowBlur = 15;


        ctx.beginPath();

        ctx.arc(
            0,
            size/5,
            size/2.5,
            0,
            Math.PI*2
        );

        ctx.fill();


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
            "#ff7700";

        ctx.fillRect(
            -size/3,
            0,
            size/1.5,
            size/2
        );
    }


    ctx.restore();
}


/* =====================================================
   3D 렌더링
===================================================== */

function render() {

    ctx.save();


    if(shake > 0) {

        ctx.translate(
            (Math.random()-0.5)*shake,
            (Math.random()-0.5)*shake
        );
    }


    /*
       ★ 밝아진 천장
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
        "#161616"
    );


    ceiling.addColorStop(
        1,
        "#513b3b"
    );


    ctx.fillStyle =
        ceiling;


    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height/2
    );


    /*
       ★ 밝아진 바닥
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
        "#513737"
    );


    floor.addColorStop(
        1,
        "#121212"
    );


    ctx.fillStyle =
        floor;


    ctx.fillRect(
        0,
        canvas.height/2,
        canvas.width,
        canvas.height/2
    );


    const rays = 220;

    const fov =
        Math.PI * 0.43;


    const proj =
        (canvas.width/2) /
        Math.tan(
            fov/2
        );


    const zBuffer =
        new Array(rays)
        .fill(999);


    /*
       ★ 손전등 거리 증가
    */

    const range =
        flashlight +
        2;


    const column =
        canvas.width /
        rays;


    /* =================================================
       벽
    ================================================= */

    for(
        let i = 0;
        i < rays;
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

                hitType = 1;

                break;
            }


            if(
                houseMap[ty][tx] > 0
            ) {

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


        zBuffer[i] =
            corrected;


        const height =
            Math.min(
                canvas.height,
                proj /
                (corrected+0.0001)
            );


        /*
           ★ 기존보다 훨씬 밝게
        */

        const brightness =
            Math.max(
                0.38,
                1 -
                corrected /
                (range * 1.15)
            );


        if(
            hitType === 2
        ) {

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


        /*
           ★ 어두움 감소
        */

        ctx.fillStyle =
            `rgba(
                0,
                0,
                0,
                ${Math.max(
                    0,
                    1-brightness
                ) * 0.65}
            )`;


        ctx.fillRect(
            i*column,
            (canvas.height-height)/2,
            column+1,
            height
        );
    }


    /* =================================================
       오브젝트
    ================================================= */

    const objects = [];


    furniture.forEach(
        f => {

            const dx =
                f.x-px;

            const dy =
                f.y-py;


            const dist =
                Math.sqrt(
                    dx*dx +
                    dy*dy
                );


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


    worldItems.forEach(
        item => {

            const dx =
                item.x-px;

            const dy =
                item.y-py;


            const dist =
                Math.sqrt(
                    dx*dx +
                    dy*dy
                );


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
                Math.abs(a) <
                fov/1.8 &&
                dist < range
            ) {

                objects.push({

                    type:
                        "item",

                    data: item,

                    dist: dist,

                    angle: a
                });
            }
        }
    );


    if(
        ghost.hp > 0
    ) {

        const dx =
            ghost.x-px;

        const dy =
            ghost.y-py;


        const dist =
            Math.sqrt(
                dx*dx +
                dy*dy
            );


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
            Math.abs(a) <
            fov/1.8 &&
            dist < range
        ) {

            objects.push({

                type:
                    "ghost",

                data:
                    ghost,

                dist:
                    dist,

                angle:
                    a
            });
        }
    }


    objects.sort(
        (a,b) =>
            b.dist-a.dist
    );


    objects.forEach(
        obj => {

            const sx =
                canvas.width/2 +
                Math.tan(
                    obj.angle
                ) * proj;


            const ray =
                Math.floor(
                    (
                        sx /
                        canvas.width
                    ) * rays
                );


            if(
                ray < 0 ||
                ray >= rays
            )
                return;


            if(
                obj.dist >
                zBuffer[ray]
            )
                return;


            if(
                obj.type ===
                "furniture"
            ) {

                const size =
                    Math.min(
                        170,
                        proj *
                        0.55 /
                        obj.dist
                    );


                drawFurniture(
                    obj.data.type,
                    sx,
                    canvas.height/2 +
                    size/3,
                    size
                );
            }


            if(
                obj.type === "item"
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
                    ) * 4;


                drawItem(
                    obj.data.type,
                    sx,
                    canvas.height/2 +
                    size/3 +
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


                ctx.shadowBlur =
                    5;


                ctx.fillText(
                    obj.data.name +
                    " [R]",
                    sx,
                    canvas.height/2 -
                    size/1.1
                );


                ctx.restore();
            }


            if(
                obj.type === "ghost"
            ) {

                const size =
                    Math.min(
                        220,
                        proj *
                        0.7 /
                        obj.dist
                    );


                drawGhost(
                    sx,
                    canvas.height/2 +
                    size/4,
                    size,
                    obj.data.stun > 0
                );
            }

        }
    );


    /*
       손에 든 칼
    */

    if(items.knife) {

        ctx.save();


        const swing =
            attackTimer > 0
            ? (10-attackTimer)*10
            : 0;


        ctx.translate(
            canvas.width -
            120 -
            swing,

            canvas.height -
            80 +
            swing
        );


        ctx.rotate(-0.6);


        ctx.fillStyle =
            "#ccc";


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


    ctx.restore();


    drawMinimap();
}


/* =====================================================
   미니맵
===================================================== */

function drawMinimap() {

    const mw = 190;

    const mh = 170;


    mapCtx.fillStyle =
        "#050505";


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
                    "#3f3f3f";

            } else if(tile === 2) {

                mapCtx.fillStyle =
                    "#9b672c";

            } else {

                mapCtx.fillStyle =
                    "#151515";
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
       아이템
    */

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


    /*
       귀신
    */

    if(
        ghost.hp > 0
    ) {

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


    /*
       플레이어
    */

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


    /*
       방향
    */

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
            px +
            Math.cos(angle)*1.2
        ) * cell,

        (
            py +
            Math.sin(angle)*1.2
        ) * cell
    );


    mapCtx.stroke();
}


/* =====================================================
   게임오버
===================================================== */

function triggerGameOver() {

    gameOver = true;

    sound("scare");


    document.getElementById(
        "gameover"
    ).style.display =
        "flex";
}


function resetGame() {

    initGame();
}


/* =====================================================
   게임 루프
===================================================== */

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
    height=640,
    scrolling=False
)
```
