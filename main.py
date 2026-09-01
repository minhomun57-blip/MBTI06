import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="낡은 집에서의 탈출 - 3D", layout="wide")

st.title("🏚️ 낡은 집에서의 탈출 (Old House Escape)")
st.caption("화면 클릭 후 영문 상태에서 조작 | W: 전진 | S: 후진 | A: 좌측 | D: 우측 | E (꾹 누르기): 달리기 | 마우스: 회전")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background-color: #000; font-family: sans-serif; user-select: none; }
        #canvas { width: 100%; height: 530px; display: block; cursor: pointer; }
        
        /* UI 및 게이지 바 스타일 */
        #ui { position: absolute; top: 15px; left: 15px; color: white; text-shadow: 1px 1px 3px black; font-size: 14px; display: flex; flex-direction: column; gap: 8px; }
        .bar-container { width: 180px; height: 16px; background: rgba(255,255,255,0.2); border: 2px solid #333; border-radius: 8px; overflow: hidden; }
        .bar-fill { height: 100%; width: 100%; transition: width 0.1s linear; }
        #hp-bar { background: linear-gradient(90deg, #ff3333, #ff6666); }
        #stamina-bar { background: linear-gradient(90deg, #33cc33, #66ff66); }

        #inventory { position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; }
        .slot { width: 55px; height: 55px; border: 2px solid #555; background: rgba(0,0,0,0.8); color: white; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; border-radius: 5px; text-align: center; }
        #msg { position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); color: red; font-size: 32px; font-weight: bold; text-align: center; text-shadow: 2px 2px 5px black; }
        #room-info { position: absolute; top: 15px; right: 15px; color: #aaa; font-size: 14px; text-align: right; }
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
        <div style="color:gold; font-weight:bold;">장소: 낡은 집 안채</div>
        <div>목표: 가구 사이를 수색해 열쇠를 찾고 탈출하라</div>
    </div>
    
    <div id="inventory">
        <div class="slot" id="slot1">[1]<br>회복약</div>
        <div class="slot" id="slot2">[2]<br>배터리</div>
        <div class="slot" id="slot3">[3]<br>부적</div>
        <div class="slot" id="slot4">[4]<br>녹슨 열쇠</div>
    </div>

    <div id="msg">화면을 클릭하면 게임이 시작됩니다.</div>
    <canvas id="canvas"></canvas>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 530;

// 낡은 집 맵 구조 (0: 길, 1: 벽, 2: 열쇠, 3: 출구, 4: 단검, 5: 포션, 6: 배터리, 7~9: 가구)
const houseMap = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,7,0,0,1,8,0,0,1,9,0,0,4,0,1],
    [1,7,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,1,5,0,0,0,7,0,0,0,8,1,0,1],
    [1,0,1,0,0,0,0,7,0,0,0,0,1,0,1],
    [1,0,0,0,9,0,0,0,0,0,6,0,0,0,1],
    [1,0,1,0,0,0,0,8,0,0,0,0,1,0,1],
    [1,0,1,6,0,0,0,8,0,0,0,5,1,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,9,0,0,1,0,0,0,1,0,0,0,7,0,1],
    [1,0,0,0,1,3,1,0,1,0,0,0,7,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
];

let px = 7.5, py = 7.5;
let angle = 0;
let hp = 100;
let stamina = 100;
let flashRange = 10;
let gameOver = false;

let items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
let isAttacking = 0;

// 선명한 붉은빛의 귀신
let ghosts = [
    { x: 3.5, y: 3.5, hp: 80, stun: 0 },
    { x: 11.5, y: 11.5, hp: 80, stun: 0 }
];

const keys = {};

// 키 입력 리스너 (대소문자 및 한글 입력 방지)
window.addEventListener('keydown', e => {
    let k = e.key.toLowerCase();
    if (k === 'ㄷ') k = 'w';
    if (k === 'ㄴ') k = 's';
    if (k === 'ㅁ') k = 'a';
    if (k === 'ㅇ') k = 'd';
    if (k === 'ㄷ') k = 'e';
    keys[k] = true;
    
    if (e.key === '1' && items.potion > 0) {
        hp = Math.min(100, hp + 50);
        items.potion--;
        updateUI();
    }
    if (e.key === '2' && items.battery > 0) {
        flashRange = 14;
        items.battery--;
        updateUI();
    }
    if (e.key === '3' && items.talisman > 0) {
        ghosts.forEach(g => g.stun = 180);
        items.talisman--;
        updateUI();
    }
});

window.addEventListener('keyup', e => {
    let k = e.key.toLowerCase();
    if (k === 'ㄷ') k = 'w';
    if (k === 'ㄴ') k = 's';
    if (k === 'ㅁ') k = 'a';
    if (k === 'ㅇ') k = 'd';
    if (k === 'ㄷ') k = 'e';
    keys[k] = false;
});

canvas.addEventListener('click', () => {
    if (document.pointerLockElement !== canvas) {
        canvas.requestPointerLock();
        document.getElementById('msg').innerText = "";
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
    // 체력 및 스테미나 바 업데이트
    document.getElementById('hp-bar').style.width = Math.max(0, hp) + "%";
    document.getElementById('stamina-bar').style.width = Math.max(0, stamina) + "%";
    
    document.getElementById('weapon').innerText = items.knife ? "녹슨 단검 (클릭: 공격)" : "맨손";
    
    document.getElementById('slot1').style.borderColor = items.potion > 0 ? "lime" : "#555";
    document.getElementById('slot2').style.borderColor = items.battery > 0 ? "yellow" : "#555";
    document.getElementById('slot3').style.borderColor = items.talisman > 0 ? "cyan" : "#555";
    document.getElementById('slot4').style.borderColor = items.key ? "gold" : "#555";
}

function isSolid(x, y) {
    let cell = houseMap[Math.floor(y)][Math.floor(x)];
    return cell === 1 || cell === 7 || cell === 8 || cell === 9;
}

function update() {
    if (gameOver) return;

    // E 키 누르고 있을 때만 달리기 적용 및 스테미나 0.5 감소
    let speed = 0.04;
    let isMoving = keys['w'] || keys['s'] || keys['a'] || keys['d'];

    if (keys['e'] && isMoving && stamina >= 0.5) {
        speed = 0.08;
        stamina = Math.max(0, stamina - 0.5); // 달릴 때만 0.5 차감
    } else {
        stamina = Math.min(100, stamina + 0.1); // 안 달릴 땐 서서히 회복 (걸을 때 차감 안됨)
    }

    // W, S, A, D 이동
    let dx = 0, dy = 0;
    if (keys['w']) { dx += Math.cos(angle) * speed; dy += Math.sin(angle) * speed; }
    if (keys['s']) { dx -= Math.cos(angle) * speed; dy -= Math.sin(angle) * speed; }
    if (keys['a']) { dx += Math.sin(angle) * speed; dy -= Math.cos(angle) * speed; }
    if (keys['d']) { dx -= Math.sin(angle) * speed; dy += Math.cos(angle) * speed; }

    if (!isSolid(px + dx, py)) px += dx;
    if (!isSolid(px, py + dy)) py += dy;

    // 아이템 수집
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

    // 귀신 추격 AI
    ghosts.forEach(g => {
        if (g.hp <= 0) return;
        if (g.stun > 0) {
            g.stun--;
        } else {
            let gdx = px - g.x, gdy = py - g.y;
            let dist = Math.sqrt(gdx*gdx + gdy*gdy);
            if (dist > 0.1) {
                g.x += (gdx / dist) * 0.02;
                g.y += (gdy / dist) * 0.02;
            }
            if (dist < 0.6) {
                hp -= 1.2;
                if (hp <= 0) {
                    gameOver = true;
                    document.getElementById('msg').innerText = "💀 낡은 집의 원혼에게 붙잡혔습니다...";
                }
            }
        }
    });

    if (isAttacking > 0) isAttacking--;
}

function renderFurniture(type, sx, canvasHeight, size) {
    ctx.save();
    if (type === 7) {
        ctx.fillStyle = '#4a2e18';
        ctx.fillRect(sx - size/2, canvasHeight/2, size, size/2);
    } else if (type === 8) {
        ctx.fillStyle = '#3d2514';
        ctx.fillRect(sx - size/2, canvasHeight/2 + size/6, size, size/3);
    } else if (type === 9) {
        ctx.fillStyle = '#2b1a0e';
        ctx.fillRect(sx - size/3, canvasHeight/2 - size/6, size/1.5, size/1.2);
    }
    ctx.restore();
}

function render() {
    ctx.fillStyle = '#080604';
    ctx.fillRect(0, 0, canvas.width, canvas.height/2);
    ctx.fillStyle = '#120d08';
    ctx.fillRect(0, canvas.height/2, canvas.width, canvas.height/2);

    const fov = Math.PI / 3;
    const numRays = 130;
    const w = canvas.width / numRays;

    for (let i = 0; i < numRays; i++) {
        let rayAngle = (angle - fov / 2) + (i / numRays) * fov;
        let distance = 0;
        let hit = false;
        let hitType = 1;

        while (!hit && distance < flashRange) {
            distance += 0.05;
            let tx = Math.floor(px + Math.cos(rayAngle) * distance);
            let ty = Math.floor(py + Math.sin(rayAngle) * distance);

            if (tx < 0 || tx >= 15 || ty < 0 || ty >= 15) {
                hit = true;
                hitType = 1;
            } else if (isSolid(tx, ty)) {
                hit = true;
                hitType = houseMap[ty][tx];
            }
        }

        let correctedDist = distance * Math.cos(rayAngle - angle);
        let h = Math.min(canvas.height, canvas.height / (correctedDist + 0.0001));
        let shade = Math.max(0, Math.floor(160 - correctedDist * (160 / flashRange)));

        if (hitType === 1) {
            ctx.fillStyle = `rgb(${shade}, ${Math.floor(shade*0.4)}, ${Math.floor(shade*0.2)})`;
        } else {
            ctx.fillStyle = `rgb(${Math.floor(shade*0.6)}, ${Math.floor(shade*0.3)}, ${Math.floor(shade*0.1)})`;
        }
        ctx.fillRect(i * w, (canvas.height - h) / 2, w + 1, h);
    }

    // 가구 렌더링
    for (let y = 0; y < 15; y++) {
        for (let x = 0; x < 15; x++) {
            let cell = houseMap[y][x];
            if (cell >= 7 && cell <= 9) {
                let fdx = (x + 0.5) - px;
                let fdy = (y + 0.5) - py;
                let fDist = Math.sqrt(fdx*fdx + fdy*fdy);
                let fAngle = Math.atan2(fdy, fdx) - angle;

                while (fAngle < -Math.PI) fAngle += 2 * Math.PI;
                while (fAngle > Math.PI) fAngle -= 2 * Math.PI;

                if (Math.abs(fAngle) < fov / 2 && fDist < flashRange) {
                    let sx = (canvas.width / 2) + Math.tan(fAngle) * (canvas.width / 2);
                    let size = Math.min(280, canvas.height / fDist);
                    renderFurniture(cell, sx, canvas.height, size);
                }
            }
        }
    }

    // 선명하게 가시화된 붉은 유령(귀신)
    ghosts.forEach(g => {
        if (g.hp <= 0) return;
        let gdx = g.x - px, gdy = g.y - py;
        let gDist = Math.sqrt(gdx*gdx + gdy*gdy);
        let gAngle = Math.atan2(gdy, gdx) - angle;

        while (gAngle < -Math.PI) gAngle += 2 * Math.PI;
        while (gAngle > Math.PI) gAngle -= 2 * Math.PI;

        if (Math.abs(gAngle) < fov / 2 && gDist < flashRange) {
            let sx = (canvas.width / 2) + Math.tan(gAngle) * (canvas.width / 2);
            let size = Math.min(380, canvas.height / gDist);

            ctx.save();
            // 귀신 몸통 (붉은 발광체)
            ctx.fillStyle = g.stun > 0 ? '#00ffff' : '#ff1a1a';
            ctx.beginPath();
            ctx.arc(sx, canvas.height/2 - size/6, size/2.5, 0, Math.PI * 2);
            ctx.fill();

            // 유령 눈빛
            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(sx - size/8, canvas.height/2 - size/4, size/12, 0, Math.PI * 2);
            ctx.arc(sx + size/8, canvas.height/2 - size/4, size/12, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
    });

    // 공격 무기
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
