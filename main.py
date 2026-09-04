import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="낡은 집에서의 탈출 - 3D", layout="wide")

st.title("🏚️ 낡은 집에서의 탈출 (Old House Escape)")
st.caption("조작 방법 | W/S/A/D: 이동 | ← / → (방향키): 시점 회전 | E: 달리기 | 1,2,3,4: 아이템 사용 | 마우스 클릭: 공격")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #000; font-family: sans-serif; user-select: none; }
        #canvas { width: 100%; height: 530px; display: block; cursor: pointer; }
        
        #ui { position: absolute; top: 15px; left: 15px; color: white; text-shadow: 1px 1px 3px black; font-size: 14px; display: flex; flex-direction: column; gap: 8px; z-index: 5; pointer-events: none; }
        .bar-container { width: 180px; height: 16px; background: rgba(255,255,255,0.15); border: 2px solid #444; border-radius: 8px; overflow: hidden; }
        .bar-fill { height: 100%; width: 100%; transition: width 0.1s linear; }
        #hp-bar { background: linear-gradient(90deg, #cc0000, #ff4d4d); }
        #stamina-bar { background: linear-gradient(90deg, #28a745, #5cdb5c); }

        #inventory { position: absolute; bottom: 15px; right: 15px; display: flex; gap: 8px; z-index: 5; pointer-events: none; }
        .slot { width: 60px; height: 60px; border: 2px solid #444; background: rgba(0,0,0,0.85); color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; border-radius: 6px; text-align: center; }
        .slot-key { color: #ffcc00; font-size: 10px; margin-bottom: 2px; }

        #msg { position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); color: #ff3333; font-size: 26px; font-weight: bold; text-align: center; text-shadow: 2px 2px 5px black; z-index: 5; pointer-events: none; }
        #room-info { position: absolute; top: 15px; right: 15px; color: #aaa; font-size: 14px; text-align: right; z-index: 5; pointer-events: none; }

        #jumpscare {
            display: none;
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: #000;
            z-index: 99;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        #scare-face {
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, #ff0000 0%, #330000 70%, #000000 100%);
            border-radius: 50%;
            position: relative;
            box-shadow: 0 0 60px #ff0000;
            animation: shake 0.05s infinite alternate;
        }
        .eye { position: absolute; top: 35%; width: 65px; height: 65px; background: #fff; border-radius: 50%; box-shadow: inset 0 0 15px #000; }
        .eye.left { left: 20%; }
        .eye.right { right: 20%; }
        .pupil { position: absolute; top: 25%; left: 25%; width: 30px; height: 30px; background: #000; border-radius: 50%; box-shadow: 0 0 10px #ff0000; }
        .mouth { position: absolute; bottom: 15%; left: 20%; width: 60%; height: 80px; background: #000; border-radius: 0 0 50px 50px; border: 4px solid #880000; }
        #scare-text { color: #ff0000; font-size: 32px; font-weight: 900; margin-top: 20px; text-shadow: 0 0 10px #ff0000; }
        #restart-btn { margin-top: 15px; padding: 10px 20px; font-size: 16px; background: #333; color: white; border: 1px solid #777; cursor: pointer; border-radius: 5px; }
        #restart-btn:hover { background: #555; }

        @keyframes shake {
            0% { transform: translate(4px, 4px) scale(1.05); }
            100% { transform: translate(-4px, -4px) scale(1.1); }
        }
    </style>
</head>
<body>
    <div id="ui">
        <div>
            <span>체력</span>
            <div class="bar-container"><div id="hp-bar" class="bar-fill"></div></div>
        </div>
        <div>
            <span>스테미나 (E키 달리기)</span>
            <div class="bar-container"><div id="stamina-bar" class="bar-fill"></div></div>
        </div>
        <div>장착 무기: <span id="weapon" style="color:cyan;">맨손</span></div>
    </div>

    <div id="room-info">
        <div style="color:gold; font-weight:bold;">장소: 오래된 저택 복도</div>
        <div>목표: 열쇠를 찾아 탈출하라</div>
    </div>
    
    <div id="inventory">
        <div class="slot" id="slot1"><span class="slot-key">[1]</span>회복약<br><span id="cnt-potion">0</span></div>
        <div class="slot" id="slot2"><span class="slot-key">[2]</span>배터리<br><span id="cnt-battery">0</span></div>
        <div class="slot" id="slot3"><span class="slot-key">[3]</span>부적<br><span id="cnt-talisman">1</span></div>
        <div class="slot" id="slot4"><span class="slot-key">[4]</span>열쇠<br><span id="cnt-key">X</span></div>
    </div>

    <div id="msg">화면을 클릭하여 게임을 시작하세요</div>
    
    <div id="jumpscare">
        <div id="scare-face">
            <div class="eye left"><div class="pupil"></div></div>
            <div class="eye right"><div class="pupil"></div></div>
            <div class="mouth"></div>
        </div>
        <div id="scare-text">💀 원혼에게 붙잡혔습니다! 💀</div>
        <button id="restart-btn" onclick="resetGame()">다시 시도하기</button>
    </div>
    
    <canvas id="canvas"></canvas>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 530;

let houseMap = [];
let px = 7.5, py = 7.5;
let angle = 0;
let hp = 100;
let stamina = 100;
let flashRange = 10;
let gameOver = false;
let items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
let isAttacking = 0;
let ghosts = [];
let zBuffer = new Array(160).fill(0);

const initialMap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,7,0,10,1,8,0,0,1,9,0,11,4,0,1],
    [1,7,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,10,0,0,0,0,2,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,1,5,0,0,0,7,0,0,0,8,1,0,1],
    [1,0,1,0,11,0,0,7,0,10,0,0,1,0,1],
    [1,0,0,0,9,0,0,0,0,0,6,0,0,0,1],
    [1,0,1,0,0,0,0,8,0,0,0,11,1,0,1],
    [1,0,1,6,0,10,0,8,0,0,0,5,1,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,9,0,10,1,0,0,0,1,11,0,0,7,0,1],
    [1,0,0,0,1,3,1,0,1,0,0,0,7,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

function initGame() {
    houseMap = JSON.parse(JSON.stringify(initialMap));
    px = 7.5; py = 7.5;
    angle = 0;
    hp = 100;
    stamina = 100;
    flashRange = 10;
    gameOver = false;
    items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
    isAttacking = 0;
    ghosts = [
        { x: 1.5, y: 1.5, hp: 80, stun: 0 },
        { x: 13.5, y: 13.5, hp: 80, stun: 0 }
    ];
    document.getElementById('jumpscare').style.display = 'none';
    document.getElementById('msg').innerText = "화면을 클릭하여 게임을 시작하세요";
    document.getElementById('msg').style.color = "#ff3333";
    updateUI();
}

function resetGame() {
    initGame();
}

const keys = {};

function parseKey(k) {
    if (k === 'ArrowLeft') return 'left';
    if (k === 'ArrowRight') return 'right';
    k = k.toLowerCase();
    if (k === 'ㅈ') return 'w';
    if (k === 'ㄴ') return 's';
    if (k === 'ㅁ') return 'a';
    if (k === 'ㅇ') return 'd';
    if (k === 'ㄷ') return 'e';
    return k;
}

window.addEventListener('keydown', e => {
    let k = parseKey(e.key);
    keys[k] = true;
    
    if (!gameOver) {
        if (e.key === '1' && items.potion > 0) { 
            hp = Math.min(100, hp + 50); 
            items.potion--; 
            updateUI(); 
        }
        if (e.key === '2' && items.battery > 0) { 
            flashRange = 15; 
            items.battery--; 
            updateUI(); 
        }
        if (e.key === '3' && items.talisman > 0) { 
            ghosts.forEach(g => g.stun = 240); 
            items.talisman--; 
            updateUI(); 
        }
        if (e.key === '4' && items.key) {
            document.getElementById('msg').innerText = "🔑 열쇠 준비됨! 출구(탈출문)로 가세요.";
            setTimeout(() => { if (!gameOver) document.getElementById('msg').innerText = ""; }, 2500);
        }
    }
});

window.addEventListener('keyup', e => {
    let k = parseKey(e.key);
    keys[k] = false;
});

canvas.addEventListener('click', () => {
    window.focus();
    if (document.getElementById('msg').innerText.includes("클릭")) {
        document.getElementById('msg').innerText = "";
    }
    if (items.knife && isAttacking === 0 && !gameOver) {
        isAttacking = 10;
        checkAttackHit();
    }
});

function checkAttackHit() {
    ghosts.forEach(g => {
        if (g.hp <= 0) return;
        let gdx = g.x - px, gdy = g.y - py;
        let dist = Math.sqrt(gdx*gdx + gdy*gdy);
        let gAngle = Math.atan2(gdy, gdx) - angle;
        while (gAngle < -Math.PI) gAngle += 2 * Math.PI;
        while (gAngle > Math.PI) gAngle -= 2 * Math.PI;

        if (dist < 1.8 && Math.abs(gAngle) < 0.6) {
            g.hp -= 40;
            g.stun = 40;
        }
    });
}

function updateUI() {
    document.getElementById('hp-bar').style.width = Math.max(0, hp) + "%";
    document.getElementById('stamina-bar').style.width = Math.max(0, stamina) + "%";
    document.getElementById('weapon').innerText = items.knife ? "녹슨 단검 (클릭: 공격)" : "맨손";
    
    document.getElementById('cnt-potion').innerText = items.potion;
    document.getElementById('cnt-battery').innerText = items.battery;
    document.getElementById('cnt-talisman').innerText = items.talisman;
    document.getElementById('cnt-key').innerText = items.key ? "획득" : "미획득";

    document.getElementById('slot1').style.borderColor = items.potion > 0 ? "#00ff00" : "#444";
    document.getElementById('slot2').style.borderColor = items.battery > 0 ? "#ffff00" : "#444";
    document.getElementById('slot3').style.borderColor = items.talisman > 0 ? "#00ffff" : "#444";
    document.getElementById('slot4').style.borderColor = items.key ? "#ffd700" : "#444";
}

function isSolid(x, y) {
    if (x < 0 || x >= 15 || y < 0 || y >= 15) return true;
    let cell = houseMap[Math.floor(y)][Math.floor(x)];
    return cell === 1 || (cell >= 7 && cell <= 11);
}

function triggerJumpscare() {
    gameOver = true;
    document.getElementById('jumpscare').style.display = 'flex';
}

function update() {
    if (gameOver) return;

    const rotSpeed = 0.04;
    if (keys['left']) angle -= rotSpeed;
    if (keys['right']) angle += rotSpeed;

    let speed = 0.04;
    let isMoving = keys['w'] || keys['s'] || keys['a'] || keys['d'];

    if (keys['e'] && isMoving && stamina >= 0.5) {
        speed = 0.07;
        stamina = Math.max(0, stamina - 0.4);
    } else {
        stamina = Math.min(100, stamina + 0.15);
    }

    let dx = 0, dy = 0;
    if (keys['w']) { dx += Math.cos(angle) * speed; dy += Math.sin(angle) * speed; }
    if (keys['s']) { dx -= Math.cos(angle) * speed; dy -= Math.sin(angle) * speed; }
    if (keys['a']) { dx += Math.sin(angle) * speed; dy -= Math.cos(angle) * speed; }
    if (keys['d']) { dx -= Math.sin(angle) * speed; dy += Math.cos(angle) * speed; }

    const margin = 0.25;
    if (!isSolid(px + dx + Math.sign(dx)*margin, py)) px += dx;
    if (!isSolid(px, py + dy + Math.sign(dy)*margin)) py += dy;

    let ix = Math.floor(px), iy = Math.floor(py);
    let cell = houseMap[iy][ix];
    if (cell === 2) { items.key = true; houseMap[iy][ix] = 0; }
    else if (cell === 4) { items.knife = true; houseMap[iy][ix] = 0; }
    else if (cell === 5) { items.potion++; houseMap[iy][ix] = 0; }
    else if (cell === 6) { items.battery++; houseMap[iy][ix] = 0; }
    else if (cell === 3 && items.key) {
        gameOver = true;
        document.getElementById('msg').innerText = "🚪 낡은 집의 빗장을 풀고 탈출에 성공했습니다!";
        document.getElementById('msg').style.color = "gold";
    }
    updateUI();

    ghosts.forEach(g => {
        if (g.hp <= 0) return;
        if (g.stun > 0) {
            g.stun--;
        } else {
            let gdx = px - g.x, gdy = py - g.y;
            let dist = Math.sqrt(gdx*gdx + gdy*gdy);
            if (dist > 0.1) {
                g.x += (gdx / dist) * 0.008;
                g.y += (gdy / dist) * 0.008;
            }
            if (dist < 0.6) {
                hp -= 1.5;
                if (hp <= 0) triggerJumpscare();
            }
        }
    });

    if (isAttacking > 0) isAttacking--;
}

function renderMinimap() {
    const size = 6;
    const offsetX = 15;
    const offsetY = canvas.height - (15 * size) - 15;

    ctx.fillStyle = "rgba(0,0,0,0.5)";
    ctx.fillRect(offsetX - 2, offsetY - 2, 15 * size + 4, 15 * size + 4);

    for (let r = 0; r < 15; r++) {
        for (let c = 0; c < 15; c++) {
            if (houseMap[r][c] === 1) ctx.fillStyle = "#555";
            else if (houseMap[r][c] === 3) ctx.fillStyle = "gold";
            else ctx.fillStyle = "#111";
            ctx.fillRect(offsetX + c * size, offsetY + r * size, size - 1, size - 1);
        }
    }

    ctx.fillStyle = "red";
    ctx.beginPath();
    ctx.arc(offsetX + px * size, offsetY + py * size, 2.5, 0, Math.PI * 2);
    ctx.fill();
}

function render() {
    ctx.fillStyle = '#050403';
    ctx.fillRect(0, 0, canvas.width, canvas.height/2);
    ctx.fillStyle = '#0f0b07';
    ctx.fillRect(0, canvas.height/2, canvas.width, canvas.height/2);

    const fov = Math.PI / 3;
    const numRays = 160;
    const w = canvas.width / numRays;

    for (let i = 0; i < numRays; i++) {
        let rayAngle = (angle - fov / 2) + (i / numRays) * fov;
        let distance = 0;
        let hit = false;
        let hitType = 1;

        while (!hit && distance < flashRange) {
            distance += 0.03;
            let rx = px + Math.cos(rayAngle) * distance;
            let ry = py + Math.sin(rayAngle) * distance;
            let tx = Math.floor(rx);
            let ty = Math.floor(ry);

            if (tx < 0 || tx >= 15 || ty < 0 || ty >= 15) {
                hit = true; hitType = 1;
            } else if (isSolid(tx, ty)) {
                hit = true; hitType = houseMap[ty][tx];
            }
        }

        let correctedDist = distance * Math.cos(rayAngle - angle);
        zBuffer[i] = correctedDist;

        let h = Math.min(canvas.height, canvas.height / (correctedDist + 0.0001));
        let shade = Math.max(0, Math.floor(180 - correctedDist * (180 / flashRange)));

        let r = Math.floor(shade * 0.5);
        let g = Math.floor(shade * 0.25);
        let b = Math.floor(shade * 0.15);

        ctx.fillStyle = (hitType === 1) ? `rgb(${r}, ${g}, ${b})` : `rgb(${Math.floor(r*0.6)}, ${Math.floor(g*0.6)}, ${Math.floor(b*0.6)})`;
        let topY = (canvas.height - h) / 2;
        ctx.fillRect(i * w, topY, w + 1, h);
    }

    // 귀신 렌더링
    ghosts.forEach(g => {
        if (g.hp <= 0) return;
        let gdx = g.x - px, gdy = g.y - py;
        let gDist = Math.sqrt(gdx*gdx + gdy*gdy);
        let gAngle = Math.atan2(gdy, gdx) - angle;

        while (gAngle < -Math.PI) gAngle += 2 * Math.PI;
        while (gAngle > Math.PI) gAngle -= 2 * Math.PI;

        if (Math.abs(gAngle) < fov / 2 && gDist < flashRange) {
            let sx = (canvas.width / 2) + Math.tan(gAngle) * (canvas.width / 2);
            let rayIndex = Math.floor((sx / canvas.width) * numRays);
            
            if (rayIndex >= 0 && rayIndex < numRays && gDist < zBuffer[rayIndex]) {
                let size = Math.min(380, canvas.height / gDist);
                
                ctx.save();
                let topY = canvas.height / 2 - size / 2;
                ctx.fillStyle = g.stun > 0 ? '#1a3a3a' : '#0a0a0d';
                ctx.beginPath();
                ctx.arc(sx, topY + size/3, size/4, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = g.stun > 0 ? '#00ffff' : '#ff0000';
                ctx.shadowColor = g.stun > 0 ? '#00ffff' : '#ff0000';
                ctx.shadowBlur = 10;
                ctx.beginPath();
                ctx.arc(sx - size/12, topY + size/3, size/30, 0, Math.PI * 2);
                ctx.arc(sx + size/12, topY + size/3, size/30, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }
        }
    });

    if (items.knife) {
        ctx.save();
        let attackOffset = isAttacking * 8;
        ctx.fillStyle = '#aaa';
        ctx.beginPath();
        ctx.moveTo(canvas.width/2 + 80 - attackOffset, canvas.height - attackOffset);
        ctx.lineTo(canvas.width/2 + 130 - attackOffset, canvas.height - 120 - attackOffset);
        ctx.lineTo(canvas.width/2 + 150 - attackOffset, canvas.height - 100 - attackOffset);
        ctx.fill();
        ctx.restore();
    }

    renderMinimap();
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

components.html(game_html, height=560)
