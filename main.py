import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🏚️ 저주받은 저택",
    layout="wide"
)

st.title("🏚️ 저주받은 저택")
st.caption(
    "W/A/S/D 이동 | ←/→ 또는 마우스 드래그: 시점 회전 | "
    "E 달리기 | R 상호작용 | 1 회복약 | 2 배터리 | "
    "3 퇴마부적"
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
    user-select: none;
}

#canvas {
    width: 100%;
    height: 600px;
    display: block;
    background: #000;
    cursor: crosshair;
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
    background: rgba(0,0,0,0.6);
    padding: 12px;
    border-radius: 8px;
    min-width: 220px;
}

.bar {
    width: 200px;
    height: 16px;
    background: #111;
    border: 1px solid #777;
    margin-top: 4px;
    border-radius: 4px;
    overflow: hidden;
}

.fill {
    height: 100%;
    transition: width 0.1s linear;
}

#hp { background: #e74c3c; width: 100%; }
#stamina { background: #2ecc71; width: 100%; }

.statusText {
    font-weight: bold;
    margin-top: 4px;
}

#mapBox {
    position: absolute;
    right: 15px;
    top: 15px;
    width: 200px;
    height: 200px;
    background: rgba(0,0,0,0.85);
    border: 2px solid #555;
    z-index: 10;
    border-radius: 8px;
    overflow: hidden;
}

#mapTitle {
    color: #fff;
    text-align: center;
    padding: 4px;
    font-size: 11px;
    border-bottom: 1px solid #444;
    background: #111;
}

#minimap {
    width: 200px;
    height: 175px;
    display: block;
}

#inventory {
    position: absolute;
    bottom: 15px;
    right: 15px;
    z-index: 10;
    display: flex;
    gap: 8px;
    pointer-events: none;
}

.slot {
    width: 65px;
    height: 60px;
    background: rgba(10,10,10,0.85);
    border: 1px solid #555;
    color: #ddd;
    text-align: center;
    font-size: 11px;
    padding-top: 5px;
    border-radius: 6px;
}

.key {
    color: #f1c40f;
    font-weight: bold;
}

#msg {
    position: absolute;
    left: 50%;
    top: 25%;
    transform: translate(-50%, -50%);
    color: #ff4444;
    font-size: 18px;
    font-weight: bold;
    z-index: 20;
    text-align: center;
    text-shadow: 0 0 8px #000;
    pointer-events: none;
    background: rgba(0,0,0,0.6);
    padding: 10px 20px;
    border-radius: 8px;
    border: 1px solid #444;
}

#gameover {
    display: none;
    position: absolute;
    inset: 0;
    z-index: 100;
    background: rgba(0,0,0,0.95);
    color: #e74c3c;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

#gameoverText {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
}

#restart {
    background: #222;
    border: 1px solid #e74c3c;
    color: #e74c3c;
    padding: 10px 25px;
    cursor: pointer;
    font-size: 16px;
    border-radius: 4px;
}

#restart:hover {
    background: #e74c3c;
    color: #fff;
}
</style>
</head>
<body>

<div id="ui">
    <div class="statusText">❤️ 체력 <span id="hpText">100 / 100</span></div>
    <div class="bar"><div id="hp" class="fill"></div></div>
    <div class="statusText" style="margin-top:8px;">💨 스테미나 <span id="staminaText">100 / 100</span></div>
    <div class="bar"><div id="stamina" class="fill"></div></div>
</div>

<div id="mapBox">
    <div id="mapTitle">🗺️ 저택 지도 (🟨 출구)</div>
    <canvas id="minimap"></canvas>
</div>

<div id="inventory">
    <div class="slot"><div class="key">[1]</div>💊 회복약<br><span id="potion">0</span></div>
    <div class="slot"><div class="key">[2]</div>🔋 배터리<br><span id="battery">0</span></div>
    <div class="slot"><div class="key">[3]</div>📜 부적<br><span id="talisman">1</span></div>
    <div class="slot"><div class="key">[4]</div>🔑 열쇠<br><span id="key">없음</span></div>
</div>

<div id="msg">저택에서 열쇠를 찾아 탈출하세요!</div>

