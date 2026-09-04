import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="낡은 집에서의 탈출 - 수정판", layout="wide")

st.title("🏚️ 낡은 집에서의 탈출 (Old House Escape)")
st.caption("조작 방법 | W/A/S/D: 이동 | 방향키(←/→) 또는 마우스 드래그: 시점 회전 | E: 달리기 | 1,2,3: 아이템 사용 | 클릭: 공격")

fixed_game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #000; font-family: 'Courier New', monospace; user-select: none; }
        #canvas { width: 100%; height: 550px; display: block; cursor: grab; }
        #canvas:active { cursor: grabbing; }
        
        #ui { position: absolute; top: 15px; left: 15px; color: #e0e0e0; text-shadow: 2px 2px 4px #000; font-size: 13px; display: flex; flex-direction: column; gap: 8px; z-index: 5; pointer-events: none; }
        .bar-container { width: 200px; height: 14px; background: rgba(0,0,0,0.8); border: 1px solid #555; border-radius: 3px; overflow: hidden; }
        .bar-fill { height: 100%; width: 100%; transition: width 0.05s linear; }
        #hp-bar { background: linear-gradient(90deg, #800000, #ff0000); }
        #stamina-bar { background: linear-gradient(90deg, #1b5e20, #4caf50); }

        #inventory { position: absolute; bottom: 15px; right: 15px; display: flex; gap: 8px; z-index: 5; pointer-events: none; }
        .slot { width: 65px; height: 65px; border: 1px solid #444; background: rgba(10,10,10,0.85); color: #ccc; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 10px; border-radius: 4px; text-align: center; }
        .slot-key { color: #ffcc00; font-size: 10px; margin-bottom: 2px; font-weight: bold; }

        #msg { position: absolute; top: 35%; left: 50%; transform: translate(-50%, -50%); color: #ff2222; font-size: 20px; font-weight: bold; text-align: center; text-shadow: 0 0 8px #000; z-index: 5; pointer-events: none; }
        #room-info { position: absolute; top: 15px; right: 15px; color: #888; font-size: 12px; text-align: right; z-index: 5; pointer-events: none; }

        #glitch-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; z-index: 4; opacity: 0;
            background: repeating-linear-gradient(0deg, rgba(255,0,0,0.08), rgba(255,0,0,0.08) 2px, transparent 2px, transparent 4px);
        }

        #jumpscare {
            display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-color: #000; z-index: 99; flex-direction: column; justify-content: center; align-items: center;
        }
        #scare-face {
            width: 300px; height: 350px; background: radial-gradient(circle, #4a0000 0%, #1a0000 60%, #000000 100%);
            border-radius: 40% 40% 50% 50%; position: relative; box-shadow: 0 0 100px #ff0000;
            animation: violent-shake 0.03s infinite alternate;
        }
        .eye { position: absolute; top: 30%; width: 50px; height: 70px; background: #fff; border-radius: 50%; box-shadow: inset 0 0 20px #ff0000; }
        .eye.left { left: 22%; transform: rotate(-10deg); }
        .eye.right { right: 22%; transform: rotate(10deg); }
        .pupil { position: absolute; top: 35%; left: 35%; width: 12px; height: 12px; background: #000; border-radius: 50%; box-shadow: 0 0 8px #ff0000; }
        .mouth { position: absolute; bottom: 12%; left: 15%; width: 70%; height: 120px; background: #050000; border-radius: 10px 10px 60px 60px; border: 3px solid #600; overflow: hidden; }
        .teeth { width: 100%; height: 20px; background: repeating-linear-gradient(90deg, #ddd, #ddd 10px, #000 10px, #000 15px); }
        
        #scare-text { color: #ff0000; font-size: 26px; font-weight: 900; margin-top: 25px; text-shadow: 0 0 15px #ff0000; }
        #restart-btn { margin-top: 20px; padding: 12px 28px; font-size: 15px; background: #111; color: #ff4d4d; border: 1px solid #ff0000; cursor: pointer; border-radius: 3px; font-weight: bold; }
        #restart-btn:hover { background: #300; color: #fff; }

        @keyframes violent-shake {
            0% { transform: translate(5px, -5px) scale(1.05); }
            100% { transform: translate(-5px, 5px) scale(1.1); }
        }
    </style>
</head>
<body>
    <div id="glitch-overlay"></div>

    <div id="ui">
        <div>
            <span>생명력</span>
            <div class="bar-container"><div id="hp-bar" class="bar-fill"></div></div>
        </div>
        <div>
            <span>스테미나 (E: 달리기)</span>
            <div class="bar-container"><div id="stamina-bar" class="bar-fill"></div></div>
        </div>
        <div>무기: <span id="weapon" style="color:#ffcc00;">맨손</span></div>
    </div>

    <div id="room-info">
        <div style="color:#ff4d4d; font-weight:bold;">구역: 저주받은 저택</div>
        <div>목표: 황금색 탈출문을 찾아 탈출하라</div>
    </div>
    
    <div id="inventory">
        <div class="slot" id="slot1"><span class="slot-key">[1]</span>회복약<br><span id="cnt-potion">0</span></div>
        <div class="slot" id="slot2"><span class="slot-key">[2]</span>배터리<br><span id="cnt-battery">0</span></div>
        <div class="slot" id="slot3"><span class="slot-key">[3]</span>퇴마부적<br><span id="cnt-talisman">1</span></div>
        <div class="slot" id="slot4"><span class="slot-key">[4]</span>탈출열쇠<br><span id="cnt-key">미획득</span></div>
    </div>

    <div id="msg">키보드 방향키(←/→) 또는 마우스 드래그로 화면을 돌리세요</div>
    
    <div id="jumpscare">
        <div id="scare-face">
            <div class="eye left"><div class="pupil"></div></div>
            <div class="eye right"><div class="pupil"></div></div>
            <div class="mouth"><div class="teeth"></div></div>
        </div>
        <div id="scare-text">당신의 영혼이 저택에 귀속되었습니다...</div>
        <button id="restart-btn" onclick="resetGame()">다시 도전하기</button>
    </div>
    
    <canvas id="canvas"></canvas>

<script>
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function initAudio() {
    if (!audioCtx) audioCtx = new AudioContext();
}

function playSound(type) {
    if (!audioCtx) return;
    const now = audioCtx.currentTime;

    if (type === 'attack') {
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.exponentialRampToValueAtTime(40, now + 0.12);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.12);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.12);
    } else if (type === 'hit') {
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'square';
        osc.frequency.setValueAtTime(90, now);
        osc.frequency.exponentialRampToValueAtTime(20, now + 0.18);
        gain.gain.setValueAtTime(0.4, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.18);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.18);
    } else if (type === 'item') {
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.exponentialRampToValueAtTime(880, now + 0.15);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.15);
    } else if (type === 'jumpscare') {
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(200, now);
        osc.frequency.linearRampToValueAtTime(800, now + 0.1);
        osc.frequency.linearRampToValueAtTime(100, now + 0.8);
        gain.gain.setValueAtTime(0.7, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.8);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.8);
    }
}

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 550;

let houseMap = [];
let px = 7.5, py = 7.5;
let angle = 0;
let hp = 100;
let stamina = 100;
let flashRange = 8;
let gameOver = false;
let items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
let isAttacking = 0;
let ghosts = [];
let worldItems = [];
let zBuffer = new Array(160).fill(0);
let screenShake = 0;

const initialMap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,3,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

function initGame() {
    houseMap = JSON.parse(JSON.stringify(initialMap));
    px = 7.5; py = 7.5;
    angle = 0;
    hp = 100;
    stamina = 100;
    flashRange = 8;
    gameOver = false;
    items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
    isAttacking = 0;

    ghosts = [
        { x: 1.5, y: 1.5, hp: 100, stun: 0 },
        { x: 13.5, y: 13.5, hp: 100, stun: 0 }
    ];

    worldItems = [
        { x: 1.5, y: 12.5, type: 'key', name: '열쇠', color: '#ffd700' },
        { x: 13.5, y: 1.5, type: 'knife', name: '단검', color: '#aaaaaa' },
        { x: 3.5, y: 3.5, type: 'potion', name: '포션', color: '#ff3333' },
        { x: 11.5, y: 11.5, type: 'battery', name: '배터리', color: '#33ff33' }
    ];

    document.getElementById('jumpscare').style.display = 'none';
    document.getElementById('msg').innerText = "방향키(←/→) 또는 마우스 드래그로 시점을 돌리세요";
    document.getElementById('msg').style.color = "#ff2222";
    updateUI();
}

function resetGame() { initGame(); }

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
            hp = Math.min(100, hp + 60); items.potion--; 
            playSound('item'); showTmpMsg("💊 체력을 회복했습니다."); updateUI(); 
        }
        if (e.key === '2' && items.battery > 0) { 
            flashRange = 13; items.battery--; 
            playSound('item'); showTmpMsg("🔋 시야 범위가 확충되었습니다."); updateUI(); 
        }
        if (e.key === '3' && items.talisman > 0) { 
            ghosts.forEach(g => { g.stun = 200; g.x += (g.x - px); g.y += (g.y - py); }); 
            items.talisman--; playSound('item'); screenShake = 12;
            showTmpMsg("📜 퇴마 부적으로 원혼을 격퇴했습니다!"); updateUI(); 
        }
    }
});

