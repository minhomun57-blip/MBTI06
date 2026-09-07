import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
page_title="🏚️ 저주받은 저택",
layout="wide"
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
}

.bar-fill {
    height: 100%;
    width: 100%;
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
    text-align: center;
}

.slot-key {
    color: #ffaa00;
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
}

#room-info {
    position: absolute;
    top: 15px;
    right: 15px;
    color: #aaa;
    font-size: 11px;
    text-align: right;
    z-index: 5;
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
}

.eye {
    position: absolute;
    top: 25%;
    width: 65px;
    height: 85px;
    background: #fff;
    border-radius: 50%;
    box-shadow:
        inset 0 0 30px #f00,
        0 0 20px #f00;
}

.eye.left {
    left: 18%;
}

.eye.right {
    right: 18%;
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

#scare-text {
    color: red;
    font-size: 30px;
    font-weight: 900;
    margin-top: 30px;
}

#restart-btn {
    margin-top: 25px;
    padding: 12px 32px;
    background: #050505;
    color: #f33;
    border: 1px solid red;
    cursor: pointer;
}
</style>

</head>

<body>

<div id="glitch-overlay"></div>

<div id="ui">

```
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
    <span id="weapon" style="color:#ffcc00;">
        맨손
    </span>
</div>
```

</div>

<div id="room-info">
    <div
        style="color:#ff3333;font-weight:bold;"
        id="current-room-name"
    >
        현재 위치: 중앙 홀
    </div>
    <div>화면 클릭 후 이동하세요</div>
</div>

<div id="inventory">

```
<div class="slot">
    <span class="slot-key">[1]</span>
    회복약
    <br>
    <span id="cnt-potion">0</span>
</div>

<div class="slot">
    <span class="slot-key">[2]</span>
    배터리
    <br>
    <span id="cnt-battery">0</span>
</div>

<div class="slot">
    <span class="slot-key">[3]</span>
    퇴마부적
    <br>
    <span id="cnt-talisman">1</span>
</div>

<div class="slot">
    <span class="slot-key">[4]</span>
    탈출열쇠
    <br>
    <span id="cnt-key">미획득</span>
</div>
```

</div>

<div id="msg">
화면을 클릭하여 게임을 시작하세요
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

<canvas id="canvas" tabindex="0"></canvas>

<script>

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

canvas.width = 900;
canvas.height = 580;


/* =========================
   게임 데이터
========================= */

let houseMap = [];
let MAP_SIZE = 21;

let px = 10.5;
let py = 10.5;

let angle = 0;

let hp = 100;
let stamina = 100;

let flashRange = 12;

let gameOver = false;

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

let isAttacking = 0;
let screenShake = 0;
let animTimer = 0;

const fov = Math.PI * 0.48;


/* =========================
   맵
=========================

   0 = 빈 공간
   1 = 벽
   2 = 얇은 문
   3 = 탈출문

   기존보다 방 개수를 줄이고
   중앙 홀을 크게 만듦.
*/

const initialMap = [

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],

[1,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],

[1,1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,1,1,1,1,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],

[1,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],

[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],

[1,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,1],

[1,1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,1,1,1,1,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],

[1,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,3,1],

[1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

];


/* =========================
   초기화
========================= */

