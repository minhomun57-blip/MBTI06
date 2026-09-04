import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="낡은 집에서의 탈출 - 극악 공포", layout="wide")

st.title("🏚️ 낡은 집에서의 탈출 (Old House Escape - Nightmare Edition)")
st.caption("조작 방법 | W/S/A/D: 이동 | 마우스 이동: 시점 회전 (화면 클릭 시 고정) | E: 달리기 | 1,2,3: 아이템 사용 | 마우스 좌클릭: 공격")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { margin: 0; overflow: hidden; background-color: #000; font-family: 'Courier New', monospace; user-select: none; }
        #canvas { width: 100%; height: 550px; display: block; cursor: crosshair; }
        
        #ui { position: absolute; top: 15px; left: 15px; color: #e0e0e0; text-shadow: 2px 2px 4px #000; font-size: 13px; display: flex; flex-direction: column; gap: 8px; z-index: 5; pointer-events: none; }
        .bar-container { width: 200px; height: 14px; background: rgba(0,0,0,0.8); border: 1px solid #555; border-radius: 3px; overflow: hidden; }
        .bar-fill { height: 100%; width: 100%; transition: width 0.05s linear; }
        #hp-bar { background: linear-gradient(90deg, #800000, #ff0000); }
        #stamina-bar { background: linear-gradient(90deg, #1b5e20, #4caf50); }

        #inventory { position: absolute; bottom: 15px; right: 15px; display: flex; gap: 8px; z-index: 5; pointer-events: none; }
        .slot { width: 65px; height: 65px; border: 1px solid #444; background: rgba(10,10,10,0.85); color: #ccc; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 10px; border-radius: 4px; text-align: center; }
        .slot-key { color: #ffcc00; font-size: 10px; margin-bottom: 2px; font-weight: bold; }

        #msg { position: absolute; top: 35%; left: 50%; transform: translate(-50%, -50%); color: #ff2222; font-size: 22px; font-weight: bold; text-align: center; text-shadow: 0 0 8px #000; z-index: 5; pointer-events: none; }
        #room-info { position: absolute; top: 15px; right: 15px; color: #888; font-size: 12px; text-align: right; z-index: 5; pointer-events: none; }

        /* 글리치 오버레이 */
        #glitch-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; z-index: 4; opacity: 0;
            background: repeating-linear-gradient(0deg, rgba(255,0,0,0.05), rgba(255,0,0,0.05) 1px, transparent 1px, transparent 2px);
        }

        /* 기괴한 점프스케어 연출 */
        #jumpscare {
            display: none;
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: #000;
            z-index: 99;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }
        #scare-face {
            width: 320px;
            height: 380px;
            background: radial-gradient(circle, #3a0000 0%, #1a0000 60%, #000000 100%);
            border-radius: 40% 40% 50% 50%;
            position: relative;
            box-shadow: 0 0 100px #ff0000;
            animation: violent-shake 0.03s infinite alternate;
        }
        .eye { position: absolute; top: 30%; width: 50px; height: 70px; background: #fff; border-radius: 50%; box-shadow: inset 0 0 20px #ff0000; }
        .eye.left { left: 22%; transform: rotate(-10deg); }
        .eye.right { right: 22%; transform: rotate(10deg); }
        .pupil { position: absolute; top: 35%; left: 35%; width: 12px; height: 12px; background: #000; border-radius: 50%; box-shadow: 0 0 8px #ff0000; }
        .mouth { position: absolute; bottom: 12%; left: 15%; width: 70%; height: 120px; background: #050000; border-radius: 10px 10px 60px 60px; border: 3px solid #600; overflow: hidden; }
        .teeth { width: 100%; height: 20px; background: repeating-linear-gradient(90deg, #ddd, #ddd 10px, #000 10px, #000 15px); }
        
        #scare-text { color: #ff0000; font-size: 36px; font-weight: 900; margin-top: 25px; text-shadow: 0 0 15px #ff0000; letter-spacing: 3px; }
        #restart-btn { margin-top: 20px; padding: 12px 28px; font-size: 15px; background: #111; color: #ff4d4d; border: 1px solid #ff0000; cursor: pointer; border-radius: 3px; font-family: inherit; font-weight: bold; }
        #restart-btn:hover { background: #300; color: #fff; }

        @keyframes violent-shake {
            0% { transform: translate(6px, -6px) scale(1.1) rotate(1deg); }
            50% { transform: translate(-6px, 6px) scale(1.15) rotate(-1deg); }
            100% { transform: translate(-4px, -4px) scale(1.08) rotate(2deg); }
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
        <div style="color:#ff4d4d; font-weight:bold;">구역: 저주받은 저택 1층</div>
        <div>목표: 피묻은 열쇠를 찾아 탈출하라</div>
    </div>
    
    <div id="inventory">
        <div class="slot" id="slot1"><span class="slot-key">[1]</span>회복약<br><span id="cnt-potion">0</span></div>
        <div class="slot" id="slot2"><span class="slot-key">[2]</span>배터리<br><span id="cnt-battery">0</span></div>
        <div class="slot" id="slot3"><span class="slot-key">[3]</span>퇴마부적<br><span id="cnt-talisman">1</span></div>
        <div class="slot" id="slot4"><span class="slot-key">[4]</span>탈출열쇠<br><span id="cnt-key">미획득</span></div>
    </div>

    <div id="msg">화면을 클릭하여 시점을 고정하고 시작하세요</div>
    
    <div id="jumpscare">
        <div id="scare-face">
            <div class="eye left"><div class="pupil"></div></div>
            <div class="eye right"><div class="pupil"></div></div>
            <div class="mouth"><div class="teeth"></div></div>
        </div>
        <div id="scare-text">당신의 영혼이 저택에 귀속되었습니다...</div>
        <button id="restart-btn" onclick="resetGame()">다시 저주에 도전하기</button>
    </div>
    
    <canvas id="canvas"></canvas>

<script>
// --- Web Audio API 기반 오디오 합성기 (외부 파일 없이 작동) ---
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
        osc.frequency.setValueAtTime(120, now);
        osc.frequency.exponentialRampToValueAtTime(30, now + 0.15);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.15);
    } else if (type === 'hit') {
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'square';
        osc.frequency.setValueAtTime(80, now);
        osc.frequency.exponentialRampToValueAtTime(20, now + 0.2);
        gain.gain.setValueAtTime(0.5, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.2);
    } else if (type === 'talisman') {
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(600, now);
        osc.frequency.exponentialRampToValueAtTime(150, now + 0.6);
        gain.gain.setValueAtTime(0.6, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.6);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.6);
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
        // 비명/저주음 생성 (노이즈 + 저음 oscillator)
        let osc = audioCtx.createOscillator();
        let gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(300, now);
        osc.frequency.linearRampToValueAtTime(700, now + 0.1);
        osc.frequency.linearRampToValueAtTime(100, now + 0.8);
        gain.gain.setValueAtTime(0.8, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.9);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.9);
    }
}

// BGM 및 스태틱 사운드 루프
let bgmOsc = null;
let heartbeatTimer = 0;
function playHeartbeat(dist) {
    if (!audioCtx) return;
    let now = audioCtx.currentTime;
    let osc = audioCtx.createOscillator();
    let gain = audioCtx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(55, now);
    osc.frequency.exponentialRampToValueAtTime(30, now + 0.08);
    let vol = Math.max(0.05, 0.4 - (dist * 0.04));
    gain.gain.setValueAtTime(vol, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
    osc.connect(gain); gain.connect(audioCtx.destination);
    osc.start(now); osc.stop(now + 0.08);
}

// --- 게임 변수 및 맵 설정 ---
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
let zBuffer = new Array(160).fill(0);
let screenShake = 0;

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
    flashRange = 8;
    gameOver = false;
    items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
    isAttacking = 0;
    ghosts = [
        { x: 1.5, y: 1.5, hp: 100, stun: 0 },
        { x: 13.5, y: 13.5, hp: 100, stun: 0 }
    ];
    document.getElementById('jumpscare').style.display = 'none';
    document.getElementById('msg').innerText = "화면을 클릭하여 시점을 고정하고 시작하세요";
    document.getElementById('msg').style.color = "#ff2222";
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
            hp = Math.min(100, hp + 60); 
            items.potion--; 
            playSound('item');
            showTmpMsg("💊 기괴한 회복약을 복용했습니다.");
            updateUI(); 
        }
        if (e.key === '2' && items.battery > 0) { 
            flashRange = 14; 
            items.battery--; 
            playSound('item');
            showTmpMsg("🔋 라이트 전압을 올려 시야를 넓혔습니다.");
            updateUI(); 
        }
        if (e.key === '3' && items.talisman > 0) { 
            ghosts.forEach(g => {
                g.stun = 300;
                // 강하게 밀쳐냄
                g.x += (g.x - px) * 2;
                g.y += (g.y - py) * 2;
            }); 
            items.talisman--; 
            playSound('talisman');
            screenShake = 15;
            showTmpMsg("📜 퇴마 부적이 강렬한 빛을 내뿜습니다!");
            updateUI(); 
        }
    }
});

