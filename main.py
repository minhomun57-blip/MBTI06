import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
page_title="🏚️ 저주받은 저택",
layout="wide"
)

st.title("🏚️ 저주받은 저택: 가구 확장판")
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
    overflow: hidden;
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
    color: #f33;
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
    pointer-events: none;
}

#glitch-overlay {
    position: absolute;
    inset: 0;
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
    inset: 0;
    background: #050000;
    z-index: 99;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

#scare-face {
    width: 340px;
    height: 400px;
    background: radial-gradient(circle,#800,#200,#000);
    border-radius: 45% 45% 50% 50%;
    position: relative;
    box-shadow: 0 0 150px #f00;
    animation: shake .02s infinite alternate;
}

.eye {
    position: absolute;
    top: 25%;
    width: 65px;
    height: 85px;
    background: white;
    border-radius: 50%;
    box-shadow: inset 0 0 30px red,0 0 20px red;
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
    background: black;
    border-radius: 50%;
}

.mouth {
    position: absolute;
    bottom: 8%;
    left: 10%;
    width: 80%;
    height: 150px;
    background: black;
    border-radius: 10px 10px 70px 70px;
    border: 4px solid #a00;
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
    font-weight: bold;
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

@keyframes shake {
    from {
        transform: translate(10px,-10px) scale(1.1);
    }
    to {
        transform: translate(-10px,10px) scale(1.2);
    }
}
</style>

</head>

<body>

<div id="glitch-overlay"></div>

<div id="ui">

```
<div>
    생명력
    <div class="bar-container">
        <div id="hp-bar" class="bar-fill"></div>
    </div>
</div>

<div>
    스테미나
    <div class="bar-container">
        <div id="stamina-bar" class="bar-fill"></div>
    </div>
</div>

<div>
    무기:
    <span id="weapon" style="color:#ffcc00">
        맨손
    </span>
</div>
```

</div>

<div id="room-info">
    <div id="current-room-name"
         style="color:#ff3333;font-weight:bold">
        현재 위치: 중앙 홀
    </div>
    <div>
        화면 클릭 후 WASD로 이동
    </div>
</div>

<div id="inventory">

```
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
    부적<br>
    <span id="cnt-talisman">1</span>
</div>

<div class="slot">
    <span class="slot-key">[4]</span>
    탈출열쇠<br>
    <span id="cnt-key">미획득</span>
</div>
```

</div>

<div id="msg">
문이나 아이템 근처에서 R
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
    당신의 영혼은 저택의 일부가 되었습니다...
</div>

<button id="restart-btn"
        onclick="resetGame()">
    다시 도전하기
</button>
```

</div>

<canvas id="canvas" tabindex="0"></canvas>

<script>

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

canvas.width = 800;
canvas.height = 580;


/* =========================
   게임 변수
========================= */

let MAP_SIZE = 25;

let px = 12.5;
let py = 12.5;

let angle = 0;

let hp = 100;
let stamina = 100;

let flashRange = 14;

let gameOver = false;

let isAttacking = 0;

let screenShake = 0;

let animTimer = 0;

let ghosts = [];

let worldItems = [];

let furnitureList = [];

let houseMap = [];

let items = {
    potion: 0,
    battery: 0,
    talisman: 1,
    key: false,
    knife: false
};

const keys = {};

const fov = Math.PI * 0.42;


/* =========================
   맵
   방을 4개에서 3개 구조로 축소
========================= */

const initialMap = [

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

[1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1],

[1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1],

[1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],

[1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1],

[1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1],

[1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],

[1,0,1,1,1,0,1,1,1,0,0,0,1,1,1,0,1,1,1,0,1,1,1,0,1],

[1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,1],

[1,0,1,0,0,0,2,0,1,0,0,0,1,0,1,0,2,0,0,0,1,0,1,0,1],

[1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,1],

[1,0,1,1,1,0,1,1,1,0,0,0,1,1,1,0,1,1,1,0,1,1,1,0,1],

[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],

[1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

[1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1],

[1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1],

[1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],

[1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1],

[1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1],

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1]

];


/* =========================
   텍스처
========================= */

const wallTex = document.createElement("canvas");

wallTex.width = 64;
wallTex.height = 64;

const wCtx = wallTex.getContext("2d");

wCtx.fillStyle = "#2d1d1a";
wCtx.fillRect(0,0,64,64);

wCtx.fillStyle = "#140a08";

for(let i=0;i<64;i+=16){

    wCtx.fillRect(0,i,64,2);

    for(let j=0;j<64;j+=16){

        let offset =
            (i/16)%2===0 ? 0 : 8;

        wCtx.fillRect(
            j+offset,
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

dCtx.fillStyle = "#241208";

dCtx.fillRect(
    0,0,64,64
);

dCtx.fillStyle = "#4b2915";

dCtx.fillRect(
    4,4,56,56
);

for(let x=5;x<60;x+=7){

    dCtx.fillStyle="#351b0c";

    dCtx.fillRect(
        x,5,2,54
    );
}


/* =========================
   초기화
========================= */

function initGame(){

    houseMap =
        JSON.parse(
            JSON.stringify(initialMap)
        );

    px = 12.5;
    py = 12.5;

    angle = 0;

    hp = 100;
    stamina = 100;

    flashRange = 14;

    gameOver = false;

    isAttacking = 0;

    screenShake = 0;

    items = {
        potion:0,
        battery:0,
        talisman:1,
        key:false,
        knife:false
    };


    ghosts = [

        {
            x:3.5,
            y:3.5,
            hp:100,
            stun:0
        },

        {
            x:20.5,
            y:3.5,
            hp:100,
            stun:0
        },

        {
            x:3.5,
            y:17.5,
            hp:100,
            stun:0
        }

    ];


    /* =====================
       아이템
    ===================== */

    worldItems = [

        {
            x:2.5,
            y:2.5,
            type:"knife",
            name:"녹슨 단검"
        },

        {
            x:21.5,
            y:2.5,
            type:"potion",
            name:"회복약"
        },

        {
            x:2.5,
            y:10.5,
            type:"battery",
            name:"배터리"
        },

        {
            x:21.5,
            y:10.5,
            type:"potion",
            name:"회복약"
        },

        {
            x:2.5,
            y:17.5,
            type:"battery",
            name:"배터리"
        },

        {
            x:21.5,
            y:18.5,
            type:"key",
            name:"피묻은 열쇠"
        }

    ];


    /* =====================
       가구 대폭 추가
    ===================== */

    furnitureList = [

        /* 서재 */

        {
            x:1.5,y:1.5,
            type:"bookshelf",
            name:"책장"
        },

        {
            x:4.5,y:1.5,
            type:"bookshelf",
            name:"책장"
        },

        {
            x:1.5,y:4.5,
            type:"desk",
            name:"책상"
        },

        {
            x:2.5,y:4.5,
            type:"chair",
            name:"의자"
        },

        {
            x:4.5,y:4.5,
            type:"cabinet",
            name:"서류함"
        },


        /* 중앙 홀 */

        {
            x:10.5,y:8.5,
            type:"clock",
            name:"괘종시계"
        },

        {
            x:12.5,y:8.5,
            type:"chair",
            name:"낡은 의자"
        },

        {
            x:14.5,y:8.5,
            type:"chair",
            name:"낡은 의자"
        },

        {
            x:10.5,y:11.5,
            type:"candelabra",
            name:"촛대"
        },

        {
            x:14.5,y:11.5,
            type:"candelabra",
            name:"촛대"
        },

        {
            x:11.5,y:13.5,
            type:"desk",
            name:"긴 테이블"
        },

        {
            x:13.5,y:13.5,
            type:"chair",
            name:"의자"
        },


        /* 침실 */

        {
            x:19.5,y:1.5,
            type:"bed",
            name:"침대"
        },

        {
            x:21.5,y:1.5,
            type:"cabinet",
            name:"옷장"
        },

        {
            x:19.5,y:4.5,
            type:"desk",
            name:"화장대"
        },

        {
            x:20.5,y:4.5,
            type:"chair",
            name:"의자"
        },

        {
            x:22.5,y:4.5,
            type:"cabinet",
            name:"서랍장"
        },


        /* 남쪽 방 */

        {
            x:1.5,y:16.5,
            type:"bed",
            name:"핏자국 침대"
        },

        {
            x:4.5,y:16.5,
            type:"bookshelf",
            name:"작은 책장"
        },

        {
            x:1.5,y:19.5,
            type:"cabinet",
            name:"철제 캐비닛"
        },

        {
            x:4.5,y:19.5,
            type:"desk",
            name:"실험 책상"
        },

        {
            x:5.0,y:19.5,
            type:"chair",
            name:"의자"
        },


        /* 남동쪽 방 */

        {
            x:19.5,y:16.5,
            type:"cabinet",
            name:"철제 보관함"
        },

        {
            x:21.5,y:16.5,
            type:"bookshelf",
            name:"낡은 책장"
        },

        {
            x:19.5,y:19.5,
            type:"desk",
            name:"실험대"
        },

        {
            x:21.5,y:19.5,
            type:"chair",
            name:"의자"
        }

    ];


    document.getElementById(
        "jumpscare"
    ).style.display="none";

    document.getElementById(
        "msg"
    ).innerText =
        "문이나 아이템 근처에서 R 키";

    updateUI();
}


function resetGame(){

    initGame();

}


/* =========================
   입력
========================= */

function parseKey(k){

    if(k==="ArrowLeft")
        return "left";

    if(k==="ArrowRight")
        return "right";

    return k.toLowerCase();
}


window.addEventListener(
    "keydown",
    e=>{

        let k=parseKey(e.key);

        keys[k]=true;

        if(
            [
                "ArrowUp",
                "ArrowDown",
                "ArrowLeft",
                "ArrowRight",
                " "
            ].includes(e.key)
        ){

            e.preventDefault();

        }


        if(gameOver)
            return;


        if(k==="r")
            handleInteract();


        if(e.key==="1" &&
           items.potion>0){

            hp=Math.min(
                100,
                hp+60
            );

            items.potion--;

            showTmpMsg(
                "💊 체력을 회복했습니다."
            );

            updateUI();

        }


        if(e.key==="2" &&
           items.battery>0){

            flashRange=18;

            items.battery--;

            showTmpMsg(
                "🔋 손전등이 강해졌습니다."
            );

            updateUI();

        }


        if(e.key==="3" &&
           items.talisman>0){

            ghosts.forEach(g=>{

                g.stun=200;

            });

            items.talisman--;

            screenShake=10;

            showTmpMsg(
                "📜 원혼을 퇴마했습니다."
            );

            updateUI();

        }

    }
);


window.addEventListener(
    "keyup",
    e=>{

        keys[
            parseKey(e.key)
        ]=false;

    }
);


/* =========================
   상호작용
========================= */

function handleInteract(){

    if(gameOver)
        return;


    let targetX =
        Math.floor(
            px+
            Math.cos(angle)*1.2
        );

    let targetY =
        Math.floor(
            py+
            Math.sin(angle)*1.2
        );


    if(
        targetX>=0 &&
        targetX<MAP_SIZE &&
        targetY>=0 &&
        targetY<MAP_SIZE
    ){

        let tile =
            houseMap[targetY][targetX];


        if(tile===2){

            houseMap[targetY][targetX]=0;

            showTmpMsg(
                "🚪 문을 열었습니다."
            );

            return;

        }


        if(tile===3){

            if(items.key){

                gameOver=true;

                document.getElementById(
                    "msg"
                ).innerText =
                    "🎉 탈출 성공!";

                document.getElementById(
                    "msg"
                ).style.color="gold";

            }else{

                showTmpMsg(
                    "🔒 피묻은 열쇠가 필요합니다."
                );

            }

            return;

        }

    }


    for(let i=worldItems.length-1;i>=0;i--){

        let item =
            worldItems[i];

        let dist =
            Math.hypot(
                px-item.x,
                py-item.y
            );


        if(dist<1.5){

            if(item.type==="key"){

                items.key=true;

                showTmpMsg(
                    "🔑 피묻은 열쇠를 얻었습니다!"
                );

            }


            if(item.type==="knife"){

                items.knife=true;

                showTmpMsg(
                    "🗡️ 녹슨 단검을 얻었습니다!"
                );

            }


            if(item.type==="potion"){

                items.potion++;

                showTmpMsg(
                    "💊 회복약을 얻었습니다."
                );

            }


            if(item.type==="battery"){

                items.battery++;

                showTmpMsg(
                    "🔋 배터리를 얻었습니다."
                );

            }


            worldItems.splice(i,1);

            updateUI();

            return;

        }

    }


    showTmpMsg(
        "상호작용할 대상이 없습니다."
    );

}


/* =========================
   UI
========================= */

function updateUI(){

    document.getElementById(
        "hp-bar"
    ).style.width =
        Math.max(0,hp)+"%";


    document.getElementById(
        "stamina-bar"
    ).style.width =
        Math.max(0,stamina)+"%";


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

function isSolid(x,y){

    if(
        x<0 ||
        x>=MAP_SIZE ||
        y<0 ||
        y>=MAP_SIZE
    )
        return true;


    let tile =
        houseMap[
            Math.floor(y)
        ][
            Math.floor(x)
        ];


    return tile===1 ||
           tile===2;

}


/* =========================
   임시 메시지
========================= */

function showTmpMsg(txt){

    let msg =
        document.getElementById(
            "msg"
        );

    msg.innerText=txt;

    setTimeout(()=>{

        if(
            !gameOver &&
            msg.innerText===txt
        ){

            msg.innerText="";

        }

    },2500);

}


/* =========================
   공격
========================= */

function checkAttackHit(){

    ghosts.forEach(g=>{

        if(g.hp<=0)
            return;


        let dx=g.x-px;
        let dy=g.y-py;

        let dist=Math.hypot(dx,dy);

        let a=
            Math.atan2(dy,dx)-angle;


        while(a<-Math.PI)
            a+=Math.PI*2;

        while(a>Math.PI)
            a-=Math.PI*2;


        if(
            dist<2 &&
            Math.abs(a)<0.7
        ){

            g.hp-=50;

            g.stun=50;

            screenShake=8;


            if(g.hp<=0){

                showTmpMsg(
                    "💀 원혼을 성불시켰습니다!"
                );

            }

        }

    });

}


let mouseDown=false;
let lastMouseX=0;


canvas.addEventListener(
    "mousedown",
    e=>{

        canvas.focus();

        mouseDown=true;

        lastMouseX=e.clientX;


        if(
            items.knife &&
            isAttacking===0 &&
            !gameOver
        ){

            isAttacking=10;

            checkAttackHit();

        }

    }
);


window.addEventListener(
    "mouseup",
    ()=>{
        mouseDown=false;
    }
);


window.addEventListener(
    "mousemove",
    e=>{

        if(mouseDown){

            let dx=
                e.clientX-lastMouseX;

            angle+=dx*0.006;

            lastMouseX=e.clientX;

        }

    }
);


/* =========================
   업데이트
========================= */

function update(){

    if(gameOver)
        return;


    animTimer+=0.05;


    if(screenShake>0)
        screenShake--;


    if(keys.left || keys.a)
        angle-=0.045;


    if(keys.right || keys.d)
        angle+=0.045;


    let running=
        keys.e &&
        stamina>0;


    let speed=
        running
        ? 0.065
        : 0.038;


    if(running &&
       (keys.w||keys.s)){

        stamina=Math.max(
            0,
            stamina-0.5
        );

    }else{

        stamina=Math.min(
            100,
            stamina+0.25
        );

    }


    let dx=0;
    let dy=0;


    if(keys.w){

        dx+=Math.cos(angle)*speed;
        dy+=Math.sin(angle)*speed;

    }


    if(keys.s){

        dx-=Math.cos(angle)*speed;
        dy-=Math.sin(angle)*speed;

    }


    if(
        !isSolid(
            px+dx,
            py
        )
    ){

        px+=dx;

    }


    if(
        !isSolid(
            px,
            py+dy
        )
    ){

        py+=dy;

    }


    /* 방 이름 */

    let x=Math.floor(px);
    let y=Math.floor(py);

    let room="중앙 홀";


    if(x<7 && y<7)
        room="북서쪽 서재";


    else if(x>17 && y<7)
        room="북동쪽 침실";


    else if(x<7 && y>14)
        room="남서쪽 침실";


    else if(x>17 && y>14)
        room="남동쪽 밀실";


    document.getElementById(
        "current-room-name"
    ).innerText =
        "현재 위치: "+room;


    /* 귀신 */

    let minDist=999;


    ghosts.forEach(g=>{

        if(g.hp<=0)
            return;


        let dx=px-g.x;
        let dy=py-g.y;

        let dist=Math.hypot(dx,dy);


        minDist=
            Math.min(
                minDist,
                dist
            );


        if(g.stun>0){

            g.stun--;

        }else{

            if(dist>0.1){

                let mx=
                    dx/dist*0.018;

                let my=
                    dy/dist*0.018;


                if(
                    !isSolid(
                        g.x+mx,
                        g.y
                    )
                )
                    g.x+=mx;


                if(
                    !isSolid(
                        g.x,
                        g.y+my
                    )
                )
                    g.y+=my;

            }


            if(dist<0.6){

                hp-=2;

                screenShake=5;


                if(hp<=0){

                    triggerJumpscare();

                }

            }

        }

    });


    if(minDist<5.5){

        document.getElementById(
            "glitch-overlay"
        ).style.opacity =
            (5.5-minDist)/5.5*.75;

    }else{

        document.getElementById(
            "glitch-overlay"
        ).style.opacity=0;

    }


    if(isAttacking>0)
        isAttacking--;


    updateUI();

}


/* =========================
   3D 가구
========================= */

function drawFurniture(
    type,
    sx,
    sy,
    size
){

    ctx.save();

    ctx.translate(
        sx,
        sy
    );


    if(type==="bookshelf"){

        ctx.fillStyle="#3a200d";

        ctx.fillRect(
            -size/2,
            -size,
            size,
            size*1.2
        );


        ctx.fillStyle="#160b05";

        ctx.fillRect(
            -size/2.3,
            -size/1.2,
            size/1.15,
            size
        );


        ctx.fillStyle="#6b3d1e";

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


        ctx.fillStyle="#aa2222";

        ctx.fillRect(
            -size/3,
            -size/1.1,
            size/8,
            size/3
        );


        ctx.fillStyle="#2288aa";

        ctx.fillRect(
            -size/8,
            -size/1.1,
            size/8,
            size/3
        );

    }


    else if(type==="desk"){

        ctx.fillStyle="#422817";

        ctx.fillRect(
            -size/1.3,
            -size/4,
            size*1.5,
            size/6
        );


        ctx.fillStyle="#241308";

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


    else if(type==="chair"){

        ctx.fillStyle="#3a200d";

        ctx.fillRect(
            -size/4,
            -size/1.2,
            size/2,
            size/1.8
        );


        ctx.fillStyle="#543118";

        ctx.fillRect(
            -size/3,
            -size/3,
            size/1.5,
            size/8
        );

    }


    else if(type==="bed"){

        ctx.fillStyle="#4a2e1b";

        ctx.fillRect(
            -size/1.2,
            -size/6,
            size*1.6,
            size/2
        );


        ctx.fillStyle="#aaa";

        ctx.fillRect(
            -size/1.1,
            -size/4,
            size*1.4,
            size/4
        );


        ctx.fillStyle="#eee";

        ctx.fillRect(
            -size/1.1,
            -size/3,
            size/2.5,
            size/5
        );

    }


    else if(type==="cabinet"){

        ctx.fillStyle="#30363b";

        ctx.fillRect(
            -size/3,
            -size,
            size/1.5,
            size*1.1
        );


        ctx.fillStyle="#666";

        ctx.fillRect(
            0,
            -size/2,
            size/10,
            size/8
        );

    }


    else if(type==="clock"){

        ctx.fillStyle="#2d1a0e";

        ctx.fillRect(
            -size/4,
            -size,
            size/2,
            size*1.3
        );


        ctx.fillStyle="#ffeecc";

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


    else if(type==="candelabra"){

        ctx.fillStyle="#887711";

        ctx.fillRect(
            -size/16,
            -size/2,
            size/8,
            size
        );


        ctx.fillStyle="#ff9900";

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
){

    ctx.save();

    ctx.translate(
        sx,
        sy
    );


    if(type==="key"){

        ctx.fillStyle="#ffd700";

        ctx.beginPath();

        ctx.arc(
            0,
            -size/3,
            size/3,
            0,
            Math.PI*2
        );

        ctx.fill();


        ctx.fillStyle="#111";

        ctx.beginPath();

        ctx.arc(
            0,
            -size/3,
            size/7,
            0,
            Math.PI*2
        );

        ctx.fill();


        ctx.fillStyle="#ffd700";

        ctx.fillRect(
            -size/10,
            -size/4,
            size/5,
            size
        );

    }


    else if(type==="knife"){

        ctx.fillStyle="#ccc";

        ctx.beginPath();

        ctx.moveTo(
            0,
            -size,
        );

        ctx.lineTo(
            size/5,
            0
        );

        ctx.lineTo(
            -size/5,
            0
        );

        ctx.closePath();

        ctx.fill();


        ctx.fillStyle="#4a2511";

        ctx.fillRect(
            -size/5,
            0,
            size/2.5,
            size/2
        );

    }


    else if(type==="potion"){

        ctx.fillStyle="#ff1133";

        ctx.beginPath();

        ctx.arc(
            0,
            size/5,
            size/2.5,
            0,
            Math.PI*2
        );

        ctx.fill();


        ctx.fillStyle="#8b5a2b";

        ctx.fillRect(
            -size/6,
            -size/3,
            size/3,
            size/5
        );

    }


    else if(type==="battery"){

        ctx.fillStyle="#222";

        ctx.fillRect(
            -size/3,
            -size/3,
            size/1.5,
            size
        );


        ctx.fillStyle="#ff6600";

        ctx.fillRect(
            -size/3,
            0,
            size/1.5,
            size/2
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
){

    ctx.save();

    ctx.translate(
        sx,
        sy
    );


    ctx.fillStyle =
        stun>0
        ? "rgba(100,255,255,.4)"
        : "rgba(210,220,255,.85)";


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
        stun>0
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

function drawWeapon(){

    if(!items.knife)
        return;


    ctx.save();


    let swing =
        isAttacking>0
        ? (10-isAttacking)*8
        : 0;


    ctx.translate(
        canvas.width-140-swing,
        canvas.height-100+swing
    );


    ctx.rotate(-Math.PI/4);


    ctx.fillStyle="#aaa";

    ctx.fillRect(
        -10,
        -120,
        20,
        100
    );


    ctx.fillStyle="#4a2511";

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
   렌더링
========================= */

function render(){

    ctx.save();


    if(screenShake>0){

        ctx.translate(
            (Math.random()-.5)*screenShake,
            (Math.random()-.5)*screenShake
        );

    }


    /* 천장 */

    let ceil=
        ctx.createLinearGradient(
            0,0,
            0,canvas.height/2
        );

    ceil.addColorStop(
        0,
        "#050505"
    );

    ceil.addColorStop(
        1,
        "#241515"
    );


    ctx.fillStyle=ceil;

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height/2
    );


    /* 바닥 */

    let floor=
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
        "#030303"
    );


    ctx.fillStyle=floor;

    ctx.fillRect(
        0,
        canvas.height/2,
        canvas.width,
        canvas.height/2
    );


    const numRays=160;

    const w=
        canvas.width/numRays;


    const projDist=
        canvas.width/2/
        Math.tan(fov/2);


    let zBuffer=
        new Array(numRays);


    let curRange=
        flashRange+
        (Math.random()-.5)*.2;


    /* 벽 */

    for(
        let i=0;
        i<numRays;
        i++
    ){

        let rayAngle=
            angle-fov/2+
            (i/numRays)*fov;


        let distance=0;

        let hit=false;

        let hitType=1;

        let wallX=0;


        while(
            !hit &&
            distance<curRange
        ){

            distance+=.025;


            let rx=
                px+
                Math.cos(rayAngle)*
                distance;


            let ry=
                py+
                Math.sin(rayAngle)*
                distance;


            let tx=Math.floor(rx);
            let ty=Math.floor(ry);


            if(
                tx<0 ||
                tx>=MAP_SIZE ||
                ty<0 ||
                ty>=MAP_SIZE
            ){

                hit=true;

            }


            else if(
                houseMap[ty][tx]>0
            ){

                hit=true;

                hitType=
                    houseMap[ty][tx];


                wallX=
                    ((rx-tx)+(ry-ty));

                wallX=
                    (wallX-
                     Math.floor(wallX))*64;

            }

        }


        let corrected=
            distance*
            Math.cos(
                rayAngle-angle
            );


        zBuffer[i]=corrected;


        let h=
            Math.min(
                canvas.height,
                projDist/
                (corrected+.0001)
            );


        let shade=
            Math.max(
                .15,
                1-corrected/curRange
            );


        if(hitType===3){

            ctx.fillStyle=
                `rgba(230,190,60,${shade})`;

            ctx.fillRect(
                i*w,
                (canvas.height-h)/2,
                w+1,
                h
            );

        }


        else if(hitType===2){

            ctx.drawImage(
                doorTex,
                Math.floor(wallX),
                0,
                1,
                64,
                i*w,
                (canvas.height-h)/2,
                w+1,
                h
            );

        }


        else{

            ctx.drawImage(
                wallTex,
                Math.floor(wallX),
                0,
                1,
                64,
                i*w,
                (canvas.height-h)/2,
                w+1,
                h
            );

        }

    }


    /* 가구 */

    furnitureList.forEach(
        furn=>{

            let dx=
                furn.x-px;

            let dy=
                furn.y-py;


            let dist=
                Math.hypot(dx,dy);


            let a=
                Math.atan2(dy,dx)-angle;


            while(a<-Math.PI)
                a+=Math.PI*2;

            while(a>Math.PI)
                a-=Math.PI*2;


            if(
                Math.abs(a)<fov/1.8 &&
                dist<curRange
            ){

                let sx=
                    canvas.width/2+
                    Math.tan(a)*
                    projDist;


                let index=
                    Math.floor(
                        sx/canvas.width*
                        numRays
                    );


                if(
                    index>=0 &&
                    index<numRays &&
                    dist<zBuffer[index]
                ){

                    let size=
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


    /* 아이템 */

    worldItems.forEach(
        item=>{

            let dx=
                item.x-px;

            let dy=
                item.y-py;


            let dist=
                Math.hypot(dx,dy);


            let a=
                Math.atan2(dy,dx)-angle;


            while(a<-Math.PI)
                a+=Math.PI*2;

            while(a>Math.PI)
                a-=Math.PI*2;


            if(
                Math.abs(a)<fov/1.8 &&
                dist<curRange
            ){

                let sx=
                    canvas.width/2+
                    Math.tan(a)*
                    projDist;


                let index=
                    Math.floor(
                        sx/canvas.width*
                        numRays
                    );


                if(
                    index>=0 &&
                    index<numRays &&
                    dist<zBuffer[index]
                ){

                    let size=
                        Math.min(
                            120,
                            projDist*.45/dist
                        );


                    drawItem(
                        item.type,
                        sx,
                        canvas.height/2+
                        size/3,
                        size
                    );


                    ctx.fillStyle="white";

                    ctx.font=
                        "bold 12px sans-serif";

                    ctx.textAlign="center";

                    ctx.fillText(
                        item.name+
                        " [R]",
                        sx,
                        canvas.height/2-
                        size
                    );

                }

            }

        }
    );


    /* 귀신 */

    ghosts.forEach(
        g=>{

            if(g.hp<=0)
                return;


            let dx=
                g.x-px;

            let dy=
                g.y-py;


            let dist=
                Math.hypot(dx,dy);


            let a=
                Math.atan2(dy,dx)-angle;


            while(a<-Math.PI)
                a+=Math.PI*2;

            while(a>Math.PI)
                a-=Math.PI*2;


            if(
                Math.abs(a)<fov/1.8 &&
                dist<curRange
            ){

                let sx=
                    canvas.width/2+
                    Math.tan(a)*
                    projDist;


                let index=
                    Math.floor(
                        sx/canvas.width*
                        numRays
                    );


                if(
                    index>=0 &&
                    index<numRays &&
                    dist<zBuffer[index]
                ){

                    let size=
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

function triggerJumpscare(){

    gameOver=true;

    document.getElementById(
        "jumpscare"
    ).style.display="flex";

}


function gameLoop(){

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
