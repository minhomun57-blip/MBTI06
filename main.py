import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="🏚️ 저주받은 저택 - 호러 에디션", layout="wide")

st.title("🏚️ 저주받은 저택의 비밀 (Wide Vision Edition)")
st.caption("조작 방법 | W/A/S/D: 이동 | 방향키(←/→) 또는 마우스 드래그: 시점 회전 | E: 달리기 | 1,2,3: 아이템 사용 | 클릭: 무기 공격")

horror_game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #000; font-family: 'Courier New', monospace; user-select: none; }
        #canvas { width: 100%; height: 580px; display: block; cursor: grab; }
        #canvas:active { cursor: grabbing; }
        
        #ui { position: absolute; top: 15px; left: 15px; color: #d0d0d0; text-shadow: 2px 2px 5px #000; font-size: 13px; display: flex; flex-direction: column; gap: 8px; z-index: 5; pointer-events: none; }
        .bar-container { width: 220px; height: 12px; background: rgba(0,0,0,0.9); border: 1px solid #444; border-radius: 2px; overflow: hidden; }
        .bar-fill { height: 100%; width: 100%; transition: width 0.05s linear; }
        #hp-bar { background: linear-gradient(90deg, #500, #ff0000); }
        #stamina-bar { background: linear-gradient(90deg, #050, #00ff44); }

        #inventory { position: absolute; bottom: 15px; right: 15px; display: flex; gap: 8px; z-index: 5; pointer-events: none; }
        .slot { width: 65px; height: 65px; border: 1px solid #333; background: rgba(5,5,5,0.9); color: #aaa; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 10px; border-radius: 3px; text-align: center; }
        .slot-key { color: #ffaa00; font-size: 10px; margin-bottom: 2px; font-weight: bold; }

        #msg { position: absolute; top: 30%; left: 50%; transform: translate(-50%, -50%); color: #ff1111; font-size: 22px; font-weight: bold; text-align: center; text-shadow: 0 0 10px #000; z-index: 5; pointer-events: none; letter-spacing: 2px; }
        #room-info { position: absolute; top: 15px; right: 15px; color: #777; font-size: 11px; text-align: right; z-index: 5; pointer-events: none; }

        #glitch-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; z-index: 4; opacity: 0;
            background: repeating-linear-gradient(0deg, rgba(255,0,0,0.12), rgba(255,0,0,0.12) 2px, transparent 2px, transparent 4px);
        }

        #jumpscare {
            display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-color: #000; z-index: 99; flex-direction: column; justify-content: center; align-items: center;
        }
        #scare-face {
            width: 320px; height: 380px; background: radial-gradient(circle, #600 0%, #100 60%, #000 100%);
            border-radius: 40% 40% 50% 50%; position: relative; box-shadow: 0 0 120px #f00;
            animation: violent-shake 0.02s infinite alternate;
        }
        .eye { position: absolute; top: 28%; width: 55px; height: 75px; background: #fff; border-radius: 50%; box-shadow: inset 0 0 25px #f00; }
        .eye.left { left: 20%; transform: rotate(-12deg); }
        .eye.right { right: 20%; transform: rotate(12deg); }
        .pupil { position: absolute; top: 35%; left: 35%; width: 10px; height: 10px; background: #000; border-radius: 50%; box-shadow: 0 0 10px #f00; }
        .mouth { position: absolute; bottom: 10%; left: 12%; width: 76%; height: 130px; background: #000; border-radius: 10px 10px 60px 60px; border: 3px solid #800; overflow: hidden; }
        .teeth { width: 100%; height: 25px; background: repeating-linear-gradient(90deg, #ccc, #ccc 12px, #000 12px, #000 18px); }
        
        #scare-text { color: #ff0000; font-size: 28px; font-weight: 900; margin-top: 30px; text-shadow: 0 0 20px #ff0000; letter-spacing: 3px; }
        #restart-btn { margin-top: 25px; padding: 12px 32px; font-size: 15px; background: #050505; color: #ff3333; border: 1px solid #ff0000; cursor: pointer; font-weight: bold; }
        #restart-btn:hover { background: #300; color: #fff; }

        @keyframes violent-shake {
            0% { transform: translate(6px, -6px) scale(1.05); }
            100% { transform: translate(-6px, 6px) scale(1.12); }
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
        <div style="color:#ff3333; font-weight:bold;">구역: 심연의 미로</div>
        <div>목표: 피묻은 열쇠를 찾아 황금문으로 탈출하라</div>
    </div>
    
    <div id="inventory">
        <div class="slot" id="slot1"><span class="slot-key">[1]</span>회복약<br><span id="cnt-potion">0</span></div>
        <div class="slot" id="slot2"><span class="slot-key">[2]</span>배터리<br><span id="cnt-battery">0</span></div>
        <div class="slot" id="slot3"><span class="slot-key">[3]</span>퇴마부적<br><span id="cnt-talisman">1</span></div>
        <div class="slot" id="slot4"><span class="slot-key">[4]</span>탈출열쇠<br><span id="cnt-key">미획득</span></div>
    </div>

    <div id="msg">방향키(←/→) 또는 드래그로 시점을 조절하세요</div>
    
    <div id="jumpscare">
        <div id="scare-face">
            <div class="eye left"><div class="pupil"></div></div>
            <div class="eye right"><div class="pupil"></div></div>
            <div class="mouth"><div class="teeth"></div></div>
        </div>
        <div id="scare-text">당신의 영혼은 이제 저택의 일부입니다...</div>
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
        osc.frequency.setValueAtTime(140, now);
        osc.frequency.exponentialRampToValueAtTime(30, now + 0.15);
        gain.gain.setValueAtTime(0.4, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.15);
    } else if (type === 'hit') {
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'square';
        osc.frequency.setValueAtTime(80, now);
        osc.frequency.exponentialRampToValueAtTime(15, now + 0.2);
        gain.gain.setValueAtTime(0.5, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.2);
    } else if (type === 'item') {
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(520, now);
        osc.frequency.exponentialRampToValueAtTime(1040, now + 0.18);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.18);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.18);
    } else if (type === 'jumpscare') {
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(180, now);
        osc.frequency.linearRampToValueAtTime(900, now + 0.1);
        osc.frequency.linearRampToValueAtTime(80, now + 0.9);
        gain.gain.setValueAtTime(0.8, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.9);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.9);
    }
}

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 580;

// 절차적 벽면 텍스처
const texCanvas = document.createElement('canvas');
texCanvas.width = 64; texCanvas.height = 64;
const texCtx = texCanvas.getContext('2d');
texCtx.fillStyle = '#1c0f0d'; texCtx.fillRect(0,0,64,64);
texCtx.fillStyle = '#0f0706';
for(let i=0; i<64; i+=16) {
    texCtx.fillRect(0, i, 64, 2);
    for(let j=0; j<64; j+=16) {
        let offset = (i/16)%2 === 0 ? 0 : 8;
        texCtx.fillRect(j+offset, i, 2, 16);
    }
}
for(let i=0; i<80; i++) {
    texCtx.fillStyle = `rgba(0,0,0,${Math.random()*0.4})`;
    texCtx.fillRect(Math.random()*64, Math.random()*64, 3, 3);
}

let houseMap = [];
let MAP_SIZE = 21;
let px = 1.5, py = 1.5;
let angle = 0;
let hp = 100;
let stamina = 100;
let flashRange = 9;
let gameOver = false;
let items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
let isAttacking = 0;
let ghosts = [];
let worldItems = [];
let zBuffer = new Array(160).fill(0);
let screenShake = 0;
let animTimer = 0;

// FOV 넓힘 (약 75도 설정으로 답답함 제거)
const fov = Math.PI * 0.42; 

const initialMap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1],
    [1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

function initGame() {
    houseMap = JSON.parse(JSON.stringify(initialMap));
    MAP_SIZE = houseMap.length;
    px = 1.5; py = 1.5;
    angle = 0;
    hp = 100;
    stamina = 100;
    flashRange = 9;
    gameOver = false;
    items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
    isAttacking = 0;

    ghosts = [
        { x: 9.5, y: 9.5, hp: 100, stun: 0 },
        { x: 17.5, y: 3.5, hp: 100, stun: 0 },
        { x: 3.5, y: 17.5, hp: 100, stun: 0 }
    ];

    worldItems = [
        { x: 19.5, y: 1.5, type: 'key', name: '피묻은 열쇠' },
        { x: 1.5, y: 19.5, type: 'knife', name: '녹슨 단검' },
        { x: 9.5, y: 1.5, type: 'potion', name: '의용 회복제' },
        { x: 11.5, y: 17.5, type: 'battery', name: '고전압 배터리' }
    ];

    document.getElementById('jumpscare').style.display = 'none';
    document.getElementById('msg').innerText = "방향키(←/→) 또는 드래그로 시점을 회전하세요";
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
            flashRange = 14; items.battery--; 
            playSound('item'); showTmpMsg("🔋 손전등 출력이 강화되었습니다."); updateUI(); 
        }
        if (e.key === '3' && items.talisman > 0) { 
            ghosts.forEach(g => { g.stun = 200; g.x += (g.x - px)*0.5; g.y += (g.y - py)*0.5; }); 
            items.talisman--; playSound('item'); screenShake = 12;
            showTmpMsg("📜 부적으로 주변의 원혼을 퇴마했습니다!"); updateUI(); 
        }
    }
});