window.addEventListener('keyup', e => {
    let k = parseKey(e.key);
    keys[k] = false;
});

// 마우스 포인터 락 시점 회전
canvas.addEventListener('click', () => {
    initAudio();
    canvas.requestPointerLock = canvas.requestPointerLock || canvas.mozRequestPointerLock;
    canvas.requestPointerLock();
    if (document.getElementById('msg').innerText.includes("클릭")) {
        document.getElementById('msg').innerText = "";
    }
    if (items.knife && isAttacking === 0 && !gameOver) {
        isAttacking = 10;
        playSound('attack');
        checkAttackHit();
    }
});

document.addEventListener('mousemove', e => {
    if (document.pointerLockElement === canvas || document.mozPointerLockElement === canvas) {
        angle += e.movementX * 0.003;
    }
});

function showTmpMsg(txt) {
    let msgEl = document.getElementById('msg');
    msgEl.innerText = txt;
    setTimeout(() => { if (!gameOver && msgEl.innerText === txt) msgEl.innerText = ""; }, 2000);
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
            g.hp -= 50;
            g.stun = 50;
            playSound('hit');
            screenShake = 8;
            if (g.hp <= 0) showTmpMsg("💀 원혼이 단검에 베여 소멸했습니다!");
        }
    });
}

function updateUI() {
    document.getElementById('hp-bar').style.width = Math.max(0, hp) + "%";
    document.getElementById('stamina-bar').style.width = Math.max(0, stamina) + "%";
    document.getElementById('weapon').innerText = items.knife ? "녹슨 단검 (좌클릭: 공격)" : "맨손";
    
    document.getElementById('cnt-potion').innerText = items.potion;
    document.getElementById('cnt-battery').innerText = items.battery;
    document.getElementById('cnt-talisman').innerText = items.talisman;
    document.getElementById('cnt-key').innerText = items.key ? "획득완료" : "미획득";

    document.getElementById('slot1').style.borderColor = items.potion > 0 ? "#ff0000" : "#444";
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
    playSound('jumpscare');
    document.getElementById('jumpscare').style.display = 'flex';
}

