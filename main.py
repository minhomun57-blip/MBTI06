import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
page_title="🏚️ 저주받은 저택",
layout="wide",
initial_sidebar_state="collapsed"
)

st.title("🏚️ 저주받은 저택")
st.caption(
"W/A/S/D: 이동 | ←/→: 회전 | E: 달리기 | R: 문 열기/아이템 획득 | "
"1: 회복약 | 2: 배터리 | 3: 퇴마부적 | 클릭: 공격"
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
    overflow: hidden;
    background: #000;
    font-family: "Courier New", monospace;
    user-select: none;
}

#game-wrap {
    position: relative;
    width: 100%;
    height: 600px;
    overflow: hidden;
    background: #000;
}

#canvas {
    width: 100%;
    height: 600px;
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
    z-index: 10;
    color: #ddd;
    text-shadow: 2px 2px 5px #000;
    font-size: 13px;
    pointer-events: none;
}

.bar-container {
    width: 210px;
    height: 11px;
    background: rgba(0,0,0,.85);
    border: 1px solid #555;
    margin-top: 3px;
}

.bar-fill {
    width: 100%;
    height: 100%;
    transition: width .08s linear;
}

#hp-bar {
    background: linear-gradient(90deg,#500,#f00);
}

#stamina-bar {
    background: linear-gradient(90deg,#063,#00ff55);
}

#weapon {
    color: #ffcc00;
    font-weight: bold;
}

#room-info {
    position: absolute;
    top: 15px;
    right: 235px;
    z-index: 10;
    color: #ccc;
    text-align: right;
    font-size: 12px;
    pointer-events: none;
}

#current-room-name {
    color: #ff4444;
    font-weight: bold;
}

#map-container {
    position: absolute;
    top: 12px;
    right: 12px;
    width: 190px;
    height: 190px;
    z-index: 20;
    background: rgba(0,0,0,.82);
    border: 2px solid #513b32;
    box-shadow: 0 0 12px #000;
}

#map-title {
    height: 20px;
    line-height: 20px;
    text-align: center;
    color: #d8b27a;
    font-size: 11px;
    background: #160e0a;
    border-bottom: 1px solid #49352b;
}

#minimap {
    width: 190px;
    height: 170px;
    display: block;
}

#inventory {
    position: absolute;
    right: 15px;
    bottom: 15px;
    z-index: 10;
    display: flex;
    gap: 7px;
    pointer-events: none;
}

.slot {
    width: 62px;
    height: 62px;
    background: rgba(5,5,5,.9);
    border: 1px solid #444;
    color: #aaa;
    text-align: center;
    font-size: 9px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.slot-key {
    color: #ffaa00;
    font-weight: bold;
    margin-bottom: 3px;
}

#msg {
    position: absolute;
    left: 50%;
    top: 30%;
    transform: translate(-50%,-50%);
    color: #ff3333;
    font-size: 19px;
    font-weight: bold;
    text-align: center;
    text-shadow: 0 0 10px #000;
    z-index: 30;
    pointer-events: none;
    white-space: nowrap;
}

#crosshair {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 12px;
    height: 12px;
    transform: translate(-50%,-50%);
    z-index: 8;
    pointer-events: none;
}

#crosshair:before,
#crosshair:after {
    content: "";
    position: absolute;
    background: rgba(255,255,255,.75);
}

#crosshair:before {
    width: 12px;
    height: 1px;
    top: 5px;
    left: 0;
}

#crosshair:after {
    width: 1px;
    height: 12px;
    left: 5px;
    top: 0;
}

#glitch-overlay {
    position: absolute;
    inset: 0;
    z-index: 7;
    pointer-events: none;
    opacity: 0;
    background:
        repeating-linear-gradient(
            0deg,
            rgba(255,0,0,.16),
            rgba(255,0,0,.16) 2px,
            transparent 2px,
            transparent 5px
        );
}

#jumpscare {
    display: none;
    position: absolute;
    inset: 0;
    z-index: 100;
    background: #050000;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    animation: redflash .08s infinite alternate;
}

@keyframes redflash {
    from { background:#000; }
    to { background:#250000; }
}

#scare-face {
    width: 310px;
    height: 370px;
    position: relative;
    border-radius: 48% 48% 45% 45%;
    background:
        radial-gradient(circle,#900 0%,#300 48%,#000 100%);
    box-shadow: 0 0 130px #f00;
    animation: shake .02s infinite alternate;
}

@keyframes shake {
    from { transform:translate(8px,-7px) scale(1.08); }
    to { transform:translate(-8px,7px) scale(1.18); }
}

.eye {
    position: absolute;
    top: 24%;
    width: 60px;
    height: 78px;
    border-radius: 50%;
    background: white;
    box-shadow: inset 0 0 25px red,0 0 20px red;
}

.eye.left {
    left: 18%;
    transform: rotate(-12deg);
}

.eye.right {
    right: 18%;
    transform: rotate(12deg);
}

.pupil {
    width: 13px;
    height: 13px;
    border-radius: 50%;
    background: #000;
    position: absolute;
    left: 38%;
    top: 34%;
}

.mouth {
    position: absolute;
    left: 10%;
    bottom: 8%;
    width: 80%;
    height: 140px;
    background: #000;
    border: 4px solid #a00;
    border-radius: 10px 10px 65px 65px;
    overflow: hidden;
}

.teeth {
    height: 35px;
    background:
        repeating-linear-gradient(
            90deg,
            #eee,
            #eee 14px,
            #300 14px,
            #300 20px
        );
}

#scare-text {
    color: #f00;
    font-size: 25px;
    font-weight: bold;
    margin-top: 25px;
    text-shadow: 0 0 20px red;
}

#restart-btn {
    margin-top: 20px;
    padding: 11px 28px;
    background: #080808;
    color: #f33;
    border: 1px solid red;
    cursor: pointer;
}
</style>