function initGame() {

    houseMap =
        JSON.parse(
            JSON.stringify(initialMap)
        );

    MAP_SIZE = houseMap.length;

    /*
       벽에 붙어서 시작하지 않도록
       중앙 홀 안쪽에서 시작.
    */
    px = 10.5;
    py = 10.5;

    /*
       처음부터 벽이 눈앞에 보이는
       문제를 방지하기 위해
       아래쪽을 바라봄.
    */
    angle = Math.PI / 2;

    hp = 100;
    stamina = 100;

    flashRange = 12;

    gameOver = false;

    items = {
        potion: 0,
        battery: 0,
        talisman: 1,
        key: false,
        knife: false
    };

    /*
       ★ 귀신은 단 한 마리
    */
    ghosts = [
        {
            x: 18.5,
            y: 18.5,
            hp: 100,
            stun: 0
        }
    ];

    /*
       아이템
    */
    worldItems = [

        {
            x: 2.5,
            y: 2.5,
            type: "knife",
            name: "녹슨 단검"
        },

        {
            x: 18.5,
            y: 2.5,
            type: "potion",
            name: "회복약"
        },

        {
            x: 2.5,
            y: 10.5,
            type: "battery",
            name: "고전압 배터리"
        },

        {
            x: 18.5,
            y: 10.5,
            type: "potion",
            name: "회복약"
        },

        {
            x: 2.5,
            y: 18.5,
            type: "battery",
            name: "배터리"
        },

        {
            x: 18.5,
            y: 18.5,
            type: "key",
            name: "피묻은 열쇠"
        }

    ];


    /*
       ★ 가구를 많이 배치
    */
    furnitureList = [

        /* 북서쪽 방 */

        {
            x: 1.5,
            y: 1.5,
            type: "bookshelf",
            name: "큰 책장"
        },

        {
            x: 3.5,
            y: 1.5,
            type: "bookshelf",
            name: "낡은 책장"
        },

        {
            x: 1.5,
            y: 3.5,
            type: "desk",
            name: "나무 책상"
        },

        {
            x: 3.5,
            y: 3.5,
            type: "chair",
            name: "의자"
        },

        {
            x: 4.5,
            y: 2.5,
            type: "cabinet",
            name: "서류장"
        },


        /* 북동쪽 방 */

        {
            x: 17.5,
            y: 1.5,
            type: "bed",
            name: "낡은 침대"
        },

        {
            x: 19.0,
            y: 1.5,
            type: "cabinet",
            name: "약품장"
        },

        {
            x: 17.5,
            y: 3.5,
            type: "desk",
            name: "작업대"
        },

        {
            x: 19.0,
            y: 3.5,
            type: "chair",
            name: "의자"
        },


        /* 중앙 */

        {
            x: 8.5,
            y: 8.5,
            type: "clock",
            name: "괘종시계"
        },

        {
            x: 12.5,
            y: 8.5,
            type: "chair",
            name: "의자"
        },

        {
            x: 8.5,
            y: 12.5,
            type: "chair",
            name: "낡은 의자"
        },

        {
            x: 12.5,
            y: 12.5,
            type: "candelabra",
            name: "촛대"
        },

        {
            x: 10.5,
            y: 7.5,
            type: "candelabra",
            name: "촛대"
        },

        {
            x: 10.5,
            y: 13.5,
            type: "candelabra",
            name: "촛대"
        },


        /* 남서쪽 방 */

        {
            x: 1.5,
            y: 16.5,
            type: "bed",
            name: "핏자국 침대"
        },

        {
            x: 3.5,
            y: 16.5,
            type: "cabinet",
            name: "장롱"
        },

        {
            x: 1.5,
            y: 19,
            type: "bookshelf",
            name: "작은 책장"
        },

        {
            x: 3.5,
            y: 19,
            type: "desk",
            name: "작은 책상"
        },


        /* 남동쪽 방 */

        {
            x: 17.5,
            y: 16.5,
            type: "cabinet",
            name: "철제 보관함"
        },

        {
            x: 19,
            y: 16.5,
            type: "desk",
            name: "실험용 책상"
        },

        {
            x: 17.5,
            y: 19,
            type: "bookshelf",
            name: "실험 기록장"
        },

        {
            x: 19,
            y: 19,
            type: "chair",
            name: "낡은 의자"
        }

    ];

    document.getElementById(
        "jumpscare"
    ).style.display = "none";

    document.getElementById(
        "msg"
    ).innerText =
        "문 앞이나 아이템 근처에서 R 키를 누르세요";

    updateUI();
}


/* =========================
   키 입력
========================= */

const keys = {};

function parseKey(k) {

    if (k === "ArrowLeft")
        return "left";

    if (k === "ArrowRight")
        return "right";

    k = k.toLowerCase();

    if (k === "ㅈ") return "w";
    if (k === "ㄴ") return "s";
    if (k === "ㅁ") return "a";
    if (k === "ㅇ") return "d";
    if (k === "ㄷ") return "e";
    if (k === "ㄱ") return "r";

    return k;
}


/* =========================
   상호작용
========================= */

