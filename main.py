import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="낡은 집에서의 탈출 - 3D", layout="wide")

st.title("🏚️ 낡은 집에서의 탈출 (Old House Escape)")
st.caption("화면 클릭 후 조작 | W(ㅈ): 전진 | S(ㄴ): 후진 | A(ㅁ): 좌측 | D(ㅇ): 우측 | E(ㄷ) 꾹 누르기: 달리기")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background-color: #000; font-family: sans-serif; user-select: none; }
        #canvas { width: 100%; height: 530px; display: block; cursor: pointer; }
        
        #ui { position: absolute; top: 15px; left: 15px; color: white; text-shadow: 1px 1px 3px black; font-size: 14px; display: flex; flex-direction: column; gap: 8px; }
        .bar-container { width: 180px; height: 16px; background: rgba(255,255,255,0.2); border: 2px solid #333; border-radius: 8px; overflow: hidden; }
        .bar-fill { height: 100%; width: 100%; transition: width 0.1s linear; }
        #hp-bar { background: linear-gradient(90deg, #ff3333, #ff6666); }
        #stamina-bar { background: linear-gradient(90deg, #33cc33, #66ff66); }

        #inventory { position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; }
        .slot { width: 55px; height: 55px; border: 2px solid #555; background: rgba(0,0,0,0.8); color: white; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; border-radius: 5px; text-align: center; }
        #msg { position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); color: red; font-size: 28px; font-weight: bold; text-align: center; text-shadow: 2px 2px 5px black; }
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

    <div id="msg">클릭하여 시작하세요</div>
    <canvas id="canvas"></canvas>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 530;

// 0: 길, 1: 벽, 2: 열쇠, 3: 출구, 4: 단검, 5: 포션, 6: 배터리
// 7: 침대, 8: 책상, 9: 서랍장, 10: 의자, 11: 옷장
const houseMap = [
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

// 플레이어 시작 위치 (중앙 안전 지대)
let px = 7.5, py = 7.5;
let angle = 0;
let hp = 100;
let stamina = 100;
let flashRange = 10;
let gameOver = false;

let items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
let isAttacking = 0;

// 귀신 스폰 위치를 플레이어와 멀리 떨어진 구석으로 수정
let ghosts = [
    { x: 1.5, y: 1.5, hp: 80, stun: 0 },
    { x: 13.5, y: 13.5, hp: 80, stun: 0 }
];

const keys = {};

// 키보드 입력을 영어 및 한글 조합에 맞춰 변환
function parseKey(k) {
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
    let k = parseKey(e.key);
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
    // 벽(1) 및 모든 가구(7~11) 충돌 처리
    return cell === 1 || (cell >= 7 && cell <= 11);
}

function update() {
    if (gameOver) return;

    let speed = 0.04;
    let isMoving = keys['w'] || keys['s'] || keys['a'] || keys['d'];

    // E키 누르고 이동 시만 달리기 적용
    if (keys['e'] && isMoving && stamina >= 0.5) {
        speed = 0.08;
        stamina = Math.max(0, stamina - 0.5);
    } else {
        stamina = Math.min(100, stamina + 0.1);
    }

    let dx = 0, dy = 0;
    if (keys['w']) { dx += Math.cos(angle) * speed; dy += Math.sin(angle) * speed; }
    if (keys['s']) { dx -= Math.cos(angle) * speed; dy -= Math.sin(angle) * speed; }
    if (keys['a']) { dx += Math.sin(angle) * speed; dy -= Math.cos(angle) * speed; }
    if (keys['d']) { dx -= Math.sin(angle) * speed; dy += Math.cos(angle) * speed; }

    if (!isSolid(px + dx, py)) px += dx;
    if (!isSolid(px, py + dy)) py += dy;

    // 아이템 습득 처리
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
                g.x += (gdx / dist) * 0.018;
                g.y += (gdy / dist) * 0.018;
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
        // 침대
        ctx.fillStyle = '#4a2e18';
        ctx.fillRect(sx - size/2, canvasHeight/2, size, size/2);
    } else if (type === 8) {
        // 책상
        ctx.fillStyle = '#3d2514';
        ctx.fillRect(sx - size/2, canvasHeight/2 + size/6, size, size/3);
    } else if (type === 9) {
        // 서랍장
        ctx.fillStyle = '#2b1a0e';
        ctx.fillRect(sx - size/3, canvasHeight/2 - size/6, size/1.5, size/1.2);
    } else if (type === 10) {
        // 의자
        ctx.fillStyle = '#5c3a21';
        ctx.fillRect(sx - size/4, canvasHeight/2 + size/8, size/2, size/2);
    } else if (type === 11) {
        // 대형 옷장
        ctx.fillStyle = '#1f1208';
        ctx.fillRect(sx - size/2.5, canvasHeight/2 - size/2, size/1.25, size);
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

    // 다양한 가구 오브젝트 렌더링
    for (let y = 0; y < 15; y++) {
        for (let x = 0; x < 15; x++) {
            let cell = houseMap[y][x];
            if (cell >= 7 && cell <= 11) {
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

    // 붉은 발광 유령(귀신)
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
            ctx.fillStyle = g.stun > 0 ? '#00ffff' : '#ff1a1a';
            ctx.beginPath();
            ctx.arc(sx, canvas.height/2 - size/6, size/2.5, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(sx - size/8, canvas.height/2 - size/4, size/12, 0, Math.PI * 2);
            ctx.arc(sx + size/8, canvas.height/2 - size/4, size/12, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
    });

    // 무기 애니메이션
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
