import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="저택 탈출: 3D 공포 생존", layout="wide")

st.title("🏰 저택 탈출 (3D Horror Mansion)")
st.caption("WASD: 이동 | 마우스: 시점 회전 | 클릭: 단검 공격 | 1~3: 아이템 사용 | Shift: 달리기")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background-color: #000; font-family: sans-serif; user-select: none; }
        #canvas { width: 100%; height: 530px; display: block; }
        #ui { position: absolute; top: 10px; left: 10px; color: white; text-shadow: 1px 1px 3px black; font-size: 15px; }
        #inventory { position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; }
        .slot { width: 55px; height: 55px; border: 2px solid #555; background: rgba(0,0,0,0.8); color: white; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; border-radius: 5px; text-align: center; }
        #msg { position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); color: red; font-size: 32px; font-weight: bold; text-align: center; text-shadow: 2px 2px 5px black; }
        #room-info { position: absolute; top: 10px; right: 10px; color: #aaa; font-size: 14px; text-align: right; }
    </style>
</head>
<body>
    <div id="ui">
        <div>체력: <span id="hp" style="color:#ff4d4d;">100</span> / 100</div>
        <div>스테미나: <span id="stamina" style="color:#55ff55;">100</span>%</div>
        <div>장착 무기: <span id="weapon" style="color:#00ffff;">맨손</span></div>
    </div>

    <div id="room-info">
        <div id="location" style="color:gold; font-weight:bold;">위치: 저택 중앙 홀</div>
        <div id="mission">목표: 서재와 침실에서 열쇠를 찾아 대문을 열어라</div>
    </div>
    
    <div id="inventory">
        <div class="slot" id="slot1">[1]<br>회복약</div>
        <div class="slot" id="slot2">[2]<br>배터리</div>
        <div class="slot" id="slot3">[3]<br>부적</div>
        <div class="slot" id="slot4">[4]<br>저택 열쇠</div>
    </div>

    <div id="msg"></div>
    <canvas id="canvas"></canvas>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 530;

// 저택 맵 구조 (1: 벽, 0: 복도, 2: 저택 열쇠, 4: 단검, 5: 회복약, 6: 배터리, 3: 저택 대문)
const mansionMap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,5,0,0,1,0,0,0,1,0,0,0,4,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,1,2,1,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
    [1,6,0,0,0,0,0,0,0,0,0,0,0,5,1],
    [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,1,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,6,0,1,3,1,0,0,0,0,0,6,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

// 플레이어 상태
let px = 7.5, py = 7.5;
let angle = 0;
let hp = 100;
let stamina = 100;
let flashRange = 9;
let gameOver = false;

// 아이템 및 무기
let items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
let isAttacking = 0;

// 저택 귀신 AI (유령)
let ghosts = [
    { x: 2.5, y: 2.5, hp: 80, stun: 0 },
    { x: 12.5, y: 11.5, hp: 80, stun: 0 }
];

// 키 입력 & 조작
const keys = {};
window.addEventListener('keydown', e => {
    keys[e.key.toLowerCase()] = true;
    
    if (e.key === '1' && items.potion > 0) {
        hp = Math.min(100, hp + 50);
        items.potion--;
        updateUI();
    }
    if (e.key === '2' && items.battery > 0) {
        flashRange = 12;
        items.battery--;
        updateUI();
    }
    if (e.key === '3' && items.talisman > 0) {
        ghosts.forEach(g => g.stun = 180); // 모든 귀신 6초 마비
        items.talisman--;
        updateUI();
    }
});
window.addEventListener('keyup', e => keys[e.key.toLowerCase()] = false);

// 마우스 공격
canvas.addEventListener('click', () => {
    if (document.pointerLockElement !== canvas) {
        canvas.requestPointerLock();
    } else if (items.knife && isAttacking === 0 && !gameOver) {
        isAttacking = 10;
        checkAttackHit();
    }
});

window.addEventListener('mousemove', e => {
    if (document.pointerLockElement === canvas && !gameOver) {
        angle += e.movementX * 0.003;
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

        if (dist < 1.8 && Math.abs(gAngle) < 0.5) {
            g.hp -= 40;
            g.stun = 35;
        }
    });
}

function updateUI() {
    document.getElementById('hp').innerText = Math.max(0, Math.floor(hp));
    document.getElementById('stamina').innerText = Math.floor(stamina);
    document.getElementById('weapon').innerText = items.knife ? "은 단검 (클릭: 공격)" : "맨손";
    
    document.getElementById('slot1').style.borderColor = items.potion > 0 ? "lime" : "#555";
    document.getElementById('slot2').style.borderColor = items.battery > 0 ? "yellow" : "#555";
    document.getElementById('slot3').style.borderColor = items.talisman > 0 ? "cyan" : "#555";
    document.getElementById('slot4').style.borderColor = items.key ? "gold" : "#555";
}

function update() {
    if (gameOver) return;

    // 이동 처리
    let speed = 0.045;
    if (keys['shift'] && stamina > 5) {
        speed = 0.085;
        stamina = Math.max(0, stamina - 0.7);
    } else {
        stamina = Math.min(100, stamina + 0.25);
    }

    let dx = 0, dy = 0;
    if (keys['w']) { dx += Math.cos(angle) * speed; dy += Math.sin(angle) * speed; }
    if (keys['s']) { dx -= Math.cos(angle) * speed; dy -= Math.sin(angle) * speed; }
    if (keys['a']) { dx += Math.sin(angle) * speed; dy -= Math.cos(angle) * speed; }
    if (keys['d']) { dx -= Math.sin(angle) * speed; dy += Math.cos(angle) * speed; }

    if (mansionMap[Math.floor(py)][Math.floor(px + dx)] === 0) px += dx;
    if (mansionMap[Math.floor(py + dy)][Math.floor(px)] === 0) py += dy;

    // 습득 로직
    let ix = Math.floor(px), iy = Math.floor(py);
    let cell = mansionMap[iy][ix];
    if (cell === 2) { items.key = true; mansionMap[iy][ix] = 0; }
    else if (cell === 4) { items.knife = true; mansionMap[iy][ix] = 0; }
    else if (cell === 5) { items.potion++; mansionMap[iy][ix] = 0; }
    else if (cell === 6) { items.battery++; mansionMap[iy][ix] = 0; }
    else if (cell === 3 && items.key) {
        gameOver = true;
        document.getElementById('msg').innerText = "🏰 저택의 대문을 열고 탈출에 성공했습니다!";
        document.getElementById('msg').style.color = "gold";
    }
    updateUI();

    // 귀신 AI 추격
    ghosts.forEach(g => {
        if (g.hp <= 0) return;
        if (g.stun > 0) {
            g.stun--;
        } else {
            let gdx = px - g.x, gdy = py - g.y;
            let dist = Math.sqrt(gdx*gdx + gdy*gdy);
            if (dist > 0.1) {
                g.x += (gdx / dist) * 0.024;
                g.y += (gdy / dist) * 0.024;
            }
            if (dist < 0.6) {
                hp -= 1.8;
                if (hp <= 0) {
                    gameOver = true;
                    document.getElementById('msg').innerText = "💀 저택의 귀신에게 잡혔습니다...";
                }
            }
        }
    });

    if (isAttacking > 0) isAttacking--;
}

function render() {
    ctx.fillStyle = '#050508';
    ctx.fillRect(0, 0, canvas.width, canvas.height/2);
    ctx.fillStyle = '#0f0d13';
    ctx.fillRect(0, canvas.height/2, canvas.width, canvas.height/2);

    const fov = Math.PI / 3;
    const numRays = 130;
    const w = canvas.width / numRays;

    // 3D 저택 복도 레이캐스팅
    for (let i = 0; i < numRays; i++) {
        let rayAngle = (angle - fov / 2) + (i / numRays) * fov;
        let distance = 0;
        let hit = false;

        while (!hit && distance < flashRange) {
            distance += 0.05;
            let tx = Math.floor(px + Math.cos(rayAngle) * distance);
            let ty = Math.floor(py + Math.sin(rayAngle) * distance);

            if (tx < 0 || tx >= 15 || ty < 0 || ty >= 15 || mansionMap[ty][tx] === 1) {
                hit = true;
            }
        }

        let correctedDist = distance * Math.cos(rayAngle - angle);
        let h = Math.min(canvas.height, canvas.height / (correctedDist + 0.0001));
        let shade = Math.max(0, Math.floor(180 - correctedDist * (180 / flashRange)));

        // 저택 특유의 고풍스러운 벽면 색상
        ctx.fillStyle = `rgb(${shade}, ${Math.floor(shade*0.3)}, ${Math.floor(shade*0.2)})`;
        ctx.fillRect(i * w, (canvas.height - h) / 2, w + 1, h);
    }

    // 3D 유령(귀신) 렌더링
    ghosts.forEach(g => {
        if (g.hp <= 0) return;
        let gdx = g.x - px, gdy = g.y - py;
        let gDist = Math.sqrt(gdx*gdx + gdy*gdy);
        let gAngle = Math.atan2(gdy, gdx) - angle;

        while (gAngle < -Math.PI) gAngle += 2 * Math.PI;
        while (gAngle > Math.PI) gAngle -= 2 * Math.PI;

        if (Math.abs(gAngle) < fov / 2 && gDist < flashRange) {
            let sx = (canvas.width / 2) + Math.tan(gAngle) * (canvas.width / 2);
            let size = Math.min(320, canvas.height / gDist);

            // 기괴한 유령 형상
            ctx.save();
            ctx.fillStyle = g.stun > 0 ? '#44aaww' : 'rgba(220, 220, 240, 0.85)';
            ctx.beginPath();
            ctx.arc(sx, canvas.height/2 - size/6, size/3, 0, Math.PI * 2);
            ctx.fill();

            // 유령 꼬리 연출
            ctx.beginPath();
            ctx.moveTo(sx - size/3, canvas.height/2 - size/6);
            ctx.lineTo(sx + size/3, canvas.height/2 - size/6);
            ctx.lineTo(sx, canvas.height/2 + size/2);
            ctx.fill();

            // 핏빛 눈
            ctx.fillStyle = 'red';
            ctx.beginPath();
            ctx.arc(sx - size/10, canvas.height/2 - size/5, size/18, 0, Math.PI * 2);
            ctx.arc(sx + size/10, canvas.height/2 - size/5, size/18, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
    });

    // 1인칭 무기 애니메이션
    if (items.knife) {
        ctx.save();
        let attackOffset = isAttacking * 9;
        ctx.fillStyle = '#bbb';
        ctx.beginPath();
        ctx.moveTo(canvas.width/2 + 90 - attackOffset, canvas.height - 10 - attackOffset);
        ctx.lineTo(canvas.width/2 + 140 - attackOffset, canvas.height - 130 - attackOffset);
        ctx.lineTo(canvas.width/2 + 160 - attackOffset, canvas.height - 110 - attackOffset);
        ctx.fill();
        ctx.restore();
    }
}

function loop() {
    update();
    render();
    requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
"""

components.html(game_html, height=550)