function update() {
    if (gameOver) return;

    if (screenShake > 0) screenShake--;

    const rotSpeed = 0.04;
    if (keys['left']) angle -= rotSpeed;
    if (keys['right']) angle += rotSpeed;

    let speed = 0.038;
    let isMoving = keys['w'] || keys['s'] || keys['a'] || keys['d'];

    if (keys['e'] && isMoving && stamina >= 0.5) {
        speed = 0.068;
        stamina = Math.max(0, stamina - 0.5);
    } else {
        stamina = Math.min(100, stamina + 0.18);
    }

    let dx = 0, dy = 0;
    if (keys['w']) { dx += Math.cos(angle) * speed; dy += Math.sin(angle) * speed; }
    if (keys['s']) { dx -= Math.cos(angle) * speed; dy -= Math.sin(angle) * speed; }
    if (keys['a']) { dx += Math.sin(angle) * speed; dy -= Math.cos(angle) * speed; }
    if (keys['d']) { dx -= Math.sin(angle) * speed; dy += Math.cos(angle) * speed; }

    const margin = 0.25;
    if (!isSolid(px + dx + Math.sign(dx)*margin, py)) px += dx;
    if (!isSolid(px, py + dy + Math.sign(dy)*margin)) py += dy;

    // 아이템 습득 처리
    let ix = Math.floor(px), iy = Math.floor(py);
    let cell = houseMap[iy][ix];
    if (cell === 2) { 
        items.key = true; houseMap[iy][ix] = 0; 
        playSound('item'); showTmpMsg("🔑 피묻은 열쇠를 찾았습니다! 탈출문으로 이동하세요!");
    } else if (cell === 4) { 
        items.knife = true; houseMap[iy][ix] = 0; 
        playSound('item'); showTmpMsg("🗡️ 녹슨 단검을 얻었습니다. (마우스 클릭으로 원혼 공격 가능)");
    } else if (cell === 5) { 
        items.potion++; houseMap[iy][ix] = 0; 
        playSound('item'); showTmpMsg("💊 회복약을 획득했습니다.");
    } else if (cell === 6) { 
        items.battery++; houseMap[iy][ix] = 0; 
        playSound('item'); showTmpMsg("🔋 배터리를 획득했습니다.");
    } else if (cell === 3 && items.key) {
        gameOver = true;
        document.getElementById('msg').innerText = "🚪 낡은 집의 빗장을 풀고 피투성이 현관을 통해 탈출했습니다!";
        document.getElementById('msg').style.color = "gold";
    }
    updateUI();

    // 원혼 AI 및 사운드/글리치 연출
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
                // 추적 속도 증가
                g.x += (gdx / dist) * 0.012;
                g.y += (gdy / dist) * 0.012;
            }
            if (dist < 0.65) {
                hp -= 2.0;
                screenShake = 5;
                if (hp <= 0) triggerJumpscare();
            }
        }
    });

    // 심장박동 사운드 및 글리치
    if (minDist < 7 && !gameOver) {
        heartbeatTimer++;
        let interval = Math.max(10, Math.floor(minDist * 8));
        if (heartbeatTimer % interval === 0) {
            playHeartbeat(minDist);
        }
        document.getElementById('glitch-overlay').style.opacity = Math.max(0, (7 - minDist) / 7 * 0.8);
    } else {
        document.getElementById('glitch-overlay').style.opacity = 0;
    }

    if (isAttacking > 0) isAttacking--;
}