window.addEventListener('keyup', e => { keys[parseKey(e.key)] = false; });

let isMouseDown = false;
let lastMouseX = 0;

canvas.addEventListener('mousedown', e => {
    initAudio();
    isMouseDown = true;
    lastMouseX = e.clientX;
    
    if (items.knife && isAttacking === 0 && !gameOver) {
        isAttacking = 10;
        playSound('attack');
        checkAttackHit();
    }
});

window.addEventListener('mouseup', () => { isMouseDown = false; });

document.addEventListener('mousemove', e => {
    if (isMouseDown) {
        let dx = e.clientX - lastMouseX;
        angle += dx * 0.006;
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

        if (dist < 2.0 && Math.abs(gAngle) < 0.7) {
            g.hp -= 50; g.stun = 50; playSound('hit'); screenShake = 8;
            if (g.hp <= 0) showTmpMsg("💀 원혼을 성불시켰습니다!");
        }
    });
}

function updateUI() {
    document.getElementById('hp-bar').style.width = Math.max(0, hp) + "%";
    document.getElementById('stamina-bar').style.width = Math.max(0, stamina) + "%";
    document.getElementById('weapon').innerText = items.knife ? "녹슨 단검 (클릭: 베기)" : "맨손";
    
    document.getElementById('cnt-potion').innerText = items.potion;
    document.getElementById('cnt-battery').innerText = items.battery;
    document.getElementById('cnt-talisman').innerText = items.talisman;
    document.getElementById('cnt-key').innerText = items.key ? "획득완료" : "미획득";
}

