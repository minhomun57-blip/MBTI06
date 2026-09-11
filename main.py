import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🏚️ 저주받은 저택",
    layout="wide"
)

st.title("🏚️ 저주받은 저택")
st.caption(
    "W/A/S/D 이동 | ←/→ 시점 회전 | "
    "E 달리기 | R 상호작용 | 1 회복약 | 2 배터리 | "
    "3 퇴마부적 | 4 열쇠 확인"
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
    background: linear-gradient(90deg, #650000, #ff1111, #ff5555);
    width: 100%;
}

#stamina {
    background: linear-gradient(90deg, #006633, #00cc66, #66ff99);
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
    background: rgba(0,0,0,0.4);
    padding: 8px 15px;
    border-radius: 6px;
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

.eye.left { left: 18%; }
.eye.right { right: 18%; }

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
    background: repeating-linear-gradient(90deg, white, white 13px, #300 13px, #300 18px);
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
    from { transform: translate(5px,-5px) scale(1.05); }
    to { transform: translate(-5px,5px) scale(1.1); }
}
</style>
</head>
<body>

<div id="ui">
    <div class="statusText">❤️ 생명력 <span id="hpText">100 / 100</span></div>
    <div class="bar"><div id="hp" class="fill"></div></div>
    <br>
    <div class="statusText">💨 스테미나 <span id="staminaText">100 / 100</span></div>
    <div class="bar"><div id="stamina" class="fill"></div></div>
    <div id="weapon">무기: 맨손</div>
</div>

<div id="mapBox">
    <div id="mapTitle">🗺️ 저택 지도 (노란점: 출구)</div>
    <canvas id="minimap"></canvas>
</div>

<div id="inventory">
    <div class="slot"><div class="key">[1]</div>💊 회복약<br><span id="potion">0</span></div>
    <div class="slot"><div class="key">[2]</div>🔋 배터리<br><span id="battery">0</span></div>
    <div class="slot"><div class="key">[3]</div>📜 퇴마부적<br><span id="talisman">1</span></div>
    <div class="slot"><div class="key">[4]</div>🔑 탈출열쇠<br><span id="key">없음</span></div>
</div>

<div id="msg">R키: 문 열기 / 아이템 획득</div>

<div id="gameover">
    <div id="ghostFace">
        <div class="eye left"><div class="pupil"></div></div>
        <div class="eye right"><div class="pupil"></div></div>
        <div class="mouth"><div class="teeth"></div></div>
    </div>
    <div id="gameoverText">당신의 영혼은 저택에 갇혔습니다...</div>
    <button id="restart" onclick="resetGame()">다시 도전</button>
</div>

<canvas id="canvas" tabindex="0"></canvas>

<script>
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
canvas.width = 900;
canvas.height = 600;

const mapCanvas = document.getElementById("minimap");
mapCtx = mapCanvas.getContext("2d");
mapCanvas.width = 180;
mapCanvas.height = 160;

let audioCtx = null;

function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
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
        osc.frequency.linearRampToValueAtTime(55, now + 0.3);
    } else if (type === "item") {
        osc.type = "sine";
        osc.frequency.setValueAtTime(500, now);
        osc.frequency.exponentialRampToValueAtTime(1000, now + 0.2);
    } else if (type === "scare") {
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(100, now);
        osc.frequency.exponentialRampToValueAtTime(1000, now + 0.5);
    }

    gain.gain.setValueAtTime(0.25, now);
    gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(now + 0.3);
}

// 0: 복도, 1: 벽, 2: 문, 3: 탈출구 (우측 중앙에 배치)
const initialMap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,1],
    [1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,0,0,0,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3], // <--- 우측 끝이 출구
    [1,0,1,1,1,1,1,0,0,0,0,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1],
    [1,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

let houseMap;
const MAP_SIZE = initialMap.length;

let px = 9.5, py = 10.5;
let angle = 0;
let hp = 100, stamina = 100;
let flashlight = 16;
let gameOver = false;

let items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
let ghost;
let worldItems = [];

function showMessage(text, color = "#ff5555") {
    const msg = document.getElementById("msg");
    msg.innerText = text;
    msg.style.color = color;
}

function updateUI() {
    document.getElementById("hpText").innerText = `${Math.ceil(hp)} / 100`;
    document.getElementById("hp").style.width = `${Math.max(0, hp)}%`;
    document.getElementById("staminaText").innerText = `${Math.ceil(stamina)} / 100`;
    document.getElementById("stamina").style.width = `${Math.max(0, stamina)}%`;
    
    document.getElementById("potion").innerText = items.potion;
    document.getElementById("battery").innerText = items.battery;
    document.getElementById("talisman").innerText = items.talisman;
    document.getElementById("key").innerText = items.key ? "소지중" : "없음";
    document.getElementById("weapon").innerText = `무기: ${items.knife ? "녹슨 단검" : "맨손"}`;
}

function initGame() {
    houseMap = JSON.parse(JSON.stringify(initialMap));
    px = 9.5; py = 10.5; angle = 0;
    hp = 100; stamina = 100; flashlight = 16;
    gameOver = false;
    items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };

    ghost = { x: 16.5, y: 16.5, hp: 100, stun: 0 };
    worldItems = [
        { x: 2.5, y: 2.5, type: "knife" },
        { x: 16.5, y: 2.5, type: "potion" },
        { x: 2.5, y: 8.5, type: "battery" },
        { x: 16.5, y: 16.5, type: "key" }
    ];

    document.getElementById("gameover").style.display = "none";
    showMessage("🏚️ 저택에 들어왔습니다. 열쇠(🔑)를 찾아 우측 노란 출구로 탈출하세요.", "#ff5555");
    updateUI();
}

function resetGame() {
    initGame();
}

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