window.addEventListener('keyup', e => { keys[parseKey(e.key)] = false; });

// 마우스 드래그 및 포인터 회전 통합
let isMouseDown = false;
let lastMouseX = 0;

canvas.addEventListener('mousedown', e => {
    initAudio();
    isMouseDown = true;
    lastMouseX = e.clientX;
    
    canvas.requestPointerLock = canvas.requestPointerLock || canvas.mozRequestPointerLock;
    if (canvas.requestPointerLock) canvas.requestPointerLock();

    if (items.knife && isAttacking === 0 && !gameOver) {
        isAttacking = 8;
        playSound('attack');
        checkAttackHit();
    }
});

window.addEventListener('mouseup', () => { isMouseDown = false; });

document.addEventListener('mousemove', e => {
    if (document.pointerLockElement === canvas || document.mozPointerLockElement === canvas) {
        angle += e.movementX * 0.004;
    } else if (isMouseDown) {
        let dx = e.clientX - lastMouseX;
        angle += dx * 0.005;
        lastMouseX = e.clientX;
    }
});

function showTmpMsg(txt) {
    let msgEl = document.getElementById('msg');
    msgEl.innerText = txt;
    setTimeout(() => { if (!gameOver && msgEl.innerText === txt) msgEl.innerText = ""; }, 2500);
}