function handleInteract() {

    if (gameOver) return;

    let checkDist = 1.2;

    let targetX =
        Math.floor(
            px + Math.cos(angle) * checkDist
        );

    let targetY =
        Math.floor(
            py + Math.sin(angle) * checkDist
        );

    if (
        targetX >= 0 &&
        targetX < MAP_SIZE &&
        targetY >= 0 &&
        targetY < MAP_SIZE
    ) {

        let tile =
            houseMap[targetY][targetX];

        if (tile === 2) {

            houseMap[targetY][targetX] = 0;

            showTmpMsg(
                "🚪 문을 열었습니다."
            );

            return;
        }

        if (tile === 3) {

            if (items.key) {

                gameOver = true;

                document.getElementById(
                    "msg"
                ).innerText =
                    "🚪 탈출 성공!";

                document.getElementById(
                    "msg"
                ).style.color = "gold";

            } else {

                showTmpMsg(
                    "🔒 피묻은 열쇠가 필요합니다."
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

        let item = worldItems[i];

        let dist =
            Math.sqrt(
                (px-item.x)**2 +
                (py-item.y)**2
            );

        if (
            dist < 1.5 &&
            !picked
        ) {

            if (item.type === "key") {

                items.key = true;

                showTmpMsg(
                    "🔑 피묻은 열쇠를 획득했습니다!"
                );

            }

            if (item.type === "knife") {

                items.knife = true;

                showTmpMsg(
                    "🗡️ 녹슨 단검을 획득했습니다!"
                );

            }

            if (item.type === "potion") {

                items.potion++;

                showTmpMsg(
                    "💊 회복약을 획득했습니다!"
                );

            }

            if (item.type === "battery") {

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
            "상호작용할 대상이 없습니다."
        );
    }
}


/* =========================
   키보드
========================= */

window.addEventListener(
    "keydown",
    e => {

        let k = parseKey(e.key);

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

        if (gameOver) return;

        if (k === "r")
            handleInteract();

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

            showTmpMsg(
                "💊 체력을 회복했습니다."
            );

            updateUI();
        }

        if (
            e.key === "2" &&
            items.battery > 0
        ) {

            flashRange = 16;

            items.battery--;

            showTmpMsg(
                "🔋 손전등이 강해졌습니다."
            );

            updateUI();
        }

        if (
            e.key === "3" &&
            items.talisman > 0
        ) {

            ghosts.forEach(
                g => {

                    g.stun = 200;

                    g.x +=
                        (g.x-px)*0.5;

                    g.y +=
                        (g.y-py)*0.5;
                }
            );

            items.talisman--;

            screenShake = 12;

            showTmpMsg(
                "📜 부적으로 귀신을 밀어냈습니다!"
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
   마우스
========================= */

let isMouseDown = false;
let lastMouseX = 0;

canvas.addEventListener(
    "mousedown",
    e => {

        canvas.focus();

        isMouseDown = true;

        lastMouseX = e.clientX;

        if (
            items.knife &&
            isAttacking === 0 &&
            !gameOver
        ) {

            isAttacking = 10;

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

        if (isMouseDown) {

            let dx =
                e.clientX -
                lastMouseX;

            angle +=
                dx * 0.006;

            lastMouseX =
                e.clientX;
        }
    }
);


/* =========================
   공격
========================= */

function checkAttackHit() {

    ghosts.forEach(g => {

        if (g.hp <= 0)
            return;

        let dx =
            g.x - px;

        let dy =
            g.y - py;

        let dist =
            Math.sqrt(
                dx*dx +
                dy*dy
            );

        let a =
            Math.atan2(dy,dx)
            - angle;

        while (a < -Math.PI)
            a += Math.PI*2;

        while (a > Math.PI)
            a -= Math.PI*2;

        if (
            dist < 2.0 &&
            Math.abs(a) < 0.7
        ) {

            g.hp -= 50;

            g.stun = 50;

            screenShake = 8;

            if (g.hp <= 0) {

                showTmpMsg(
                    "💀 원혼을 성불시켰습니다!"
                );
            }
        }
    });
}


/* =========================
   UI
========================= */

function updateUI() {

    document.getElementById(
        "hp-bar"
    ).style.width =
        Math.max(0,hp) + "%";

    document.getElementById(
        "stamina-bar"
    ).style.width =
        Math.max(0,stamina) + "%";

    document.getElementById(
        "weapon"
    ).innerText =
        items.knife
        ? "녹슨 단검"
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


/* =========================
   충돌
========================= */

function isSolid(x,y) {

    if (
        x < 0 ||
        x >= MAP_SIZE ||
        y < 0 ||
        y >= MAP_SIZE
    )
        return true;

    let tile =
        houseMap[
            Math.floor(y)
        ][
            Math.floor(x)
        ];

    /*
       문 2는 열리기 전까지
       벽으로 취급
    */
    return (
        tile === 1 ||
        tile === 2
    );
}


/* =========================
   게임 오버
========================= */

function triggerJumpscare() {

    gameOver = true;

    document.getElementById(
        "jumpscare"
    ).style.display = "flex";
}


function resetGame() {

    initGame();
}


/* =========================
   메시지
========================= */

function showTmpMsg(txt) {

    let msg =
        document.getElementById(
            "msg"
        );

    msg.innerText = txt;

    setTimeout(
        () => {

            if (!gameOver &&
                msg.innerText === txt
            ) {

                msg.innerText = "";
            }

        },
        2500
    );
}


/* =========================
   게임 업데이트
========================= */

function update() {

    if (gameOver)
        return;

    animTimer += 0.05;

    if (screenShake > 0)
        screenShake--;


    /*
       회전
    */

    if (
        keys["left"] ||
        keys["a"]
    )
        angle -= 0.045;

    if (
        keys["right"] ||
        keys["d"]
    )
        angle += 0.045;


    /*
       이동
    */

    let running =
        keys["e"];

    let moving =
        keys["w"] ||
        keys["s"];

    let speed =
        running && stamina > 0
        ? 0.065
        : 0.038;

    if (
        running &&
        moving
    ) {

        stamina =
            Math.max(
                0,
                stamina - 0.4
            );

    } else {

        stamina =
            Math.min(
                100,
                stamina + 0.2
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


    const margin = 0.25;


    if (
        !isSolid(
            px + dx +
            Math.sign(dx)*margin,
            py
        )
    ) {

        px += dx;
    }


    if (
        !isSolid(
            px,
            py + dy +
            Math.sign(dy)*margin
        )
    ) {

        py += dy;
    }


    /*
       현재 방
    */

    let curX =
        Math.floor(px);

    let curY =
        Math.floor(py);

    let roomTxt =
        "중앙 홀";

    if (
        curX < 6 &&
        curY < 6
    )
        roomTxt =
            "북서쪽 서재";

    else if (
        curX > 14 &&
        curY < 6
    )
        roomTxt =
            "북동쪽 방";

    else if (
        curX < 6 &&
        curY > 14
    )
        roomTxt =
            "남서쪽 침실";

    else if (
        curX > 14 &&
        curY > 14
    )
        roomTxt =
            "남동쪽 밀실";

    document.getElementById(
        "current-room-name"
    ).innerText =
        "현재 위치: " +
        roomTxt;


    /*
       귀신 AI
       ★ 한 마리만 존재
    */

    let minDist = 999;

    ghosts.forEach(g => {

        if (g.hp <= 0)
            return;

        let dx =
            px - g.x;

        let dy =
            py - g.y;

        let dist =
            Math.sqrt(
                dx*dx +
                dy*dy
            );

        minDist =
            Math.min(
                minDist,
                dist
            );

        if (g.stun > 0) {

            g.stun--;

        } else {

            if (dist > 0.1) {

                let mx =
                    (dx/dist)*0.018;

                let my =
                    (dy/dist)*0.018;


                if (
                    !isSolid(
                        g.x + mx,
                        g.y
                    )
                )
                    g.x += mx;


                if (
                    !isSolid(
                        g.x,
                        g.y + my
                    )
                )
                    g.y += my;
            }


            if (dist < 0.6) {

                hp -= 2;

                screenShake = 5;

                if (hp <= 0)
                    triggerJumpscare();
            }
        }
    });


    /*
       귀신 근처 글리치
    */

    if (minDist < 5.5) {

        document.getElementById(
            "glitch-overlay"
        ).style.opacity =
            (
                (5.5-minDist)/5.5
            )*0.75;

    } else {

        document.getElementById(
            "glitch-overlay"
        ).style.opacity = 0;
    }


    if (isAttacking > 0)
        isAttacking--;

    updateUI();
}


/* =========================
   가구 그리기
========================= */

function drawFurniture(
    type,
    sx,
    sy,
    size
) {

    ctx.save();

    ctx.translate(sx,sy);


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
            "#111";

        ctx.fillRect(
            -size/2.3,
            -size/1.3,
            size/1.15,
            size*1.1
        );

        ctx.fillStyle =
            "#8b4513";

        for (
            let i=0;
            i<5;
            i++
        ) {

            ctx.fillRect(
                -size/2.2 +
                i*size/5,
                -size/1.1,
                size/9,
                size/2
            );
        }

    }

    else if (type === "desk") {

        ctx.fillStyle =
            "#4b2a15";

        ctx.fillRect(
            -size/1.3,
            -size/4,
            size*1.5,
            size/6
        );

        ctx.fillStyle =
            "#241308";

        ctx.fillRect(
            -size/1.3,
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
            "#573318";

        ctx.fillRect(
            -size/3,
            -size/3,
            size/1.5,
            size/8
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
            "#eee";

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
            "#777";

        ctx.fillRect(
            -size/12,
            -size/2,
            size/6,
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
            -size/1.5,
            size/8,
            0,
            Math.PI*2
        );

        ctx.fill();
    }


    ctx.restore();
}


/* =========================
   아이템
========================= */

function drawItem(
    type,
    sx,
    sy,
    size
) {

    ctx.save();

    ctx.translate(sx,sy);

    if (type === "key") {

        ctx.fillStyle =
            "#ffd700";

        ctx.beginPath();

        ctx.arc(
            0,
            -size/3,
            size/3,
            0,
            Math.PI*2
        );

        ctx.fill();

        ctx.fillRect(
            -size/12,
            -size/5,
            size/6,
            size
        );
    }

    else if (type === "knife") {

        ctx.fillStyle =
            "#ccc";

        ctx.beginPath();

        ctx.moveTo(
            0,
            -size
        );

        ctx.lineTo(
            size/6,
            0
        );

        ctx.lineTo(
            -size/6,
            0
        );

        ctx.closePath();

        ctx.fill();

        ctx.fillStyle =
            "#4a2511";

        ctx.fillRect(
            -size/5,
            0,
            size/2.5,
            size/2
        );
    }

    else if (type === "potion") {

        ctx.fillStyle =
            "#f22";

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
            size
        );

        ctx.fillStyle =
            "#ff6600";

        ctx.fillRect(
            -size/3,
            0,
            size/1.5,
            size/2.5
        );
    }

    ctx.restore();
}


/* =========================
   귀신
========================= */

function drawGhost(
    sx,
    sy,
    size,
    stun
) {

    ctx.save();

    ctx.translate(sx,sy);

    let alpha =
        stun > 0
        ? 0.35
        : 0.85;

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
   무기
========================= */

function drawWeapon() {

    if (!items.knife)
        return;

    ctx.save();

    let swing =
        isAttacking > 0
        ? (10-isAttacking)*8
        : 0;

    ctx.translate(
        canvas.width-150-swing,
        canvas.height-100+swing
    );

    ctx.rotate(
        -Math.PI/4
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
        "#4a2511";

    ctx.fillRect(
        -20,
        -20,
        40,
        10
    );

    ctx.fillRect(
        -8,
        -10,
        16,
        40
    );

    ctx.restore();
}


/* =========================
   3D 렌더링
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


    /*
       천장
    */

    let ceiling =
        ctx.createLinearGradient(
            0,
            0,
            0,
            canvas.height/2
        );

    ceiling.addColorStop(
        0,
        "#050505"
    );

    ceiling.addColorStop(
        1,
        "#211313"
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
       바닥
    */

    let floor =
        ctx.createLinearGradient(
            0,
            canvas.height/2,
            0,
            canvas.height
        );

    floor.addColorStop(
        0,
        "#241414"
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


    const numRays = 240;

    const w =
        canvas.width /
        numRays;

    const projDist =
        (canvas.width/2) /
        Math.tan(fov/2);

    let zBuffer =
        new Array(numRays);


    /*
       벽
    */

    for (
        let i=0;
        i<numRays;
        i++
    ) {

        let rayAngle =
            angle-fov/2 +
            (i/numRays)*fov;

        let distance = 0;

        let hit = false;

        let hitType = 1;

        let wallX = 0;


        while (
            !hit &&
            distance < flashRange
        ) {

            distance += 0.025;

            let rx =
                px +
                Math.cos(rayAngle) *
                distance;

            let ry =
                py +
                Math.sin(rayAngle) *
                distance;

            let tx =
                Math.floor(rx);

            let ty =
                Math.floor(ry);


            if (
                tx < 0 ||
                tx >= MAP_SIZE ||
                ty < 0 ||
                ty >= MAP_SIZE
            ) {

                hit = true;
                hitType = 1;

            } else if (
                houseMap[ty][tx] > 0
            ) {

                hit = true;

                hitType =
                    houseMap[ty][tx];

                wallX =
                    (
                        (rx-tx) +
                        (ry-ty)
                    ) % 1;

                if (wallX < 0)
                    wallX += 1;
            }
        }


        let corrected =
            distance *
            Math.cos(
                rayAngle-angle
            );

        zBuffer[i] =
            corrected;


        let h =
            Math.min(
                canvas.height,
                projDist /
                (corrected+0.0001)
            );


        let shade =
            Math.max(
                0.15,
                1-distance/
                flashRange
            );


        /*
           ★ 얇은 문
           문을 벽보다 훨씬 좁고
           어둡게 표현
        */

        if (hitType === 2) {

            let doorWidth =
                Math.max(
                    2,
                    w * 0.55
                );

            ctx.fillStyle =
                `rgba(75,35,15,${shade})`;

            ctx.fillRect(
                i*w +
                (w-doorWidth)/2,
                (canvas.height-h)/2,
                doorWidth,
                h
            );

            ctx.fillStyle =
                `rgba(20,8,4,${shade})`;

            ctx.fillRect(
                i*w +
                (w-doorWidth)/2,
                (canvas.height-h)/2,
                doorWidth,
                h
            );

            ctx.fillStyle =
                "#8a6818";

            ctx.fillRect(
                i*w +
                w/2,
                (canvas.height-h)/2,
                Math.max(2,w*.12),
                h
            );

        }

        else if (hitType === 3) {

            ctx.fillStyle =
                `rgba(230,190,60,${shade})`;

            ctx.fillRect(
                i*w,
                (canvas.height-h)/2,
                w+1,
                h
            );

        }

        else {

            ctx.fillStyle =
                `rgba(65,35,30,${shade})`;

            ctx.fillRect(
                i*w,
                (canvas.height-h)/2,
                w+1,
                h
            );
        }
    }


    /*
       가구
    */

    furnitureList.forEach(
        furn => {

            let dx =
                furn.x-px;

            let dy =
                furn.y-py;

            let dist =
                Math.sqrt(
                    dx*dx+
                    dy*dy
                );

            let a =
                Math.atan2(dy,dx)
                - angle;

            while (a < -Math.PI)
                a += Math.PI*2;

            while (a > Math.PI)
                a -= Math.PI*2;


            if (
                Math.abs(a) <
                fov/1.8 &&
                dist < flashRange
            ) {

                let sx =
                    canvas.width/2 +
                    Math.tan(a) *
                    projDist;

                let rayIndex =
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

                    let size =
                        Math.min(
                            180,
                            projDist*.55/dist
                        );

                    drawFurniture(
                        furn.type,
                        sx,
                        canvas.height/2+
                        size/2,
                        size
                    );
                }
            }
        }
    );


    /*
       아이템
    */

    worldItems.forEach(
        item => {

            let dx =
                item.x-px;

            let dy =
                item.y-py;

            let dist =
                Math.sqrt(
                    dx*dx+
                    dy*dy
                );

            let a =
                Math.atan2(dy,dx)
                - angle;

            while (a < -Math.PI)
                a += Math.PI*2;

            while (a > Math.PI)
                a -= Math.PI*2;


            if (
                Math.abs(a) <
                fov/1.8 &&
                dist < flashRange
            ) {

                let sx =
                    canvas.width/2 +
                    Math.tan(a) *
                    projDist;

                let rayIndex =
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

                    let size =
                        Math.min(
                            100,
                            projDist*.4/dist
                        );

                    let y =
                        canvas.height/2 +
                        size/3 +
                        Math.sin(
                            animTimer*2
                        )*5;

                    drawItem(
                        item.type,
                        sx,
                        y,
                        size
                    );

                    ctx.fillStyle =
                        "#fff";

                    ctx.font =
                        "bold 13px sans-serif";

                    ctx.textAlign =
                        "center";

                    ctx.shadowColor =
                        "#000";

                    ctx.shadowBlur = 5;

                    ctx.fillText(
                        item.name +
                        " [R]",
                        sx,
                        y-size
                    );

                    ctx.shadowBlur = 0;
                }
            }
        }
    );


    /*
       귀신
    */

    ghosts.forEach(
        g => {

            if (g.hp <= 0)
                return;

            let dx =
                g.x-px;

            let dy =
                g.y-py;

            let dist =
                Math.sqrt(
                    dx*dx+
                    dy*dy
                );

            let a =
                Math.atan2(dy,dx)
                - angle;

            while (a < -Math.PI)
                a += Math.PI*2;

            while (a > Math.PI)
                a -= Math.PI*2;


            if (
                Math.abs(a) <
                fov/1.8 &&
                dist < flashRange
            ) {

                let sx =
                    canvas.width/2 +
                    Math.tan(a) *
                    projDist;

                let rayIndex =
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

                    let size =
                        Math.min(
                            220,
                            projDist*.75/dist
                        );

                    drawGhost(
                        sx,
                        canvas.height/2+
                        size/4,
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
   게임 루프
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
