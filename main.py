import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="🏚️ 저주받은 저택 - R키 상호작용 에디션", layout="wide")

st.title("🏚️ 저주받은 저택: 방과 아이템의 비밀")
st.caption("조작 방법 | W/A/S/D: 이동 | 방향키(←/→) 또는 마우스 드래그: 시점 회전 | E: 달리기 | R: 상호작용(문 열기/아이템 획득) | 1,2,3: 아이템 사용 | 클릭: 공격")

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

        #msg { position: absolute; top: 30%; left: 50%; transform: translate(-50%, -50%); color: #ff1111; font-size: 20px; font-weight: bold; text-align: center; text-shadow: 0 0 10px #000; z-index: 5; pointer-events: none; letter-spacing: 1px; }
        #room-info { position: absolute; top: 15px; right: 15px; color: #aaa; font-size: 11px; text-align: right; z-index: 5; pointer-events: none; }

        #glitch-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; z-index: 4; opacity: 0;
            background: repeating-linear-gradient(0deg, rgba(255,0,0,0.18), rgba(255,0,0,0.18) 2px, transparent 2px, transparent 4px);
        }

        #jumpscare {
            display: none; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-color: #050000; z-index: 99; flex-direction: column; justify-content: center; align-items: center;
            animation: flash-red 0.08s infinite alternate;
        }
        @keyframes flash-red {
            0% { background-color: #000; }
            100% { background-color: #200000; }
        }

        #scare-face {
            width: 340px; height: 400px; background: radial-gradient(circle, #800 0%, #200 50%, #000 100%);
            border-radius: 45% 45% 50% 50%; position: relative; box-shadow: 0 0 150px #f00;
            animation: violent-shake 0.015s infinite alternate;
        }
        .eye { position: absolute; top: 25%; width: 65px; height: 85px; background: #fff; border-radius: 50%; box-shadow: inset 0 0 30px #f00, 0 0 20px #ff0000; }
        .eye.left { left: 18%; transform: rotate(-15deg); }
        .eye.right { right: 18%; transform: rotate(15deg); }
        .pupil { position: absolute; top: 30%; left: 30%; width: 14px; height: 14px; background: #000; border-radius: 50%; box-shadow: 0 0 12px #f00; }
        .mouth { position: absolute; bottom: 8%; left: 10%; width: 80%; height: 150px; background: #000; border-radius: 10px 10px 70px 70px; border: 4px solid #a00; overflow: hidden; }
        .teeth { width: 100%; height: 35px; background: repeating-linear-gradient(90deg, #eee, #eee 14px, #200 14px, #200 20px); }
        .blood-drip { position: absolute; top: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(150,0,0,0.6) 0%, transparent 80%); }

        #scare-text { color: #ff0000; font-size: 32px; font-weight: 900; margin-top: 30px; text-shadow: 0 0 25px #ff0000; letter-spacing: 4px; }
        #restart-btn { margin-top: 25px; padding: 12px 32px; font-size: 15px; background: #050505; color: #ff3333; border: 1px solid #ff0000; cursor: pointer; font-weight: bold; }
        #restart-btn:hover { background: #400; color: #fff; }

        @keyframes violent-shake {
            0% { transform: translate(10px, -10px) scale(1.1); }
            100% { transform: translate(-10px, 10px) scale(1.22); }
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
        <div style="color:#ff3333; font-weight:bold;" id="current-room-name">현재 위치: 중앙 복도</div>
        <div>문이나 아이템 근처에서 [R] 키를 누르세요</div>
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
            <div class="mouth">
                <div class="teeth"></div>
                <div class="blood-drip"></div>
            </div>
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
    } else if (type === 'door') {
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(120, now);
        osc.frequency.linearRampToValueAtTime(60, now + 0.3);
        gain.gain.setValueAtTime(0.4, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.3);
    } else if (type === 'jumpscare') {
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(180, now);
        osc.frequency.linearRampToValueAtTime(1100, now + 0.08);
        osc.frequency.linearRampToValueAtTime(60, now + 1.2);
        gain.gain.setValueAtTime(1.0, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 1.2);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 1.2);
    }
}

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 580;

const wallTex = document.createElement('canvas');
wallTex.width = 64; wallTex.height = 64;
const wCtx = wallTex.getContext('2d');
wCtx.fillStyle = '#2d1d1a'; wCtx.fillRect(0,0,64,64);
wCtx.fillStyle = '#140a08';
for(let i=0; i<64; i+=16) {
    wCtx.fillRect(0, i, 64, 2);
    for(let j=0; j<64; j+=16) {
        let offset = (i/16)%2 === 0 ? 0 : 8;
        wCtx.fillRect(j+offset, i, 2, 16);
    }
}

const doorTex = document.createElement('canvas');
doorTex.width = 64; doorTex.height = 64;
const dCtx = doorTex.getContext('2d');
dCtx.fillStyle = '#4a2e18'; dCtx.fillRect(0,0,64,64);
dCtx.fillStyle = '#261408';
dCtx.fillRect(2, 2, 60, 60);
dCtx.fillStyle = '#5c3a1e';
dCtx.fillRect(6, 6, 24, 24); dCtx.fillRect(34, 6, 24, 24);
dCtx.fillRect(6, 34, 24, 24); dCtx.fillRect(34, 34, 24, 24);
dCtx.fillStyle = '#ffaa00';
dCtx.beginPath(); dCtx.arc(10, 32, 3, 0, Math.PI*2); dCtx.fill();

let houseMap = [];
let MAP_SIZE = 21;
let px = 10.5, py = 10.5;
let angle = 0;
let hp = 100;
let stamina = 100;
let flashRange = 12;
let gameOver = false;
let items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
let isAttacking = 0;
let ghosts = [];
let worldItems = [];
let zBuffer = new Array(160).fill(0);
let screenShake = 0;
let animTimer = 0;

const fov = Math.PI * 0.42; 

const initialMap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,0,0,1],
    [1,0,0,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,0,0,1],
    [1,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,1],
    [1,1,1,1,1,0,1,1,2,1,1,1,2,1,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,2,0,1,0,0,0,1,0,2,0,0,0,1,0,1],
    [1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1],
    [1,0,1,1,2,1,1,0,0,0,0,0,0,0,1,1,2,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,2,1,1,0,0,0,0,0,0,0,1,1,2,1,1,0,1],
    [1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1],
    [1,0,1,0,0,0,2,0,1,0,0,0,1,0,2,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,0,1,1,2,1,1,1,2,1,1,0,1,1,1,1,1],
    [1,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,1],
    [1,0,0,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,0,0,1],
    [1,0,0,0,1,1,1,0,0,0,1,0,0,0,1,1,1,0,0,3,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

function initGame() {
    houseMap = JSON.parse(JSON.stringify(initialMap));
    MAP_SIZE = houseMap.length;
    px = 10.5; py = 10.5;
    angle = 0;
    hp = 100;
    stamina = 100;
    flashRange = 12;
    gameOver = false;
    items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
    isAttacking = 0;

    ghosts = [
        { x: 2.5, y: 2.5, hp: 100, stun: 0 },
        { x: 18.5, y: 2.5, hp: 100, stun: 0 },
        { x: 2.5, y: 18.5, hp: 100, stun: 0 }
    ];

    worldItems = [
        { x: 2.5, y: 1.5, type: 'knife', name: '녹슨 단검 (서재)' },
        { x: 18.5, y: 1.5, type: 'potion', name: '의용 회복제 (응급실)' },
        { x: 1.5, y: 8.5, type: 'battery', name: '고전압 배터리 (창고)' },
        { x: 19.5, y: 8.5, type: 'potion', name: '의용 회복제 (침실)' },
        { x: 1.5, y: 13.5, type: 'battery', name: '고전압 배터리 (연구실)' },
        { x: 18.5, y: 18.5, type: 'key', name: '피묻은 열쇠 (지하 밀실)' }
    ];

    document.getElementById('jumpscare').style.display = 'none';
    document.getElementById('msg').innerText = "문 앞이나 아이템 근처에서 [R] 키를 눌러 상호작용하세요";
    document.getElementById('msg').style.color = "#ff3333";
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
    if (k === 'ㄱ') return 'r';
    return k;
}

// R 키를 통한 상호작용 처리 함수
function handleInteract() {
    if (gameOver) return;

    // 1. 플레이어 앞 정면 위치 계산
    let checkDist = 1.2;
    let targetX = Math.floor(px + Math.cos(angle) * checkDist);
    let targetY = Math.floor(py + Math.sin(angle) * checkDist);

    // 2. 문(2번) 또는 탈출문(3번) 상호작용
    if (targetX >= 0 && targetX < MAP_SIZE && targetY >= 0 && targetY < MAP_SIZE) {
        let tile = houseMap[targetY][targetX];
        if (tile === 2) {
            houseMap[targetY][targetX] = 0; // 문 개방
            playSound('door');
            showTmpMsg("🚪 문을 열었습니다.");
            return;
        } else if (tile === 3) {
            if (items.key) {
                gameOver = true;
                playSound('door');
                document.getElementById('msg').innerText = "🚪 열쇠로 잠긴 문을 열고 탈출에 성공했습니다!";
                document.getElementById('msg').style.color = "gold";
            } else {
                showTmpMsg("🔒 문이 굳게 잠겨 있습니다. 피묻은 열쇠가 필요합니다.");
            }
            return;
        }
    }

    // 3. 근처 아이템 상호작용
    let picked = false;
    worldItems.forEach((item, idx) => {
        let dist = Math.sqrt((px - item.x)**2 + (py - item.y)**2);
        if (dist < 1.5 && !picked) {
            playSound('item');
            if (item.type === 'key') { items.key = true; showTmpMsg("🔑 피묻은 열쇠를 습득했습니다! 탈출문(황금색)을 찾으세요."); }
            if (item.type === 'knife') { items.knife = true; showTmpMsg("🗡️ 녹슨 단검을 습득했습니다."); }
            if (item.type === 'potion') { items.potion++; showTmpMsg("💊 의용 회복제를 습득했습니다."); }
            if (item.type === 'battery') { items.battery++; showTmpMsg("🔋 배터리를 습득했습니다."); }
            worldItems.splice(idx, 1);
            updateUI();
            picked = true;
        }
    });

    if (!picked) {
        showTmpMsg("상호작용할 대상이 가까이에 없습니다.");
    }
}

window.addEventListener('keydown', e => {
    let k = parseKey(e.key);
    keys[k] = true;
    
    if (!gameOver) {
        if (k === 'r') {
            handleInteract();
        }
        if (e.key === '1' && items.potion > 0) { 
            hp = Math.min(100, hp + 60); items.potion--; 
            playSound('item'); showTmpMsg("💊 체력을 회복했습니다."); updateUI(); 
        }
        if (e.key === '2' && items.battery > 0) { 
            flashRange = 16; items.battery--; 
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
    let tile = houseMap[Math.floor(y)][Math.floor(x)];
    return tile === 1 || tile === 2; // 벽(1) 및 닫힌 문(2)은 통과 불가 (R키로 열어야 이동 가능)
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

    let curX = Math.floor(px), curY = Math.floor(py);
    let roomTxt = "중앙 복도";
    if (curX < 4 && curY < 4) roomTxt = "북서쪽 서재 (단검 위치)";
    else if (curX > 16 && curY < 4) roomTxt = "북동쪽 응급실 (회복제 위치)";
    else if (curX < 4 && curY > 16) roomTxt = "남서쪽 침실 (부적 위치)";
    else if (curX > 16 && curY > 16) roomTxt = "남동쪽 지하 밀실 (열쇠 위치)";
    document.getElementById('current-room-name').innerText = "현재 위치: " + roomTxt;

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

function draw3DItem(type, sx, sy, size) {
    ctx.save();
    ctx.translate(sx, sy);

    if (type === 'key') {
        ctx.fillStyle = '#b38f00'; ctx.beginPath(); ctx.arc(3, -size/3 + 3, size/3.2, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#ffd700'; ctx.beginPath(); ctx.arc(0, -size/3, size/3.2, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#1a1100'; ctx.beginPath(); ctx.arc(0, -size/3, size/6, 0, Math.PI * 2); ctx.fill();
        
        ctx.fillStyle = '#ffd700';
        ctx.fillRect(-size/12, -size/6, size/6, size/1.2);
        ctx.fillRect(size/12, size/4, size/4, size/8);
        ctx.fillRect(size/12, size/2.2, size/4, size/8);

    } else if (type === 'knife') {
        ctx.fillStyle = '#888888';
        ctx.beginPath();
        ctx.moveTo(0, -size/1.5);
        ctx.lineTo(size/6, size/6);
        ctx.lineTo(-size/6, size/6);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.moveTo(0, -size/1.5);
        ctx.lineTo(0, size/6);
        ctx.lineTo(-size/6, size/6);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = '#4a2511';
        ctx.fillRect(-size/4, size/6, size/2, size/10);
        ctx.fillStyle = '#2b1408';
        ctx.fillRect(-size/8, size/6 + size/10, size/4, size/2.5);

    } else if (type === 'potion') {
        ctx.fillStyle = 'rgba(200, 200, 255, 0.4)';
        ctx.beginPath(); ctx.arc(0, size/4, size/2.2, 0, Math.PI * 2); ctx.fill();
        
        ctx.fillStyle = '#ff1133';
        ctx.beginPath(); ctx.arc(0, size/4, size/2.6, 0, Math.PI * 2); ctx.fill();
        
        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.beginPath(); ctx.arc(-size/6, size/6, size/8, 0, Math.PI * 2); ctx.fill();

        ctx.fillStyle = '#8b5a2b';
        ctx.fillRect(-size/6, -size/3, size/3, size/6);

    } else if (type === 'battery') {
        ctx.fillStyle = '#222222';
        ctx.fillRect(-size/3, -size/3, size/1.5, size/1.2);
        ctx.fillStyle = '#ff6600';
        ctx.fillRect(-size/3, 0, size/1.5, size/2.4);

        ctx.fillStyle = '#aaaaaa';
        ctx.fillRect(-size/8, -size/2, size/4, size/6);
        
        ctx.fillStyle = '#ffffff';
        ctx.font = `bold ${Math.max(10, Math.floor(size/3))}px sans-serif`;
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText('⚡', 0, size/5);
    }

    ctx.restore();
}

function render() {
    ctx.save();
    if (screenShake > 0) {
        ctx.translate((Math.random() - 0.5) * screenShake, (Math.random() - 0.5) * screenShake);
    }

    let ceilGrd = ctx.createLinearGradient(0, 0, 0, canvas.height/2);
    ceilGrd.addColorStop(0, '#0a0a0a'); ceilGrd.addColorStop(1, '#221515');
    ctx.fillStyle = ceilGrd; ctx.fillRect(0, 0, canvas.width, canvas.height/2);

    let floorGrd = ctx.createLinearGradient(0, canvas.height/2, 0, canvas.height);
    floorGrd.addColorStop(0, '#1c1010'); floorGrd.addColorStop(1, '#050505');
    ctx.fillStyle = floorGrd; ctx.fillRect(0, canvas.height/2, canvas.width, canvas.height/2);

    const numRays = 160;
    const w = canvas.width / numRays;
    let curFlashRange = flashRange + (Math.random() - 0.5) * 0.2;

    let projDist = (canvas.width / 2) / Math.tan(fov / 2);

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
        let shade = Math.max(0.15, 1 - (correctedDist / curFlashRange));

        if (hitType === 3) {
            ctx.fillStyle = `rgba(230, 190, 60, ${shade})`;
            ctx.fillRect(i * w, (canvas.height - h) / 2, w + 1, h);
        } else if (hitType === 2) {
            ctx.drawImage(doorTex, Math.floor(wallX), 0, 1, 64, i * w, (canvas.height - h) / 2, w + 1, h);
            ctx.fillStyle = `rgba(0, 0, 0, ${1 - shade})`;
            ctx.fillRect(i * w, (canvas.height - h) / 2, w + 1, h);
        } else {
            ctx.drawImage(wallTex, Math.floor(wallX), 0, 1, 64, i * w, (canvas.height - h) / 2, w + 1, h);
            ctx.fillStyle = `rgba(0, 0, 0, ${1 - shade})`;
            ctx.fillRect(i * w, (canvas.height - h) / 2, w + 1, h);
        }
    }

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
                let size = Math.min(120, projDist * 0.45 / dist);
                let floatY = Math.sin(animTimer * 2.5) * 5; 
                let centerY = canvas.height / 2 + size/3 + floatY;

                draw3DItem(item.type, sx, centerY, size);

                ctx.save();
                ctx.fillStyle = "#ffffff";
                ctx.font = `bold ${Math.max(11, Math.floor(size/2.2))}px sans-serif`;
                ctx.textAlign = "center";
                ctx.shadowColor = "#000000"; ctx.shadowBlur = 6;
                ctx.fillText(item.name + " [R 키로 습득]", sx, centerY - size/1.2);
                ctx.restore();
            }
        }
    });

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
                let size = Math.min(450, projDist * 1.1 / gDist);
                let topY = canvas.height / 2 - size / 2;
                let wobble = Math.sin(animTimer * 4) * 6;

                ctx.save();
                ctx.fillStyle = g.stun > 0 ? '#00ffff' : 'rgba(15,2,4,0.95)';
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