function isSolid(x, y) {
    if (x < 0 || x >= MAP_SIZE || y < 0 || y >= MAP_SIZE) return true;
    return houseMap[Math.floor(y)][Math.floor(x)] === 1;
}

function triggerJumpscare() {
    gameOver = true;
    playSound('jumpscare');
    document.getElementById('jumpscare').style.display = 'flex';
}

function update() {
    if (gameOver) return;
    animTimer += 0.05;
    if (screenShake > 0) screenShake--;

    if (keys['left']) angle -= 0.045;
    if (keys['right']) angle += 0.045;

    let speed = keys['e'] && stamina >= 0.5 ? 0.065 : 0.038;
    if (keys['e'] && (keys['w']||keys['s']||keys['a']||keys['d'])) stamina = Math.max(0, stamina - 0.4);
    else stamina = Math.min(100, stamina + 0.2);

    let dx = 0, dy = 0;
    if (keys['w']) { dx += Math.cos(angle) * speed; dy += Math.sin(angle) * speed; }
    if (keys['s']) { dx -= Math.cos(angle) * speed; dy -= Math.sin(angle) * speed; }
    if (keys['a']) { dx += Math.sin(angle) * speed; dy -= Math.cos(angle) * speed; }
    if (keys['d']) { dx -= Math.sin(angle) * speed; dy += Math.cos(angle) * speed; }

    const margin = 0.25;
    if (!isSolid(px + dx + Math.sign(dx)*margin, py)) px += dx;
    if (!isSolid(px, py + dy + Math.sign(dy)*margin)) py += dy;

    // 아이템 습득 판정
    worldItems.forEach((item, idx) => {
        let dist = Math.sqrt((px - item.x)**2 + (py - item.y)**2);
        if (dist < 0.7) {
            playSound('item');
            if (item.type === 'key') { items.key = true; showTmpMsg("🔑 피묻은 열쇠를 습득했습니다! 탈출문(황금색)을 찾으세요."); }
            if (item.type === 'knife') { items.knife = true; showTmpMsg("🗡️ 녹슨 단검을 습득했습니다."); }
            if (item.type === 'potion') { items.potion++; showTmpMsg("💊 의용 회복제를 습득했습니다."); }
            if (item.type === 'battery') { items.battery++; showTmpMsg("🔋 배터리를 습득했습니다."); }
            worldItems.splice(idx, 1);
            updateUI();
        }
    });

    // 탈출문 판정
    if (houseMap[Math.floor(py)][Math.floor(px)] === 3) {
        if (items.key) {
            gameOver = true;
            document.getElementById('msg').innerText = "🚪 열쇠로 잠긴 문을 열고 탈출에 성공했습니다!";
            document.getElementById('msg').style.color = "gold";
        } else {
            showTmpMsg("🔒 문이 굳게 잠겨 있습니다. 피묻은 열쇠가 필요합니다.");
        }
    }

    // 적 추적 AI
    let minDist = 999;
    ghosts.forEach(g => {
        if (g.hp <= 0) return;
        let gdx = px - g.x, gdy = py - g.y;
        let dist = Math.sqrt(gdx*gdx + gdy*gdy);
        if (dist < minDist) minDist = dist;

        if (g.stun > 0) {
            g.stun--;
        } else {
            if (dist > 0.1) {
                let moveX = (gdx / dist) * 0.018;
                let moveY = (gdy / dist) * 0.018;
                if (!isSolid(g.x + moveX, g.y)) g.x += moveX;
                if (!isSolid(g.x, g.y + moveY)) g.y += moveY;
            }
            if (dist < 0.6) {
                hp -= 2.0; screenShake = 5;
                if (hp <= 0) triggerJumpscare();
            }
        }
    });

    if (minDist < 5.5) {
        document.getElementById('glitch-overlay').style.opacity = (5.5 - minDist) / 5.5 * 0.75;
    } else {
        document.getElementById('glitch-overlay').style.opacity = 0;
    }

    if (isAttacking > 0) isAttacking--;
}