window.addEventListener("keydown", (e) => {
    const k = normalizeKey(e.key);
    keys[k] = true;
    if(gameOver) return;

    if(k === "r") interact();
    if(e.key === "1") usePotion();
    if(e.key === "2") useBattery();
    if(e.key === "3") useTalisman();
});

window.addEventListener("keyup", (e) => {
    keys[normalizeKey(e.key)] = false;
});

function usePotion() {
    if(items.potion > 0 && hp < 100) {
        hp = Math.min(100, hp + 50);
        items.potion--;
        sound("item");
        showMessage("💊 체력을 회복했습니다.", "#66ff66");
        updateUI();
    }
}

function useBattery() {
    if(items.battery > 0) {
        flashlight = 20;
        items.battery--;
        sound("item");
        showMessage("🔋 손전등 밝기가 회복되었습니다.", "#ffff66");
        updateUI();
    }
}

function useTalisman() {
    if(items.talisman > 0 && ghost.hp > 0) {
        const dx = ghost.x - px, dy = ghost.y - py;
        if(Math.sqrt(dx*dx + dy*dy) < 6) {
            ghost.stun = 180;
            items.talisman--;
            sound("item");
            showMessage("📜 부적으로 귀신을 멈췄습니다!", "#00ffff");
            updateUI();
        }
    }
}

function interact() {
    if(gameOver) return;
    let tx = Math.floor(px + Math.cos(angle) * 1.2);
    let ty = Math.floor(py + Math.sin(angle) * 1.2);

    if(tx >= 0 && tx < MAP_SIZE && ty >= 0 && ty < MAP_SIZE) {
        const tile = houseMap[ty][tx];
        if(tile === 2) {
            houseMap[ty][tx] = 0;
            sound("door");
            showMessage("🚪 문을 열었습니다.", "#ffcc66");
            return;
        } else if(tile === 3) {
            if(items.key) {
                showMessage("🎉 탈출 성공! 저택에서 벗어났습니다!", "#00ff00");
                gameOver = true;
                return;
            } else {
                showMessage("🔒 문이 잠겨있습니다. 열쇠(🔑)가 필요합니다.", "#ff3333");
                return;
            }
        }
    }

    for(let i = worldItems.length - 1; i >= 0; i--) {
        const item = worldItems[i];
        if(Math.sqrt((px - item.x)**2 + (py - item.y)**2) < 1.2) {
            if(item.type === "knife") items.knife = true;
            if(item.type === "potion") items.potion++;
            if(item.type === "battery") items.battery++;
            if(item.type === "key") items.key = true;
            worldItems.splice(i, 1);
            sound("item");
            showMessage(`아이템을 획득했습니다!`, "#ffff66");
            updateUI();
            return;
        }
    }
}

function update() {
    if(gameOver) return;

    if(keys["left"]) angle -= 0.045;
    if(keys["right"]) angle += 0.045;

    let speed = keys["e"] && stamina > 0 ? 0.065 : 0.038;
    if(keys["e"] && (keys["w"]||keys["s"]||keys["a"]||keys["d"])) {
        stamina = Math.max(0, stamina - 0.4);
    } else {
        stamina = Math.min(100, stamina + 0.2);
    }

    let dx = 0, dy = 0;
    if(keys["w"]) { dx += Math.cos(angle) * speed; dy += Math.sin(angle) * speed; }
    if(keys["s"]) { dx -= Math.cos(angle) * speed; dy -= Math.sin(angle) * speed; }

    if(houseMap[Math.floor(py)][Math.floor(px + dx)] === 0 || houseMap[Math.floor(py)][Math.floor(px + dx)] === 3) px += dx;
    if(houseMap[Math.floor(py + dy)][Math.floor(px)] === 0 || houseMap[Math.floor(py + dy)][Math.floor(px)] === 3) py += dy;

    // 귀신 AI
    if(ghost.hp > 0) {
        if(ghost.stun > 0) {
            ghost.stun--;
        } else {
            let gdx = px - ghost.x;
            let gdy = py - ghost.y;
            let dist = Math.sqrt(gdx*gdx + gdy*gdy);
            if(dist > 0.5) {
                ghost.x += (gdx / dist) * 0.02;
                ghost.y += (gdy / dist) * 0.02;
            }
            if(dist < 0.8) {
                hp -= 0.5;
                if(hp <= 0) {
                    gameOver = true;
                    document.getElementById("gameover").style.display = "flex";
                    sound("scare");
                }
            }
        }
    }
    updateUI();
}

function render() {
    ctx.fillStyle = "#111";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 미니맵 그리기
    mapCtx.fillStyle = "#000";
    mapCtx.fillRect(0, 0, mapCanvas.width, mapCanvas.height);
    const size = mapCanvas.width / MAP_SIZE;
    for(let r=0; r<MAP_SIZE; r++) {
        for(let c=0; c<MAP_SIZE; c++) {
            if(houseMap[r][c] === 1) mapCtx.fillStyle = "#555";
            else if(houseMap[r][c] === 2) mapCtx.fillStyle = "#852";
            else if(houseMap[r][c] === 3) mapCtx.fillStyle = "#ffd700"; // 황금색 출구
            else mapCtx.fillStyle = "#111";
            mapCtx.fillRect(c*size, r*size, size-1, size-1);
        }
    }
    
    // 아이템 위치 표시
    mapCtx.fillStyle = "#00ffff";
    for(let item of worldItems) {
        mapCtx.fillRect(item.x*size - 1, item.y*size - 1, 3, 3);
    }

    // 플레이어 표시
    mapCtx.fillStyle = "#0f0";
    mapCtx.beginPath();
    mapCtx.arc(px*size, py*size, 3, 0, Math.PI*2);
    mapCtx.fill();
}

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

components.html(horror_game_html, height=650)