</head>

<body>

<div id="game-wrap">

<canvas id="canvas" tabindex="0"></canvas>

<div id="glitch-overlay"></div>

<div id="crosshair"></div>

<div id="ui">

```
<div>
    생명력
    <div class="bar-container">
        <div id="hp-bar" class="bar-fill"></div>
    </div>
</div>

<div style="margin-top:8px;">
    스테미나
    <div class="bar-container">
        <div id="stamina-bar" class="bar-fill"></div>
    </div>
</div>

<div style="margin-top:8px;">
    무기:
    <span id="weapon">맨손</span>
</div>
```

</div>

<div id="room-info">
    <div id="current-room-name">현재 위치: 중앙 홀</div>
    <div>마우스를 드래그하면 시점이 회전합니다</div>
</div>

<div id="map-container">
    <div id="map-title">🗺️ 저택 지도</div>
    <canvas id="minimap" width="190" height="170"></canvas>
</div>

<div id="inventory">

```
<div class="slot">
    <span class="slot-key">[1]</span>
    회복약
    <span id="cnt-potion">0</span>
</div>

<div class="slot">
    <span class="slot-key">[2]</span>
    배터리
    <span id="cnt-battery">0</span>
</div>

<div class="slot">
    <span class="slot-key">[3]</span>
    퇴마부적
    <span id="cnt-talisman">1</span>
</div>

<div class="slot">
    <span class="slot-key">[4]</span>
    탈출열쇠
    <span id="cnt-key">미획득</span>
</div>
```

</div>

<div id="msg">
    중앙 홀에서 시작합니다. 지도에서 방 위치를 확인하세요.
</div>

<div id="jumpscare">

```
<div id="scare-face">

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

<div id="scare-text">
    당신의 영혼은 이제 저택의 일부입니다...
</div>

<button id="restart-btn" onclick="resetGame()">
    다시 도전하기
</button>
```

</div>

</div>

<script>

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const miniCanvas = document.getElementById("minimap");
const miniCtx = miniCanvas.getContext("2d");

canvas.width = 900;
canvas.height = 600;

let audioCtx = null;

function initAudio() {
    if (!audioCtx) {
        const AC = window.AudioContext || window.webkitAudioContext;
        if (AC) audioCtx = new AC();
    }
}

function sound(type) {

    if (!audioCtx) return;

    const now = audioCtx.currentTime;

    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    if (type === "door") {
        osc.type = "triangle";
        osc.frequency.setValueAtTime(130, now);
        osc.frequency.exponentialRampToValueAtTime(55, now + .3);
        gain.gain.setValueAtTime(.35, now);
        gain.gain.exponentialRampToValueAtTime(.01, now + .3);
    }

    if (type === "item") {
        osc.type = "sine";
        osc.frequency.setValueAtTime(500, now);
        osc.frequency.exponentialRampToValueAtTime(1000, now + .2);
        gain.gain.setValueAtTime(.25, now);
        gain.gain.exponentialRampToValueAtTime(.01, now + .2);
    }

    if (type === "attack") {
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.exponentialRampToValueAtTime(35, now + .15);
        gain.gain.setValueAtTime(.4, now);
        gain.gain.exponentialRampToValueAtTime(.01, now + .15);
    }

    if (type === "hit") {
        osc.type = "square";
        osc.frequency.setValueAtTime(90, now);
        osc.frequency.exponentialRampToValueAtTime(20, now + .2);
        gain.gain.setValueAtTime(.45, now);
        gain.gain.exponentialRampToValueAtTime(.01, now + .2);
    }

    if (type === "scare") {
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.linearRampToValueAtTime(1000, now + .1);
        osc.frequency.linearRampToValueAtTime(50, now + 1);
        gain.gain.setValueAtTime(.9, now);
        gain.gain.exponentialRampToValueAtTime(.01, now + 1);
    }

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start(now);
    osc.stop(now + 1.1);
}


/*
    0 = 빈 공간
    1 = 일반 벽
    2 = 문
    3 = 탈출문
*/