<div id="gameover">
    <div id="gameoverText">당신의 영혼은 저택에 갇혔습니다...</div>
    <button id="restart" onclick="resetGame()">다시 도전</button>
</div>

<canvas id="canvas"></canvas>

<script>
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
canvas.width = 900;
canvas.height = 600;

const mapCanvas = document.getElementById("minimap");
mapCtx = mapCanvas.getContext("2d");
mapCanvas.width = 200;
mapCanvas.height = 175;

const houseMap = [
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
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [1,0,1,1,1,1,1,0,0,0,0,0,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,1],
    [1,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

const MAP_SIZE = houseMap.length;

let px = 9.5, py = 10.5;
let angle = 0;
let fov = Math.PI / 3;
let hp = 100, stamina = 100;
let gameOver = false;

let items = { potion: 1, battery: 1, talisman: 1, key: false };
let ghost = { x: 16.5, y: 16.5, stun: 0 };
let worldItems = [
    { x: 2.5, y: 2.5, type: "potion", icon: "💊" },
    { x: 16.5, y: 2.5, type: "battery", icon: "🔋" },
    { x: 16.5, y: 16.5, type: "key", icon: "🔑" }
];

let depthBuffer = new Array(canvas.width);

let isDragging = false;
let prevMouseX = 0;

canvas.addEventListener("mousedown", (e) => {
    isDragging = true;
    prevMouseX = e.clientX;
});
window.addEventListener("mouseup", () => isDragging = false);
window.addEventListener("mousemove", (e) => {
    if (isDragging) {
        let deltaX = e.clientX - prevMouseX;
        angle += deltaX * 0.005;
        prevMouseX = e.clientX;
    }
});

function showMessage(text, color = "#ff4444") {
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
}

function initGame() {
    px = 9.5; py = 10.5; angle = 0;
    hp = 100; stamina = 100;
    gameOver = false;
    items = { potion: 1, battery: 1, talisman: 1, key: false };

    ghost = { x: 16.5, y: 16.5, stun: 0 };
    worldItems = [
        { x: 2.5, y: 2.5, type: "potion", icon: "💊" },
        { x: 16.5, y: 2.5, type: "battery", icon: "🔋" },
        { x: 16.5, y: 16.5, type: "key", icon: "🔑" }
    ];

    document.getElementById("gameover").style.display = "none";
    showMessage("저택에서 열쇠(🔑)를 찾아 탈출하세요!", "#ffffff");
    updateUI();
}

function resetGame() {
    initGame();
}

const keys = {};
window.addEventListener("keydown", (e) => {
    let k = e.key.toLowerCase();
    if (k === "arrowleft") k = "left";
    if (k === "arrowright") k = "right";
    keys[k] = true;

    if (gameOver) return;
    if (k === "r") interact();
    if (k === "1") usePotion();
    if (k === "2") useBattery();
    if (k === "3") useTalisman();
});

window.addEventListener("keyup", (e) => {
    let k = e.key.toLowerCase();
    if (k === "arrowleft") k = "left";
    if (k === "arrowright") k = "right";
    keys[k] = false;
});

function usePotion() {
    if (items.potion > 0 && hp < 100) {
        hp = Math.min(100, hp + 50);
        items.potion--;
        showMessage("💊 체력을 회복했습니다.", "#2ecc71");
        updateUI();
    }
}

function useBattery() {
    if (items.battery > 0) {
        items.battery--;
        showMessage("🔋 배터리를 사용했습니다.", "#f1c40f");
        updateUI();
    }
}

function useTalisman() {
    if (items.talisman > 0) {
        let dx = ghost.x - px, dy = ghost.y - py;
        if (Math.sqrt(dx*dx + dy*dy) < 6) {
            ghost.stun = 200;
            items.talisman--;
            showMessage("📜 부적으로 귀신을 멈췄습니다!", "#3498db");
            updateUI();
        }
    }
}

function interact() {
    let tx = Math.floor(px + Math.cos(angle) * 1.2);
    let ty = Math.floor(py + Math.sin(angle) * 1.2);

    if (tx >= 0 && tx < MAP_SIZE && ty >= 0 && ty < MAP_SIZE) {
        let tile = houseMap[ty][tx];
        if (tile === 2) {
            houseMap[ty][tx] = 0;
            showMessage("🚪 문을 열었습니다.", "#f39c12");
            return;
        } else if (tile === 3) {
            if (items.key) {
                showMessage("🎉 탈출 성공! 저택에서 벗어났습니다!", "#2ecc71");
                gameOver = true;
                return;
            } else {
                showMessage("🔒 열쇠(🔑)가 필요합니다.", "#e74c3c");
                return;
            }
        }
    }

    for (let i = worldItems.length - 1; i >= 0; i--) {
        let item = worldItems[i];
        if (Math.sqrt((px - item.x)**2 + (py - item.y)**2) < 1.2) {
            if (item.type === "potion") items.potion++;
            if (item.type === "battery") items.battery++;
            if (item.type === "key") items.key = true;
            worldItems.splice(i, 1);
            showMessage("아이템을 획득했습니다!", "#f1c40f");
            updateUI();
            return;
        }
    }
}

function isSolid(x, y) {
    let gx = Math.floor(x);
    let gy = Math.floor(y);
    if (gx < 0 || gx >= MAP_SIZE || gy < 0 || gy >= MAP_SIZE) return true;
    return houseMap[gy][gx] === 1 || houseMap[gy][gx] === 2;
}

function update() {
    if (gameOver) return;

    if (keys["left"]) angle -= 0.04;
    if (keys["right"]) angle += 0.04;

    let speed = keys["e"] && stamina > 0 ? 0.06 : 0.035;
    if (keys["e"] && (keys["w"] || keys["s"] || keys["a"] || keys["d"])) {
        stamina = Math.max(0, stamina - 0.4);
    } else {
        stamina = Math.min(100, stamina + 0.25);
    }

    let dx = 0, dy = 0;
    if (keys["w"]) { dx += Math.cos(angle) * speed; dy += Math.sin(angle) * speed; }
    if (keys["s"]) { dx -= Math.cos(angle) * speed; dy -= Math.sin(angle) * speed; }
    if (keys["a"]) { dx += Math.sin(angle) * speed; dy -= Math.cos(angle) * speed; }
    if (keys["d"]) { dx -= Math.sin(angle) * speed; dy += Math.cos(angle) * speed; }

    let nx = px + dx;
    let ny = py + dy;

    if (!isSolid(nx, py)) px = nx;
    if (!isSolid(px, ny)) py = ny;

    // 귀신 AI (벽 충돌 알고리즘 개선)
    if (ghost.stun > 0) {
        ghost.stun--;
    } else {
        let gdx = px - ghost.x;
        let gdy = py - ghost.y;
        let dist = Math.sqrt(gdx*gdx + gdy*gdy);
        if (dist > 0.5) {
            let ghostSpeed = 0.022;
            let moveX = (gdx / dist) * ghostSpeed;
            let moveY = (gdy / dist) * ghostSpeed;

            // 벽을 통과하지 못하도록 미끄러짐 방지 처리
            if (!isSolid(ghost.x + moveX, ghost.y)) {
                ghost.x += moveX;
            }
            if (!isSolid(ghost.x, ghost.y + moveY)) {
                ghost.y += moveY;
            }
        }
        if (dist < 0.7) {
            hp -= 0.6;
            if (hp <= 0) {
                gameOver = true;
                document.getElementById("gameover").style.display = "flex";
            }
        }
    }
    updateUI();
}

function render3D() {
    ctx.fillStyle = "#050505";
    ctx.fillRect(0, 0, canvas.width, canvas.height / 2);
    ctx.fillStyle = "#111";
    ctx.fillRect(0, canvas.height / 2, canvas.width, canvas.height / 2);

    const numRays = canvas.width;
    const halfFov = fov / 2;

    for (let i = 0; i < numRays; i++) {
        let rayAngle = (angle - halfFov) + (i / numRays) * fov;
        let distance = 0;
        let hitWall = false;
        let wallType = 0;

        let cosA = Math.cos(rayAngle);
        let sinA = Math.sin(rayAngle);

        while (!hitWall && distance < 16) {
            distance += 0.04;
            let checkX = Math.floor(px + cosA * distance);
            let checkY = Math.floor(py + sinA * distance);

            if (checkX < 0 || checkX >= MAP_SIZE || checkY < 0 || checkY >= MAP_SIZE) {
                hitWall = true;
                distance = 16;
            } else if (houseMap[checkY][checkX] > 0) {
                hitWall = true;
                wallType = houseMap[checkY][checkX];
            }
        }

        let correctedDist = distance * Math.cos(rayAngle - angle);
        depthBuffer[i] = correctedDist;

        let wallHeight = Math.min(canvas.height, (canvas.height / correctedDist));

        let color = "#333333";
        if (wallType === 1) color = "#4a4a4a";
        if (wallType === 2) color = "#8b5a2b";
        if (wallType === 3) color = "#f1c40f";

        let shade = Math.max(0, 1 - correctedDist / 12);
        ctx.fillStyle = color;
        ctx.globalAlpha = shade;
        ctx.fillRect(i, (canvas.height - wallHeight) / 2, 1, wallHeight);
        ctx.globalAlpha = 1.0;
    }

    // 3D 공간에 아이템 및 귀신 스프라이트 투영
    let sprites = [];

    for (let item of worldItems) {
        sprites.push({ x: item.x, y: item.y, text: item.icon, type: "item" });
    }
    sprites.push({ x: ghost.x, y: ghost.y, text: "👻", type: "ghost" });

    sprites.forEach(s => {
        let dx = s.x - px;
        let dy = s.y - py;
        let spriteDist = Math.sqrt(dx*dx + dy*dy);

        let spriteAngle = Math.atan2(dy, dx) - angle;
        while (spriteAngle < -Math.PI) spriteAngle += Math.PI * 2;
        while (spriteAngle > Math.PI) spriteAngle -= Math.PI * 2;

        if (Math.abs(spriteAngle) < fov) {
            let screenX = (canvas.width / 2) + Math.tan(spriteAngle) * (canvas.width / (2 * Math.tan(fov / 2)));
            let size = canvas.height / (spriteDist * Math.cos(spriteAngle));

            let colX = Math.floor(screenX);
            if (colX >= 0 && colX < canvas.width && spriteDist < depthBuffer[colX]) {
                ctx.save();
                ctx.font = `${Math.max(12, Math.floor(size * 0.4))}px sans-serif`;
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                let alpha = Math.max(0, 1 - spriteDist / 12);
                ctx.globalAlpha = alpha;
                ctx.fillText(s.text, screenX, canvas.height / 2);
                ctx.restore();
            }
        }
    });
}

function renderMinimap() {
    mapCtx.fillStyle = "#000";
    mapCtx.fillRect(0, 0, mapCanvas.width, mapCanvas.height);
    const size = mapCanvas.width / MAP_SIZE;

    for (let r = 0; r < MAP_SIZE; r++) {
        for (let c = 0; c < MAP_SIZE; c++) {
            if (houseMap[r][c] === 1) mapCtx.fillStyle = "#555";
            else if (houseMap[r][c] === 2) mapCtx.fillStyle = "#8b5a2b";
            else if (houseMap[r][c] === 3) mapCtx.fillStyle = "#f1c40f";
            else mapCtx.fillStyle = "#1a1a1a";
            mapCtx.fillRect(c * size, r * size, size - 0.5, size - 0.5);
        }
    }

    mapCtx.fillStyle = "#f1c40f";
    for (let item of worldItems) {
        mapCtx.fillRect(item.x * size - 1.5, item.y * size - 1.5, 3, 3);
    }

    mapCtx.fillStyle = "#e74c3c";
    mapCtx.fillRect(ghost.x * size - 2, ghost.y * size - 2, 4, 4);

    mapCtx.fillStyle = "#2ecc71";
    mapCtx.beginPath();
    mapCtx.arc(px * size, py * size, 3, 0, Math.PI * 2);
    mapCtx.fill();
}

function loop() {
    update();
    render3D();
    renderMinimap();
    requestAnimationFrame(loop);
}

initGame();
loop();
</script>
</body>
</html>
"""

components.html(horror_game_html, height=650)