function renderMinimap() {
    const size = 5;
    const offsetX = 15;
    const offsetY = canvas.height - (15 * size) - 15;

    ctx.fillStyle = "rgba(0,0,0,0.7)";
    ctx.fillRect(offsetX - 2, offsetY - 2, 15 * size + 4, 15 * size + 4);

    for (let r = 0; r < 15; r++) {
        for (let c = 0; c < 15; c++) {
            if (houseMap[r][c] === 1) ctx.fillStyle = "#333";
            else if (houseMap[r][c] === 3) ctx.fillStyle = "gold";
            else ctx.fillStyle = "#050505";
            ctx.fillRect(offsetX + c * size, offsetY + r * size, size - 1, size - 1);
        }
    }

    // 플레이어
    ctx.fillStyle = "#ff0000";
    ctx.beginPath();
    ctx.arc(offsetX + px * size, offsetY + py * size, 2, 0, Math.PI * 2);
    ctx.fill();
}

function render() {
    ctx.save();
    if (screenShake > 0) {
        let sx = (Math.random() - 0.5) * screenShake * 2;
        let sy = (Math.random() - 0.5) * screenShake * 2;
        ctx.translate(sx, sy);
    }

    // 천장 & 바닥 (어두운 그래디언트)
    let ceilingGrad = ctx.createLinearGradient(0, 0, 0, canvas.height/2);
    ceilingGrad.addColorStop(0, '#000000');
    ceilingGrad.addColorStop(1, '#050202');
    ctx.fillStyle = ceilingGrad;
    ctx.fillRect(0, 0, canvas.width, canvas.height/2);

    let floorGrad = ctx.createLinearGradient(0, canvas.height/2, 0, canvas.height);
    floorGrad.addColorStop(0, '#0a0303');
    floorGrad.addColorStop(1, '#000000');
    ctx.fillStyle = floorGrad;
    ctx.fillRect(0, canvas.height/2, canvas.width, canvas.height/2);

    const fov = Math.PI / 3;
    const numRays = 160;
    const w = canvas.width / numRays;

    // 플래시 불빛 미세 떨림 (Flicker)
    let flicker = (Math.random() - 0.5) * 0.4;
    let curFlashRange = Math.max(1, flashRange + flicker);

    for (let i = 0; i < numRays; i++) {
        let rayAngle = (angle - fov / 2) + (i / numRays) * fov;
        let distance = 0;
        let hit = false;
        let hitType = 1;

        while (!hit && distance < curFlashRange) {
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
        let shade = Math.max(0, Math.floor(160 - correctedDist * (160 / curFlashRange)));

        // 피투성이 어두운 적갈색 벽면 연출
        let r = Math.floor(shade * 0.6);
        let g = Math.floor(shade * 0.15);
        let b = Math.floor(shade * 0.1);

        ctx.fillStyle = (hitType === 1) ? `rgb(${r}, ${g}, ${b})` : `rgb(${Math.floor(r*0.4)}, 0, 0)`;
        let topY = (canvas.height - h) / 2;
        ctx.fillRect(i * w, topY, w + 1, h);
    }

    // 3D 원혼 (기괴한 실루엣 및 붉은 눈빛)
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
                let size = Math.min(420, canvas.height / gDist);
                
                ctx.save();
                let topY = canvas.height / 2 - size / 2;
                
                // 형체 (검은 피투성이 음영)
                ctx.fillStyle = g.stun > 0 ? '#00ffff' : '#0a0002';
                ctx.beginPath();
                ctx.ellipse(sx, topY + size/2, size/5, size/2.5, 0, 0, Math.PI * 2);
                ctx.fill();

                // 붉게 일렁이는 눈
                ctx.fillStyle = g.stun > 0 ? '#ffffff' : '#ff0000';
                ctx.shadowColor = '#ff0000';
                ctx.shadowBlur = 15;
                ctx.beginPath();
                ctx.arc(sx - size/12, topY + size/3, size/25, 0, Math.PI * 2);
                ctx.arc(sx + size/12, topY + size/3, size/25, 0, Math.PI * 2);
                ctx.fill();
                
                // 찢어진 입
                ctx.strokeStyle = '#600000';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.arc(sx, topY + size/2.2, size/15, 0, Math.PI);
                ctx.stroke();

                ctx.restore();
            }
        }
    });

    // 무기 (녹슨 단검) 휘두르기 렌더링
    if (items.knife) {
        ctx.save();
        let attackOffset = isAttacking * 12;
        ctx.fillStyle = '#888';
        ctx.strokeStyle = '#400';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(canvas.width/2 + 90 - attackOffset, canvas.height - attackOffset);
        ctx.lineTo(canvas.width/2 + 150 - attackOffset, canvas.height - 140 - attackOffset);
        ctx.lineTo(canvas.width/2 + 180 - attackOffset, canvas.height - 110 - attackOffset);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        ctx.restore();
    }

    renderMinimap();
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

components.html(game_html, height=580)