const initialMap = [

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
[1,0,0,0,1,0,0,0,2,0,0,0,1,0,0,0,1],
[1,0,0,0,2,0,0,0,1,0,0,0,2,0,0,0,1],
[1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1],

[1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
[1,0,1,1,1,2,1,0,1,1,1,0,1,0,1,0,1],
[1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1],
[1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1],
[1,0,2,0,1,0,0,0,1,0,0,0,2,0,0,0,1],

[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],

[1,0,2,0,1,0,0,0,1,0,0,0,2,0,0,0,1],
[1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1],
[1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1],
[1,0,1,1,1,2,1,0,1,1,1,0,1,0,1,0,1],

[1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
[1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1],
[1,0,0,0,2,0,0,0,1,0,0,0,2,0,0,3,1],
[1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

];

let map = [];
let MAP_SIZE = 19;

let px = 9.5;
let py = 9.5;
let angle = 0;

let hp = 100;
let stamina = 100;

let flashRange = 14;

let gameOver = false;
let attackTimer = 0;
let shake = 0;
let anim = 0;

let items = {
    potion: 0,
    battery: 0,
    talisman: 1,
    key: false,
    knife: false
};


/*
    귀신은 딱 한 마리
*/
let ghosts = [];


/*
    방 안의 가구
*/
let furniture = [];


/*
    아이템
*/
let worldItems = [];


function initGame() {

    map = JSON.parse(JSON.stringify(initialMap));

    /*
        시작 위치는 중앙의 확실한 빈 공간
    */
    px = 8.5;
    py = 10.5;
    angle = 0;

    hp = 100;
    stamina = 100;
    flashRange = 14;

    gameOver = false;
    attackTimer = 0;
    shake = 0;

    items = {
        potion: 0,
        battery: 0,
        talisman: 1,
        key: false,
        knife: false
    };


    /*
        귀신 한 마리만 배치
        시작 위치에서 상당히 멀리 떨어뜨림
    */
    ghosts = [
        {
            x: 15.5,
            y: 17.5,
            hp: 100,
            stun: 0
        }
    ];


    /*
        아이템 배치
    */
    worldItems = [

        {
            x: 2.5,
            y: 2.5,
            type: "knife",
            name: "녹슨 단검"
        },

        {
            x: 14.5,
            y: 2.5,
            type: "potion",
            name: "낡은 회복약"
        },

        {
            x: 2.5,
            y: 8.5,
            type: "battery",
            name: "고전압 배터리"
        },

        {
            x: 14.5,
            y: 8.5,
            type: "potion",
            name: "응급 회복약"
        },

        {
            x: 2.5,
            y: 16.5,
            type: "battery",
            name: "오래된 배터리"
        },

        {
            x: 14.5,
            y: 17.5,
            type: "key",
            name: "피묻은 열쇠"
        }

    ];


    /*
        가구를 많이 배치
    */
    furniture = [

        // 북서쪽 서재
        {x:1.5,y:1.8,type:"bookshelf"},
        {x:3.2,y:1.5,type:"bookshelf"},
        {x:1.6,y:3.1,type:"desk"},
        {x:3.2,y:3.2,type:"chair"},

        // 북동쪽 방
        {x:13.8,y:1.7,type:"bed"},
        {x:15.2,y:3.1,type:"cabinet"},
        {x:13.8,y:3.1,type:"chair"},
        {x:15.2,y:1.6,type:"bookshelf"},

        // 중앙
        {x:7.2,y:9.1,type:"clock"},
        {x:10.8,y:9.1,type:"clock"},
        {x:7.2,y:11.8,type:"chair"},
        {x:10.8,y:11.8,type:"chair"},
        {x:8.2,y:7.7,type:"candle"},
        {x:9.8,y:13.2,type:"candle"},

        // 남서쪽
        {x:1.6,y:13.7,type:"bed"},
        {x:3.2,y:15.1,type:"cabinet"},
        {x:1.6,y:15.5,type:"chair"},
        {x:3.2,y:13.5,type:"bookshelf"},

        // 남동쪽
        {x:13.8,y:13.7,type:"bookshelf"},
        {x:15.2,y:13.7,type:"desk"},
        {x:13.8,y:15.4,type:"chair"},
        {x:15.2,y:15.4,type:"cabinet"},
        {x:13.8,y:17.8,type:"table"},
        {x:15.2,y:17.8,type:"chair"}

    ];


    document.getElementById("jumpscare").style.display = "none";

    document.getElementById("msg").innerText =
        "중앙 홀에서 시작했습니다. 지도에서 방을 확인하세요.";

    updateUI();
}


function resetGame() {
    initGame();
}


const keys = {};


function parseKey(k) {

    if (k === "ArrowLeft") return "left";
    if (k === "ArrowRight") return "right";

    k = k.toLowerCase();

    // 한글 자판 대응
    if (k === "ㅈ") return "w";
    if (k === "ㄴ") return "s";
    if (k === "ㅁ") return "a";
    if (k === "ㅇ") return "d";
    if (k === "ㄷ") return "e";
    if (k === "ㄱ") return "r";

    return k;
}


window.addEventListener("keydown", function(e) {

    const k = parseKey(e.key);

    keys[k] = true;

    if (
        ["ArrowUp","ArrowDown","ArrowLeft",
         "ArrowRight"," "].includes(e.key)
    ) {
        e.preventDefault();
    }

    if (gameOver) return;

    if (k === "r") {
        interact();
    }

    if (e.key === "1" && items.potion > 0) {

        hp = Math.min(100, hp + 60);
        items.potion--;

        sound("item");

        showMessage("💊 체력을 회복했습니다.");

        updateUI();
    }

    if (e.key === "2" && items.battery > 0) {

        flashRange += 4;
        items.battery--;

        sound("item");

        showMessage("🔋 손전등이 밝아졌습니다.");

        updateUI();
    }

    if (e.key === "3" && items.talisman > 0) {

        items.talisman--;

        ghosts.forEach(g => {

            g.stun = 240;

            const dx = g.x - px;
            const dy = g.y - py;

            const d = Math.sqrt(dx*dx + dy*dy) || 1;

            g.x += dx / d * 1.2;
            g.y += dy / d * 1.2;

        });

        shake = 10;

        sound("item");

        showMessage("📜 퇴마부적으로 원혼을 밀어냈습니다.");

        updateUI();
    }

});


window.addEventListener("keyup", function(e) {

    keys[parseKey(e.key)] = false;

});


let mouseDown = false;
let lastMouseX = 0;


canvas.addEventListener("mousedown", function(e) {

    initAudio();

    canvas.focus();

    mouseDown = true;

    lastMouseX = e.clientX;

    if (
        items.knife &&
        attackTimer === 0 &&
        !gameOver
    ) {

        attackTimer = 12;

        sound("attack");

        checkAttack();

    }

});


window.addEventListener("mouseup", function() {
    mouseDown = false;
});


window.addEventListener("mousemove", function(e) {

    if (!mouseDown) return;

    const dx = e.clientX - lastMouseX;

    angle += dx * .006;

    lastMouseX = e.clientX;

});


function showMessage(text) {

    const msg = document.getElementById("msg");

    msg.innerText = text;

    setTimeout(function() {

        if (!gameOver && msg.innerText === text) {
            msg.innerText = "";
        }

    }, 2500);

}


function interact() {

    if (gameOver) return;

    const tx = Math.floor(
        px + Math.cos(angle) * 1.25
    );

    const ty = Math.floor(
        py + Math.sin(angle) * 1.25
    );

    if (
        tx >= 0 &&
        tx < MAP_SIZE &&
        ty >= 0 &&
        ty < MAP_SIZE
    ) {

        const tile = map[ty][tx];

        if (tile === 2) {

            map[ty][tx] = 0;

            sound("door");

            showMessage("🚪 낡은 문을 열었습니다.");

            return;
        }

        if (tile === 3) {

            if (items.key) {

                gameOver = true;

                sound("door");

                const msg =
                    document.getElementById("msg");

                msg.innerText =
                    "🚪 탈출 성공! 저택에서 빠져나왔습니다.";

                msg.style.color = "gold";

            } else {

                showMessage(
                    "🔒 문이 잠겨 있습니다. 피묻은 열쇠가 필요합니다."
                );

            }

            return;
        }
    }


    for (let i = worldItems.length - 1; i >= 0; i--) {

        const item = worldItems[i];

        const dx = px - item.x;
        const dy = py - item.y;

        const dist = Math.sqrt(dx*dx + dy*dy);

        if (dist < 1.35) {

            if (item.type === "knife") {
                items.knife = true;
                showMessage("🗡️ 녹슨 단검을 얻었습니다.");
            }

            if (item.type === "potion") {
                items.potion++;
                showMessage("💊 회복약을 얻었습니다.");
            }

            if (item.type === "battery") {
                items.battery++;
                showMessage("🔋 배터리를 얻었습니다.");
            }

            if (item.type === "key") {
                items.key = true;
                showMessage(
                    "🔑 피묻은 열쇠 획득! 황금색 탈출문을 찾으세요."
                );
            }

            worldItems.splice(i,1);

            sound("item");

            updateUI();

            return;
        }
    }

    showMessage("상호작용할 대상이 없습니다.");

}


function isSolid(x,y) {

    if (
        x < 0 ||
        x >= MAP_SIZE ||
        y < 0 ||
        y >= MAP_SIZE
    ) {
        return true;
    }

    const tile =
        map[Math.floor(y)][Math.floor(x)];

    return tile === 1 || tile === 2;
}


function checkAttack() {

    ghosts.forEach(g => {

        if (g.hp <= 0) return;

        const dx = g.x - px;
        const dy = g.y - py;

        const dist =
            Math.sqrt(dx*dx + dy*dy);

        let diff =
            Math.atan2(dy,dx) - angle;

        while (diff < -Math.PI)
            diff += Math.PI*2;

        while (diff > Math.PI)
            diff -= Math.PI*2;

        if (
            dist < 2.2 &&
            Math.abs(diff) < .75
        ) {

            g.hp -= 50;

            g.stun = 70;

            shake = 7;

            sound("hit");

            if (g.hp <= 0) {

                showMessage(
                    "💀 원혼을 성불시켰습니다!"
                );

            } else {

                showMessage(
                    "⚔️ 귀신에게 공격이 적중했습니다!"
                );

            }
        }

    });

}


function triggerJumpscare() {

    gameOver = true;

    sound("scare");

    document.getElementById(
        "jumpscare"
    ).style.display = "flex";

}


function updateUI() {

    document.getElementById(
        "hp-bar"
    ).style.width = Math.max(0,hp) + "%";

    document.getElementById(
        "stamina-bar"
    ).style.width = Math.max(0,stamina) + "%";

    document.getElementById(
        "weapon"
    ).innerText =
        items.knife
        ? "녹슨 단검"
        : "맨손";

    document.getElementById(
        "cnt-potion"
    ).innerText = items.potion;

    document.getElementById(
        "cnt-battery"
    ).innerText = items.battery;

    document.getElementById(
        "cnt-talisman"
    ).innerText = items.talisman;

    document.getElementById(
        "cnt-key"
    ).innerText =
        items.key
        ? "획득완료"
        : "미획득";

}


function getRoomName() {

    const x = Math.floor(px);
    const y = Math.floor(py);

    if (x < 5 && y < 5)
        return "북서쪽 서재";

    if (x > 12 && y < 5)
        return "북동쪽 침실";

    if (x < 5 && y > 12)
        return "남서쪽 침실";

    if (x > 12 && y > 12)
        return "남동쪽 비밀실";

    return "중앙 홀";
}


function updateRoomName() {

    document.getElementById(
        "current-room-name"
    ).innerText =
        "현재 위치: " + getRoomName();

}


function drawMap() {

    const w = miniCanvas.width;
    const h = miniCanvas.height;

    miniCtx.fillStyle = "#080706";
    miniCtx.fillRect(0,0,w,h);

    const cell =
        Math.min(
            (w-10)/MAP_SIZE,
            (h-10)/MAP_SIZE
        );

    const ox =
        (w - cell*MAP_SIZE)/2;

    const oy =
        (h - cell*MAP_SIZE)/2;


    for (let y=0;y<MAP_SIZE;y++) {

        for (let x=0;x<MAP_SIZE;x++) {

            const tile = map[y][x];

            if (tile === 1) {

                miniCtx.fillStyle = "#392923";

            } else if (tile === 2) {

                miniCtx.fillStyle = "#8a5a2b";

            } else if (tile === 3) {

                miniCtx.fillStyle = "#ffd23c";

            } else {

                miniCtx.fillStyle = "#151515";

            }

            miniCtx.fillRect(
                ox+x*cell,
                oy+y*cell,
                cell+.5,
                cell+.5
            );

        }

    }


    /*
        아이템 표시
    */
    worldItems.forEach(item => {

        let color = "#fff";

        if (item.type === "key")
            color = "#ffd700";

        if (item.type === "knife")
            color = "#ddd";

        if (item.type === "potion")
            color = "#ff3355";

        if (item.type === "battery")
            color = "#ff8c00";

        miniCtx.fillStyle = color;

        miniCtx.fillRect(
            ox + item.x*cell - 1.5,
            oy + item.y*cell - 1.5,
            3,
            3
        );

    });


    /*
        귀신 표시
    */
    ghosts.forEach(g => {

        if (g.hp <= 0) return;

        miniCtx.fillStyle = "#ff2222";

        miniCtx.beginPath();

        miniCtx.arc(
            ox+g.x*cell,
            oy+g.y*cell,
            3,
            0,
            Math.PI*2
        );

        miniCtx.fill();

    });


    /*
        플레이어 표시
    */
    miniCtx.fillStyle = "#00ff66";

    miniCtx.beginPath();

    miniCtx.arc(
        ox+px*cell,
        oy+py*cell,
        3.5,
        0,
        Math.PI*2
    );

    miniCtx.fill();


    /*
        플레이어 방향
    */
    miniCtx.strokeStyle = "#00ff66";
    miniCtx.lineWidth = 1.5;

    miniCtx.beginPath();

    miniCtx.moveTo(
        ox+px*cell,
        oy+py*cell
    );

    miniCtx.lineTo(
        ox+(px+Math.cos(angle)*1.3)*cell,
        oy+(py+Math.sin(angle)*1.3)*cell
    );

    miniCtx.stroke();

}


function drawDoorTexture(x,y,w,h) {

    /*
        기존의 이상하게 넓은 문 대신
        중앙에 좁은 낡은 나무문을 그린다.
    */

    ctx.fillStyle = "#130b07";
    ctx.fillRect(x,y,w,h);

    const doorW = w * .52;
    const doorX = x + (w-doorW)/2;

    const gradient =
        ctx.createLinearGradient(
            doorX,0,
            doorX+doorW,0
        );

    gradient.addColorStop(0,"#1b0b05");
    gradient.addColorStop(.5,"#5a3218");
    gradient.addColorStop(1,"#241006");

    ctx.fillStyle = gradient;

    ctx.fillRect(
        doorX,
        y,
        doorW,
        h
    );

    /*
        오래된 나무 판자
    */
    ctx.strokeStyle = "rgba(15,5,2,.8)";
    ctx.lineWidth = Math.max(1,w*.025);

    for (
        let i=1;
        i<7;
        i++
    ) {

        const yy =
            y + h*i/7;

        ctx.beginPath();

        ctx.moveTo(
            doorX,
            yy
        );

        ctx.lineTo(
            doorX+doorW,
            yy
        );

        ctx.stroke();

    }

    /*
        문틀
    */
    ctx.strokeStyle = "#100805";
    ctx.lineWidth = Math.max(2,w*.08);

    ctx.strokeRect(
        doorX,
        y,
        doorW,
        h
    );

    /*
        금속 경첩
    */
    ctx.fillStyle = "#403a30";

    ctx.fillRect(
        doorX+doorW*.08,
        y+h*.25,
        Math.max(2,w*.035),
        h*.1
    );

    ctx.fillRect(
        doorX+doorW*.08,
        y+h*.68,
        Math.max(2,w*.035),
        h*.1
    );

    /*
        낡은 손잡이
    */
    ctx.fillStyle = "#806a38";

    ctx.beginPath();

    ctx.arc(
        doorX+doorW*.78,
        y+h*.53,
        Math.max(2,w*.035),
        0,
        Math.PI*2
    );

    ctx.fill();

}


function drawFurniture(type,sx,sy,size) {

    ctx.save();

    ctx.translate(sx,sy);

    if (type === "bookshelf") {

        ctx.fillStyle="#351b0c";
        ctx.fillRect(
            -size*.45,
            -size,
            size*.9,
            size
        );

        ctx.fillStyle="#160b06";

        ctx.fillRect(
            -size*.38,
            -size*.9,
            size*.76,
            size*.8
        );

        ctx.fillStyle="#7a4320";

        for(let i=0;i<4;i++) {

            ctx.fillRect(
                -size*.4,
                -size*.8+i*size*.2,
                size*.8,
                size*.04
            );

        }

        ctx.fillStyle="#a23a2e";
        ctx.fillRect(
            -size*.3,
            -size*.78,
            size*.08,
            size*.17
        );

        ctx.fillStyle="#2d6a78";
        ctx.fillRect(
            -size*.1,
            -size*.77,
            size*.07,
            size*.18
        );

        ctx.fillStyle="#b58b35";
        ctx.fillRect(
            size*.1,
            -size*.58,
            size*.08,
            size*.18
        );

    }

    else if (type === "desk") {

        ctx.fillStyle="#452613";

        ctx.fillRect(
            -size*.65,
            -size*.22,
            size*1.3,
            size*.18
        );

        ctx.fillStyle="#291408";

        ctx.fillRect(
            -size*.55,
            -size*.05,
            size*.12,
            size*.7
        );

        ctx.fillRect(
            size*.43,
            -size*.05,
            size*.12,
            size*.7
        );

    }

    else if (type === "chair") {

        ctx.fillStyle="#40210f";

        ctx.fillRect(
            -size*.25,
            -size*.55,
            size*.5,
            size*.4
        );

        ctx.fillStyle="#5a3017";

        ctx.fillRect(
            -size*.38,
            -size*.18,
            size*.76,
            size*.12
        );

        ctx.fillStyle="#251107";

        ctx.fillRect(
            -size*.3,
            -size*.05,
            size*.08,
            size*.5
        );

        ctx.fillRect(
            size*.22,
            -size*.05,
            size*.08,
            size*.5
        );

    }

    else if (type === "bed") {

        ctx.fillStyle="#4b2a17";

        ctx.fillRect(
            -size*.7,
            -size*.2,
            size*1.4,
            size*.45
        );

        ctx.fillStyle="#777";

        ctx.fillRect(
            -size*.6,
            -size*.13,
            size*1.2,
            size*.28
        );

        ctx.fillStyle="#ddd";

        ctx.fillRect(
            -size*.55,
            -size*.1,
            size*.35,
            size*.22
        );

        ctx.fillStyle="#30170b";

        ctx.fillRect(
            -size*.72,
            -size*.28,
            size*1.44,
            size*.08
        );

    }

    else if (type === "cabinet") {

        ctx.fillStyle="#30343a";

        ctx.fillRect(
            -size*.35,
            -size*.85,
            size*.7,
            size*.85
        );

        ctx.strokeStyle="#111";

        ctx.strokeRect(
            -size*.35,
            -size*.85,
            size*.7,
            size*.85
        );

        ctx.fillStyle="#aaa";

        ctx.fillRect(
            -size*.05,
            -size*.62,
            size*.1,
            size*.05
        );

        ctx.fillRect(
            -size*.05,
            -size*.25,
            size*.1,
            size*.05
        );

    }

    else if (type === "clock") {

        ctx.fillStyle="#3a210f";

        ctx.fillRect(
            -size*.22,
            -size,
            size*.44,
            size*1.1
        );

        ctx.fillStyle="#e5d1a0";

        ctx.beginPath();

        ctx.arc(
            0,
            -size*.75,
            size*.17,
            0,
            Math.PI*2
        );

        ctx.fill();

        ctx.strokeStyle="#111";

        ctx.beginPath();

        ctx.moveTo(0,-size*.75);
        ctx.lineTo(0,-size*.88);

        ctx.moveTo(0,-size*.75);
        ctx.lineTo(size*.1,-size*.7);

        ctx.stroke();

    }

    else if (type === "candle") {

        ctx.fillStyle="#777";

        ctx.fillRect(
            -size*.06,
            -size*.4,
            size*.12,
            size*.45
        );

        ctx.fillStyle="#ffb300";

        ctx.beginPath();

        ctx.arc(
            0,
            -size*.48,
            size*.11,
            0,
            Math.PI*2
        );

        ctx.fill();

        ctx.fillStyle="#fff38a";

        ctx.beginPath();

        ctx.arc(
            0,
            -size*.53,
            size*.05,
            0,
            Math.PI*2
        );

        ctx.fill();

    }

    else if (type === "table") {

        ctx.fillStyle="#4b2813";

        ctx.fillRect(
            -size*.5,
            -size*.15,
            size,
            size*.15
        );

        ctx.fillRect(
            -size*.4,
            0,
            size*.1,
            size*.55
        );

        ctx.fillRect(
            size*.3,
            0,
            size*.1,
            size*.55
        );

    }

    ctx.restore();

}


function drawItem(type,sx,sy,size) {

    ctx.save();

    ctx.translate(sx,sy);

    if(type==="key") {

        ctx.fillStyle="#ffd700";

        ctx.beginPath();

        ctx.arc(
            0,
            -size*.3,
            size*.18,
            0,
            Math.PI*2
        );

        ctx.fill();

        ctx.fillRect(
            -size*.04,
            -size*.1,
            size*.08,
            size*.55
        );

        ctx.fillRect(
            0,
            size*.28,
            size*.2,
            size*.08
        );

    }

    if(type==="knife") {

        ctx.fillStyle="#ddd";

        ctx.beginPath();

        ctx.moveTo(0,-size*.7);
        ctx.lineTo(size*.16,size*.2);
        ctx.lineTo(-size*.16,size*.2);
        ctx.closePath();

        ctx.fill();

        ctx.fillStyle="#542710";

        ctx.fillRect(
            -size*.1,
            size*.18,
            size*.2,
            size*.4
        );

    }

    if(type==="potion") {

        ctx.fillStyle="#ff1744";

        ctx.beginPath();

        ctx.arc(
            0,
            size*.1,
            size*.28,
            0,
            Math.PI*2
        );

        ctx.fill();

        ctx.fillStyle="#8b5a2b";

        ctx.fillRect(
            -size*.1,
            -size*.25,
            size*.2,
            size*.18
        );

    }

    if(type==="battery") {

        ctx.fillStyle="#222";

        ctx.fillRect(
            -size*.25,
            -size*.35,
            size*.5,
            size*.65
        );

        ctx.fillStyle="#ff7300";

        ctx.fillRect(
            -size*.25,
            0,
            size*.5,
            size*.3
        );

        ctx.fillStyle="#fff";

        ctx.font="bold "+Math.floor(size*.3)+"px sans-serif";

        ctx.textAlign="center";

        ctx.fillText(
            "⚡",
            0,
            size*.2
        );

    }

    ctx.restore();

}


function drawGhost(sx,sy,size,stun) {

    ctx.save();

    ctx.translate(sx,sy);

    const alpha =
        stun > 0
        ? .35
        : .85;

    ctx.fillStyle =
        "rgba(210,225,255,"+alpha+")";

    ctx.beginPath();

    ctx.arc(
        0,
        -size*.35,
        size*.28,
        Math.PI,
        0
    );

    ctx.lineTo(
        size*.28,
        size*.45
    );

    ctx.lineTo(
        0,
        size*.25
    );

    ctx.lineTo(
        -size*.28,
        size*.45
    );

    ctx.closePath();

    ctx.fill();

    ctx.fillStyle =
        stun > 0
        ? "#00ffff"
        : "#ff1111";

    ctx.beginPath();

    ctx.arc(
        -size*.1,
        -size*.38,
        size*.06,
        0,
        Math.PI*2
    );

    ctx.fill();

    ctx.beginPath();

    ctx.arc(
        size*.1,
        -size*.38,
        size*.06,
        0,
        Math.PI*2
    );

    ctx.fill();

    ctx.restore();

}


function drawWeapon() {

    if(!items.knife) return;

    ctx.save();

    const swing =
        attackTimer > 0
        ? (12-attackTimer)*8
        : 0;

    ctx.translate(
        canvas.width-120-swing,
        canvas.height-90+swing
    );

    ctx.rotate(
        -.65 + swing*.035
    );

    ctx.fillStyle="#bbb";

    ctx.fillRect(
        -9,
        -115,
        18,
        90
    );

    ctx.fillStyle="#fff";

    ctx.fillRect(
        0,
        -115,
        8,
        90
    );

    ctx.fillStyle="#542710";

    ctx.fillRect(
        -18,
        -25,
        36,
        10
    );

    ctx.fillRect(
        -7,
        -15,
        14,
        35
    );

    ctx.restore();

}


function render() {

    ctx.save();

    if(shake > 0) {

        ctx.translate(
            (Math.random()-.5)*shake,
            (Math.random()-.5)*shake
        );

    }


    /*
        천장
    */
    const ceiling =
        ctx.createLinearGradient(
            0,
            0,
            0,
            canvas.height/2
        );

    ceiling.addColorStop(0,"#050505");
    ceiling.addColorStop(1,"#241716");

    ctx.fillStyle=ceiling;

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height/2
    );


    /*
        바닥
    */
    const floor =
        ctx.createLinearGradient(
            0,
            canvas.height/2,
            0,
            canvas.height
        );

    floor.addColorStop(0,"#241515");
    floor.addColorStop(1,"#050505");

    ctx.fillStyle=floor;

    ctx.fillRect(
        0,
        canvas.height/2,
        canvas.width,
        canvas.height/2
    );


    const rays=220;

    const fov=Math.PI*.43;

    const column =
        canvas.width/rays;

    const projection =
        (canvas.width/2) /
        Math.tan(fov/2);

    const z=[];


    for(let i=0;i<rays;i++) {

        const rayAngle =
            angle-fov/2+
            i/rays*fov;

        let dist=0;

        let tile=1;

        let hitX=0;

        while(dist<flashRange) {

            dist+=.025;

            const rx =
                px+Math.cos(rayAngle)*dist;

            const ry =
                py+Math.sin(rayAngle)*dist;

            const tx=Math.floor(rx);
            const ty=Math.floor(ry);

            if(
                tx<0 ||
                tx>=MAP_SIZE ||
                ty<0 ||
                ty>=MAP_SIZE
            ) {

                tile=1;
                break;

            }

            if(map[ty][tx]>0) {

                tile=map[ty][tx];

                hitX =
                    (rx-tx)+(ry-ty);

                break;

            }

        }


        const corrected =
            dist*Math.cos(rayAngle-angle);

        z[i]=corrected;


        const height =
            Math.min(
                canvas.height,
                projection/(corrected+.001)
            );


        const shade =
            Math.max(
                .15,
                1-corrected/flashRange
            );


        const x=i*column;
        const y=(canvas.height-height)/2;


        if(tile===2) {

            drawDoorTexture(
                x,
                y,
                column+1,
                height
            );

            ctx.fillStyle =
                "rgba(0,0,0,"+
                (1-shade)+")";

            ctx.fillRect(
                x,y,column+1,height
            );

        }

        else if(tile===3) {

            ctx.fillStyle =
                "rgba(220,175,40,"+
                shade+")";

            ctx.fillRect(
                x,y,column+1,height
            );

        }

        else {

            ctx.fillStyle =
                "rgba(65,39,32,"+
                shade+")";

            ctx.fillRect(
                x,y,column+1,height
            );

            /*
                벽의 세로 나무 무늬
            */
            if(i%14===0) {

                ctx.fillStyle =
                    "rgba(15,8,6,"+
                    shade*.45+")";

                ctx.fillRect(
                    x,
                    y,
                    1,
                    height
                );

            }

        }

    }


    /*
        가구 렌더링
    */
    furniture.forEach(f => {

        const dx=f.x-px;
        const dy=f.y-py;

        const dist=Math.sqrt(dx*dx+dy*dy);

        let a=
            Math.atan2(dy,dx)-angle;

        while(a<-Math.PI)
            a+=Math.PI*2;

        while(a>Math.PI)
            a-=Math.PI*2;

        if(
            Math.abs(a)<fov/1.8 &&
            dist<flashRange
        ) {

            const sx =
                canvas.width/2+
                Math.tan(a)*projection;

            const index =
                Math.floor(
                    sx/canvas.width*rays
                );

            if(
                index>=0 &&
                index<rays &&
                dist<z[index]
            ) {

                const size =
                    Math.min(
                        150,
                        projection*.55/dist
                    );

                drawFurniture(
                    f.type,
                    sx,
                    canvas.height/2+size*.4,
                    size
                );

            }

        }

    });


    /*
        아이템
    */
    worldItems.forEach(item => {

        const dx=item.x-px;
        const dy=item.y-py;

        const dist=Math.sqrt(dx*dx+dy*dy);

        let a=
            Math.atan2(dy,dx)-angle;

        while(a<-Math.PI)
            a+=Math.PI*2;

        while(a>Math.PI)
            a-=Math.PI*2;

        if(
            Math.abs(a)<fov/1.8 &&
            dist<flashRange
        ) {

            const sx =
                canvas.width/2+
                Math.tan(a)*projection;

            const index =
                Math.floor(
                    sx/canvas.width*rays
                );

            if(
                index>=0 &&
                index<rays &&
                dist<z[index]
            ) {

                const size =
                    Math.min(
                        90,
                        projection*.4/dist
                    );

                const float =
                    Math.sin(anim*2.5)*5;

                const sy =
                    canvas.height/2+
                    size*.25+
                    float;

                drawItem(
                    item.type,
                    sx,
                    sy,
                    size
                );

            }

        }

    });


    /*
        귀신
    */
    ghosts.forEach(g => {

        if(g.hp<=0) return;

        const dx=g.x-px;
        const dy=g.y-py;

        const dist=Math.sqrt(dx*dx+dy*dy);

        let a=
            Math.atan2(dy,dx)-angle;

        while(a<-Math.PI)
            a+=Math.PI*2;

        while(a>Math.PI)
            a-=Math.PI*2;

        if(
            Math.abs(a)<fov/1.8 &&
            dist<flashRange
        ) {

            const sx =
                canvas.width/2+
                Math.tan(a)*projection;

            const index =
                Math.floor(
                    sx/canvas.width*rays
                );

            if(
                index>=0 &&
                index<rays &&
                dist<z[index]
            ) {

                const size =
                    Math.min(
                        210,
                        projection*.75/dist
                    );

                drawGhost(
                    sx,
                    canvas.height/2+size*.2,
                    size,
                    g.stun
                );

            }

        }

    });


    drawWeapon();

    ctx.restore();

}


function update() {

    if(gameOver) return;

    anim+=.05;

    if(shake>0)
        shake--;


    /*
        회전
    */
    if(keys["left"])
        angle-=.045;

    if(keys["right"])
        angle+=.045;


    /*
        이동
    */
    const running =
        keys["e"] &&
        stamina>0;

    const speed =
        running
        ? .065
        : .038;


    if(running &&
       (keys["w"] ||
        keys["s"] ||
        keys["a"] ||
        keys["d"])) {

        stamina =
            Math.max(
                0,
                stamina-.42
            );

    } else {

        stamina =
            Math.min(
                100,
                stamina+.22
            );

    }


    let dx=0;
    let dy=0;


    if(keys["w"]) {

        dx+=Math.cos(angle)*speed;
        dy+=Math.sin(angle)*speed;

    }

    if(keys["s"]) {

        dx-=Math.cos(angle)*speed;
        dy-=Math.sin(angle)*speed;

    }


    /*
        A/D도 이동으로 사용할 수 있게
    */
    if(keys["a"]) {

        dx+=Math.cos(angle-Math.PI/2)*speed;
        dy+=Math.sin(angle-Math.PI/2)*speed;

    }

    if(keys["d"]) {

        dx+=Math.cos(angle+Math.PI/2)*speed;
        dy+=Math.sin(angle+Math.PI/2)*speed;

    }


    const margin=.2;


    if(
        !isSolid(
            px+dx+Math.sign(dx)*margin,
            py
        )
    ) {

        px+=dx;

    }


    if(
        !isSolid(
            px,
            py+dy+Math.sign(dy)*margin
        )
    ) {

        py+=dy;

    }


    updateRoomName();


    /*
        귀신 AI
    */
    ghosts.forEach(g => {

        if(g.hp<=0) return;

        if(g.stun>0) {

            g.stun--;

            return;

        }


        const dx=px-g.x;
        const dy=py-g.y;

        const dist=
            Math.sqrt(dx*dx+dy*dy);


        if(dist>0.1) {

            const speed=.017;

            const mx =
                dx/dist*speed;

            const my =
                dy/dist*speed;


            if(
                !isSolid(
                    g.x+mx,
                    g.y
                )
            ) {

                g.x+=mx;

            }


            if(
                !isSolid(
                    g.x,
                    g.y+my
                )
            ) {

                g.y+=my;

            }

        }


        if(dist<.65) {

            hp-=1.7;

            shake=5;

            if(hp<=0) {

                hp=0;

                triggerJumpscare();

            }

        }

    });


    /*
        귀신이 가까워지면 화면 글리치
    */
    let nearest=999;

    ghosts.forEach(g => {

        if(g.hp<=0) return;

        const dx=px-g.x;
        const dy=py-g.y;

        nearest=Math.min(
            nearest,
            Math.sqrt(dx*dx+dy*dy)
        );

    });


    if(nearest<5.5) {

        document.getElementById(
            "glitch-overlay"
        ).style.opacity =
            (5.5-nearest)/5.5*.75;

    } else {

        document.getElementById(
            "glitch-overlay"
        ).style.opacity=0;

    }


    if(attackTimer>0)
        attackTimer--;

    updateUI();

}


function gameLoop() {

    update();

    render();

    drawMap();

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