// 아이템 형태별 3D 드로잉 함수
function drawCustomItem(type, sx, sy, size) {
    ctx.save();
    ctx.translate(sx, sy);

    if (type === 'key') {
        // 황금 열쇠 형태
        ctx.strokeStyle = '#ffd700';
        ctx.fillStyle = '#ffaa00';
        ctx.lineWidth = Math.max(2, size/12);

        // 열쇠 손잡이 (고리)
        ctx.beginPath();
        ctx.arc(0, -size/3, size/4, 0, Math.PI * 2);
        ctx.stroke();

        // 열쇠 대
        ctx.beginPath();
        ctx.moveTo(0, -size/12);
        ctx.lineTo(0, size/2);
        ctx.stroke();

        // 열쇠 톱니
        ctx.beginPath();
        ctx.moveTo(0, size/3);
        ctx.lineTo(size/4, size/3);
        ctx.moveTo(0, size/2);
        ctx.lineTo(size/4, size/2);
        ctx.stroke();

    } else if (type === 'knife') {
        // 단검 형태
        ctx.fillStyle = '#cccccc';
        ctx.strokeStyle = '#555555';
        ctx.lineWidth = 1;

        // 칼날
        ctx.beginPath();
        ctx.moveTo(0, -size/2);
        ctx.lineTo(size/6, size/6);
        ctx.lineTo(-size/6, size/6);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        // 코등이 & 손잡이
        ctx.fillStyle = '#8B4513';
        ctx.fillRect(-size/4, size/6, size/2, size/10);
        ctx.fillRect(-size/12, size/6 + size/10, size/6, size/3);

    } else if (type === 'potion') {
        // 포션 병 형태
        ctx.fillStyle = 'rgba(255, 30, 30, 0.85)';
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5;

        // 병 몸통
        ctx.beginPath();
        ctx.arc(0, size/6, size/3, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        // 병 목 & 마개
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(-size/8, -size/4, size/4, size/4);
        ctx.fillStyle = '#8B4513';
        ctx.fillRect(-size/6, -size/3, size/3, size/10);

    } else if (type === 'battery') {
        // 배터리 형태
        ctx.fillStyle = '#00ff44';
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5;

        // 본체
        ctx.fillRect(-size/4, -size/3, size/2, size/1.5);
        ctx.strokeRect(-size/4, -size/3, size/2, size/1.5);

        // 양극 (+) 돌기
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(-size/8, -size/2, size/4, size/6);

        // 플러스 기호
        ctx.fillStyle = '#000000';
        ctx.font = `bold ${Math.max(10, Math.floor(size/3))}px sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('+', 0, 0);
    }

    ctx.restore();
}

function render() {
    ctx.save();
    if (screenShake > 0) {
        ctx.translate((Math.random() - 0.5) * screenShake, (Math.random() - 0.5) * screenShake);
    }

    // 천장 & 바닥
    let ceilGrd = ctx.createLinearGradient(0, 0, 0, canvas.height/2);
    ceilGrd.addColorStop(0, '#000000'); ceilGrd.addColorStop(1, '#080202');
    ctx.fillStyle = ceilGrd; ctx.fillRect(0, 0, canvas.width, canvas.height/2);

    let floorGrd = ctx.createLinearGradient(0, canvas.height/2, 0, canvas.height);
    floorGrd.addColorStop(0, '#050202'); floorGrd.addColorStop(1, '#000000');
    ctx.fillStyle = floorGrd; ctx.fillRect(0, canvas.height/2, canvas.width, canvas.height/2);

    const numRays = 160;
    const w = canvas.width / numRays;
    let curFlashRange = flashRange + (Math.random() - 0.5) * 0.35;

    // Projection Distance 계산 (넓은 FOV 지원)
    let projDist = (canvas.width / 2) / Math.tan(fov / 2);

    // 1. 레이캐스팅 벽면 렌더링
    for (let i = 0; i < numRays; i++) {
        let rayAngle = (angle - fov / 2) + (i / numRays) * fov;
        let distance = 0;
        let hit = false;
        let hitType = 1;
        let wallX = 0;

        while (!hit && distance < curFlashRange) {
            distance += 0.025;
            let rx = px + Math.cos(rayAngle) * distance;
            let ry = py + Math.sin(rayAngle) * distance;
            let tx = Math.floor(rx), ty = Math.floor(ry);

            if (tx < 0 || tx >= MAP_SIZE || ty < 0 || ty >= MAP_SIZE) { hit = true; hitType = 1; } 
            else if (houseMap[ty][tx] > 0) {
                hit = true; hitType = houseMap[ty][tx];
                wallX = (rx - tx) + (ry - ty); wallX = (wallX - Math.floor(wallX)) * 64;
            }
        }

        let correctedDist = distance * Math.cos(rayAngle - angle);
        zBuffer[i] = correctedDist;

        let h = Math.min(canvas.height, (projDist / (correctedDist + 0.0001)));
        let shade = Math.max(0, 1 - (correctedDist / curFlashRange));

        if (hitType === 3) {
            ctx.fillStyle = `rgba(212, 175, 55, ${shade})`;
            ctx.fillRect(i * w, (canvas.height - h) / 2, w + 1, h);
        } else {
            ctx.drawImage(texCanvas, Math.floor(wallX), 0, 1, 64, i * w, (canvas.height - h) / 2, w + 1, h);
            ctx.fillStyle = `rgba(0, 0, 0, ${1 - shade})`;
            ctx.fillRect(i * w, (canvas.height - h) / 2, w + 1, h);
        }
    }

    // 2. 특수 오프젝트(아이템) 독자적 3D 형상 렌더링
    worldItems.forEach(item => {
        let idxX = item.x - px, idxY = item.y - py;
        let dist = Math.sqrt(idxX*idxX + idxY*idxY);
        let itemAngle = Math.atan2(idxY, idxX) - angle;
        while (itemAngle < -Math.PI) itemAngle += 2 * Math.PI;
        while (itemAngle > Math.PI) itemAngle -= 2 * Math.PI;

        if (Math.abs(itemAngle) < fov / 1.8 && dist < curFlashRange) {
            let sx = (canvas.width / 2) + Math.tan(itemAngle) * projDist;
            let rayIndex = Math.floor((sx / canvas.width) * numRays);
            
            if (rayIndex >= 0 && rayIndex < numRays && dist < zBuffer[rayIndex]) {
                let size = Math.min(100, projDist * 0.4 / dist);
                let floatY = Math.sin(animTimer * 2.5) * 6; 
                let centerY = canvas.height / 2 + size/3 + floatY;

                // 아이템 고유 3D 그래픽 그리기
                drawCustomItem(item.type, sx, centerY, size);

                // 아이템 텍스트 라벨
                ctx.save();
                ctx.fillStyle = "#ffffff";
                ctx.font = `bold ${Math.max(11, Math.floor(size/2.2))}px sans-serif`;
                ctx.textAlign = "center";
                ctx.shadowColor = "#000000"; ctx.shadowBlur = 6;
                ctx.fillText(item.name, sx, centerY - size/1.3);
                ctx.restore();
            }
        }
    });

    // 3. 3D 원혼 렌더링
    ghosts.forEach(g => {
        if (g.hp <= 0) return;
        let gdx = g.x - px, gdy = g.y - py;
        let gDist = Math.sqrt(gdx*gdx + gdy*gdy);
        let gAngle = Math.atan2(gdy, gdx) - angle;
        while (gAngle < -Math.PI) gAngle += 2 * Math.PI;
        while (gAngle > Math.PI) gAngle -= 2 * Math.PI;

        if (Math.abs(gAngle) < fov / 1.8 && gDist < curFlashRange) {
            let sx = (canvas.width / 2) + Math.tan(gAngle) * projDist;
            let rayIndex = Math.floor((sx / canvas.width) * numRays);
            
            if (rayIndex >= 0 && rayIndex < numRays && gDist < zBuffer[rayIndex]) {
                let size = Math.min(420, projDist * 1.1 / gDist);
                let topY = canvas.height / 2 - size / 2;
                let wobble = Math.sin(animTimer * 4) * 6;

                ctx.save();
                ctx.fillStyle = g.stun > 0 ? '#00ffff' : 'rgba(10,0,2,0.95)';
                ctx.beginPath();
                ctx.ellipse(sx + wobble, topY + size/2, size/4, size/2.2, 0, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = g.stun > 0 ? '#ffffff' : '#ff0000';
                ctx.shadowColor = '#ff0000'; ctx.shadowBlur = 15;
                ctx.beginPath();
                ctx.arc(sx + wobble - size/10, topY + size/3, size/20, 0, Math.PI * 2);
                ctx.arc(sx + wobble + size/10, topY + size/3, size/20, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }
        }
    });

    // 4. 무기 연출
    if (items.knife) {
        ctx.save();
        let attackOffset = isAttacking * 12;
        ctx.fillStyle = '#cccccc';
        ctx.shadowColor = '#ffffff'; ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.moveTo(canvas.width/2 + 90 - attackOffset, canvas.height - attackOffset);
        ctx.lineTo(canvas.width/2 + 150 - attackOffset, canvas.height - 140 - attackOffset);
        ctx.lineTo(canvas.width/2 + 175 - attackOffset, canvas.height - 110 - attackOffset);
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

components.html(horror_game_html, height=610)