function checkAttackHit() {
    ghosts.forEach(g => {
        if (g.hp <= 0) return;
        let gdx = g.x - px, gdy = g.y - py;
        let dist = Math.sqrt(gdx*gdx + gdy*gdy);
        let gAngle = Math.atan2(gdy, gdx) - angle;
        while (gAngle < -Math.PI) gAngle += 2 * Math.PI;
        while (gAngle > Math.PI) gAngle -= 2 * Math.PI;

        if (dist < 1.8 && Math.abs(gAngle) < 0.6) {
            g.hp -= 50; g.stun = 40; playSound('hit'); screenShake = 8;
            if (g.hp <= 0) showTmpMsg("💀 원혼을 소멸시켰습니다!");
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
    document.getElementById('cnt-key').innerText = items.key ? "획득완료" : "미획득";
}

function isSolid(x, y) {
    if (x < 0 || x >= 15 || y < 0 || y >= 15) return true;
    return houseMap[Math.floor(y)][Math.floor(x)] === 1;
}

function triggerJumpscare() {
    gameOver = true;
    playSound('jumpscare');
    document.getElementById('jumpscare').style.display = 'flex';
}

function update() {
    if (gameOver) return;
    if (screenShake > 0) screenShake--;

    // 키보드 회전 조작 추가
    if (keys['left']) angle -= 0.04;
    if (keys['right']) angle += 0.04;

    let speed = keys['e'] && stamina >= 0.5 ? 0.065 : 0.038;
    if (keys['e'] && (keys['w']||keys['s']||keys['a']||keys['d'])) stamina = Math.max(0, stamina - 0.4);
    else stamina = Math.min(100, stamina + 0.2);

    let dx = 0, dy = 0;
    if (keys['w']) { dx += Math.cos(angle) * speed; dy += Math.sin(angle) * speed; }
    if (keys['s']) { dx -= Math.cos(angle) * speed; dy -= Math.sin(angle) * speed; }
    if (keys['a']) { dx += Math.sin(angle) * speed; dy -= Math.cos(angle) * speed; }
    if (keys['d']) { dx -= Math.sin(angle) * speed; dy += Math.cos(angle) * speed; }

    const margin = 0.2;
    if (!isSolid(px + dx + Math.sign(dx)*margin, py)) px += dx;
    if (!isSolid(px, py + dy + Math.sign(dy)*margin)) py += dy;

    // 아이템 습득 판정
    worldItems.forEach((item, idx) => {
        let dist = Math.sqrt((px - item.x)**2 + (py - item.y)**2);
        if (dist < 0.7) {
            playSound('item');
            if (item.type === 'key') { items.key = true; showTmpMsg("🔑 탈출 열쇠를 얻었습니다!"); }
            if (item.type === 'knife') { items.knife = true; showTmpMsg("🗡️ 녹슨 단검을 얻었습니다."); }
            if (item.type === 'potion') { items.potion++; showTmpMsg("💊 회복약을 얻었습니다."); }
            if (item.type === 'battery') { items.battery++; showTmpMsg("🔋 배터리를 얻었습니다."); }
            worldItems.splice(idx, 1);
            updateUI();
        }
    });

    // 탈출문 판정
    if (houseMap[Math.floor(py)][Math.floor(px)] === 3) {
        if (items.key) {
            gameOver = true;
            document.getElementById('msg').innerText = "🚪 열쇠로 문을 열고 저택에서 탈출했습니다!";
            document.getElementById('msg').style.color = "gold";
        } else {
            showTmpMsg("🔒 문이 잠겨 있습니다. 열쇠를 찾으세요.");
        }
    }

    // 적 추적 AI
    ghosts.forEach(g => {
        if (g.hp <= 0) return;
        let gdx = px - g.x, gdy = py - g.y;
        let dist = Math.sqrt(gdx*gdx + gdy*gdy);

        if (g.stun > 0) {
            g.stun--;
        } else {
            if (dist > 0.1) {
                let moveX = (gdx / dist) * 0.015;
                let moveY = (gdy / dist) * 0.015;
                if (!isSolid(g.x + moveX, g.y)) g.x += moveX;
                if (!isSolid(g.x, g.y + moveY)) g.y += moveY;
            }
            if (dist < 0.6) {
                hp -= 1.8; screenShake = 4;
                if (hp <= 0) triggerJumpscare();
            }
        }
    });

    if (isAttacking > 0) isAttacking--;
}

function render() {
    ctx.save();
    if (screenShake > 0) {
        ctx.translate((Math.random() - 0.5) * screenShake, (Math.random() - 0.5) * screenShake);
    }

    ctx.fillStyle = "#020202"; ctx.fillRect(0, 0, canvas.width, canvas.height/2);
    ctx.fillStyle = "#080404"; ctx.fillRect(0, canvas.height/2, canvas.width, canvas.height/2);

    const fov = Math.PI / 3;
    const numRays = 160;
    const w = canvas.width / numRays;
    let curFlashRange = flashRange + (Math.random() - 0.5) * 0.2;

    // 1. 벽면 렌더링
    for (let i = 0; i < numRays; i++) {
        let rayAngle = (angle - fov / 2) + (i / numRays) * fov;
        let distance = 0;
        let hit = false;
        let hitType = 1;

        while (!hit && distance < curFlashRange) {
            distance += 0.03;
            let rx = px + Math.cos(rayAngle) * distance;
            let ry = py + Math.sin(rayAngle) * distance;
            let tx = Math.floor(rx), ty = Math.floor(ry);

            if (tx < 0 || tx >= 15 || ty < 0 || ty >= 15) { hit = true; hitType = 1; } 
            else if (houseMap[ty][tx] > 0) { hit = true; hitType = houseMap[ty][tx]; }
        }

        let correctedDist = distance * Math.cos(rayAngle - angle);
        zBuffer[i] = correctedDist;

        let h = Math.min(canvas.height, canvas.height / (correctedDist + 0.0001));
        let shade = Math.max(0, Math.floor(180 - correctedDist * (180 / curFlashRange)));

        if (hitType === 3) ctx.fillStyle = `rgb(${shade}, ${Math.floor(shade*0.8)}, 0)`;
        else ctx.fillStyle = `rgb(${Math.floor(shade*0.5)}, ${Math.floor(shade*0.15)}, ${Math.floor(shade*0.1)})`;

        ctx.fillRect(i * w, (canvas.height - h) / 2, w + 1, h);
    }

    // 2. 아이템 3D 그래픽 객체 직접 구현
    worldItems.forEach(item => {
        let idxX = item.x - px, idxY = item.y - py;
        let dist = Math.sqrt(idxX*idxX + idxY*idxY);
        let itemAngle = Math.atan2(idxY, idxX) - angle;
        while (itemAngle < -Math.PI) itemAngle += 2 * Math.PI;
        while (itemAngle > Math.PI) itemAngle -= 2 * Math.PI;

        if (Math.abs(itemAngle) < fov / 2 && dist < curFlashRange) {
            let sx = (canvas.width / 2) + Math.tan(itemAngle) * (canvas.width / 2);
            let rayIndex = Math.floor((sx / canvas.width) * numRays);
            
            if (rayIndex >= 0 && rayIndex < numRays && dist < zBuffer[rayIndex]) {
                let size = Math.min(80, 120 / dist);
                let centerY = canvas.height / 2 + size;

                ctx.save();
                // 후광 효과
                ctx.fillStyle = item.color;
                ctx.shadowColor = item.color;
                ctx.shadowBlur = 15;
                ctx.beginPath();
                ctx.arc(sx, centerY, size/3, 0, Math.PI * 2);
                ctx.fill();

                // 아이템 텍스트 표기
                ctx.fillStyle = "#ffffff";
                ctx.font = `bold ${Math.max(10, Math.floor(size/2))}px sans-serif`;
                ctx.textAlign = "center";
                ctx.fillText(item.name, sx, centerY - size/2);
                ctx.restore();
            }
        }
    });

    // 3. 원혼 렌더링
    ghosts.forEach(g => {
        if (g.hp <= 0) return;
        let gdx = g.x - px, gdy = g.y - py;
        let gDist = Math.sqrt(gdx*gdx + gdy*gdy);
        let gAngle = Math.atan2(gdy, gdx) - angle;
        while (gAngle < -Math.PI) gAngle += 2 * Math.PI;
        while (gAngle > Math.PI) gAngle -= 2 * Math.PI;

        if (Math.abs(gAngle) < fov / 2 && gDist < curFlashRange) {
            let sx = (canvas.width / 2) + Math.tan(gAngle) * (canvas.width / 2);
            let rayIndex = Math.floor((sx / canvas.width) * numRays);
            
            if (rayIndex >= 0 && rayIndex < numRays && gDist < zBuffer[rayIndex]) {
                let size = Math.min(400, canvas.height / gDist);
                let topY = canvas.height / 2 - size / 2;
                
                ctx.save();
                ctx.fillStyle = g.stun > 0 ? '#00ffff' : '#0a0002';
                ctx.beginPath();
                ctx.ellipse(sx, topY + size/2, size/5, size/2.5, 0, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = g.stun > 0 ? '#ffffff' : '#ff0000';
                ctx.shadowColor = '#ff0000'; ctx.shadowBlur = 10;
                ctx.beginPath();
                ctx.arc(sx - size/12, topY + size/3, size/25, 0, Math.PI * 2);
                ctx.arc(sx + size/12, topY + size/3, size/25, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }
        }
    });

    // 4. 무기 렌더링
    if (items.knife) {
        ctx.save();
        let attackOffset = isAttacking * 10;
        ctx.fillStyle = '#aaa';
        ctx.beginPath();
        ctx.moveTo(canvas.width/2 + 80 - attackOffset, canvas.height - attackOffset);
        ctx.lineTo(canvas.width/2 + 140 - attackOffset, canvas.height - 130 - attackOffset);
        ctx.lineTo(canvas.width/2 + 160 - attackOffset, canvas.height - 100 - attackOffset);
        ctx.closePath();
        ctx.fill();
        ctx.restore();
    }

    ctx.restore();
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

components.html(fixed_game_html, height=580)
