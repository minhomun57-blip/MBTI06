import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="낡은 집에서의 탈출 - 3D", layout="wide")

st.title("🏚️ 낡은 집에서의 탈출 (Old House Escape)")
st.caption("조작 방법 | W/S/A/D: 이동 | ← / → (방향키): 시점 회전 | E: 달리기 | 1,2,3,4: 아이템 사용 | 마우스 클릭: 공격")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background-color: #000; font-family: sans-serif; user-select: none; }
        #canvas { width: 100%; height: 530px; display: block; cursor: pointer; }
        
        #ui { position: absolute; top: 15px; left: 15px; color: white; text-shadow: 1px 1px 3px black; font-size: 14px; display: flex; flex-direction: column; gap: 8px; z-index: 5; }
        .bar-container { width: 180px; height: 16px; background: rgba(255,255,255,0.15); border: 2px solid #444; border-radius: 8px; overflow: hidden; }
        .bar-fill { height: 100%; width: 100%; transition: width 0.1s linear; }
        #hp-bar { background: linear-gradient(90deg, #cc0000, #ff4d4d); }
        #stamina-bar { background: linear-gradient(90deg, #28a745, #5cdb5c); }

        /* 인벤토리를 우측 하단으로 이동 */
        #inventory { position: absolute; bottom: 15px; right: 15px; display: flex; gap: 8px; z-index: 5; }
        .slot { width: 60px; height: 60px; border: 2px solid #444; background: rgba(0,0,0,0.85); color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; border-radius: 6px; text-align: center; }
        .slot-key { color: #ffcc00; font-size: 10px; margin-bottom: 2px; }

        #msg { position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); color: red; font-size: 28px; font-weight: bold; text-align: center; text-shadow: 2px 2px 5px black; z-index: 5; }
        #room-info { position: absolute; top: 15px; right: 15px; color: #aaa; font-size: 14px; text-align: right; z-index: 5; }

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
            width: 320px;
            height: 320px;
            background: radial-gradient(circle, #ff0000 0%, #330000 70%, #000000 100%);
            border-radius: 50%;
            position: relative;
            box-shadow: 0 0 60px #ff0000;
            animation: shake 0.05s infinite alternate;
        }
        .eye {
            position: absolute;
            top: 35%;
            width: 70px;
            height: 70px;
            background: #fff;
            border-radius: 50%;
            box-shadow: inset 0 0 15px #000;
        }
        .eye.left { left: 20%; }
        .eye.right { right: 20%; }
        .pupil {
            position: absolute;
            top: 25%; left: 25%;
            width: 35px; height: 35px;
            background: #000;
            border-radius: 50%;
            box-shadow: 0 0 10px #ff0000;
        }
        .mouth {
            position: absolute;
            bottom: 15%; left: 20%;
            width: 60%; height: 90px;
            background: #000;
            border-radius: 0 0 50px 50px;
            border: 4px solid #880000;
        }
        #scare-text {
            color: #ff0000;
            font-size: 36px;
            font-weight: 900;
            margin-top: 20px;
            text-shadow: 0 0 10px #ff0000;
        }

        @keyframes shake {
            0% { transform: translate(4px, 4px) scale(1.1); }
            100% { transform: translate(-4px, -4px) scale(1.15); }
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
    
    <!-- 오른쪽 하단 인벤토리 -->
    <div id="inventory">
        <div class="slot" id="slot1"><span class="slot-key">[1]</span>회복약<br><span id="cnt-potion">0</span></div>
        <div class="slot" id="slot2"><span class="slot-key">[2]</span>배터리<br><span id="cnt-battery">0</span></div>
        <div class="slot" id="slot3"><span class="slot-key">[3]</span>부적<br><span id="cnt-talisman">1</span></div>
        <div class="slot" id="slot4"><span class="slot-key">[4]</span>열쇠<br><span id="cnt-key">X</span></div>
    </div>

    <div id="msg">게임 화면을 클릭해 시작하세요</div>
    <div id="jumpscare">
        <div id="scare-face">
            <div class="eye left"><div class="pupil"></div></div>
            <div class="eye right"><div class="pupil"></div></div>
            <div class="mouth"></div>
        </div>
        <div id="scare-text">💀 원혼에게 붙잡혔습니다! 💀</div>
    </div>
    <canvas id="canvas"></canvas>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 530;

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

let px = 7.5, py = 7.5;
let angle = 0;
let hp = 100;
let stamina = 100;
let flashRange = 10;
let gameOver = false;

let items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
let isAttacking = 0;

let ghosts = [
    { x: 1.5, y: 1.5, hp: 80, stun: 0 },
    { x: 13.5, y: 13.5, hp: 80, stun: 0 }
];

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

// 1, 2, 3, 4 키 아이템 사용
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
    if (e.key === '4' && items.key) {
        document.getElementById('msg').innerText = "🔑 열쇠를 준비했습니다. 탈출구(3)로 가세요!";
        setTimeout(() => { if (!gameOver) document.getElementById('msg').innerText = ""; }, 2000);
    }
});

window.addEventListener('keyup', e => {
    let k = parseKey(e.key);
    keys[k] = false;
});

canvas.addEventListener('click', () => {
    document.getElementById('msg').innerText = "";
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
                g.x += (gdx / dist) * 0.007;
                g.y += (gdy / dist) * 0.007;
            }
            if (dist < 0.6) {
                hp -= 2.0;
                if (hp <= 0) {
                    triggerJumpscare();
                }
            }
        }
    });

    if (isAttacking > 0) isAttacking--;
}

function renderFurniture(type, sx, canvasHeight, size) {
    ctx.save();
    if (type === 7) {
        ctx.fillStyle = '#3a200d';
        ctx.fillRect(sx - size/2, canvasHeight/2, size, size/2);
        ctx.fillStyle = '#221307';
        ctx.fillRect(sx - size/2, canvasHeight/2 + size/4, size, size/8);
    } else if (type === 8) {
        ctx.fillStyle = '#2e1c0c';
        ctx.fillRect(sx - size/2, canvasHeight/2 + size/6, size, size/3);
    } else if (type === 9) {
        ctx.fillStyle = '#221208';
        ctx.fillRect(sx - size/3, canvasHeight/2 - size/6, size/1.5, size/1.2);
    } else if (type === 10) {
        ctx.fillStyle = '#422814';
        ctx.fillRect(sx - size/4, canvasHeight/2 + size/8, size/2, size/2);
    } else if (type === 11) {
        ctx.fillStyle = '#170c05';
        ctx.fillRect(sx - size/2.5, canvasHeight/2 - size/2, size/1.25, size);
    }
    ctx.restore();
}

function renderGhost(sx, canvasHeight, size, isStunned) {
    ctx.save();
    let topY = canvasHeight / 2 - size / 2;

    // 검은 로브/후드 실루엣
    ctx.fillStyle = isStunned ? '#1a3a3a' : '#0a0a0d';
    ctx.beginPath();
    ctx.moveTo(sx, topY); 
    ctx.quadraticCurveTo(sx + size/2, topY + size/4, sx + size/3, topY + size);
    ctx.lineTo(sx - size/3, topY + size);
    ctx.quadraticCurveTo(sx - size/2, topY + size/4, sx, topY);
    ctx.fill();

    // 얼굴 내부의 짙은 어둠
    ctx.fillStyle = '#000000';
    ctx.beginPath();
    ctx.ellipse(sx, topY + size/3, size/6, size/4, 0, 0, Math.PI * 2);
    ctx.fill();

    // 붉게 빛나는 눈동자 (스턴 시 청록색)
    ctx.fillStyle = isStunned ? '#00ffff' : '#ff0000';
    ctx.shadowColor = isStunned ? '#00ffff' : '#ff0000';
    ctx.shadowBlur = 15;

    ctx.beginPath();
    ctx.arc(sx - size/12, topY + size/3.2, size/28, 0, Math.PI * 2);
    ctx.arc(sx + size/12, topY + size/3.2, size/28, 0, Math.PI * 2);
    ctx.fill();

    // 스턴 시 안개/아우라 연출
    if (isStunned) {
        ctx.strokeStyle = 'rgba(0, 255, 255, 0.5)';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(sx, topY + size/3, size/3, 0, Math.PI * 2);
        ctx.stroke();
    }

    ctx.restore();
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
        let hitX = 0, hitY = 0;

        while (!hit && distance < flashRange) {
            distance += 0.04;
            let rx = px + Math.cos(rayAngle) * distance;
            let ry = py + Math.sin(rayAngle) * distance;
            let tx = Math.floor(rx);
            let ty = Math.floor(ry);

            if (tx < 0 || tx >= 15 || ty < 0 || ty >= 15) {
                hit = true;
                hitType = 1;
            } else if (isSolid(tx, ty)) {
                hit = true;
                hitType = houseMap[ty][tx];
                hitX = rx - tx;
                hitY = ry - ty;
            }
        }

        let correctedDist = distance * Math.cos(rayAngle - angle);
        let h = Math.min(canvas.height, canvas.height / (correctedDist + 0.0001));
        let shade = Math.max(0, Math.floor(180 - correctedDist * (180 / flashRange)));

        let edge = (hitX < 0.05 || hitX > 0.95 || hitY < 0.05 || hitY > 0.95) ? 0.7 : 1.0;
        let r = Math.floor(shade * 0.5 * edge);
        let g = Math.floor(shade * 0.25 * edge);
        let b = Math.floor(shade * 0.15 * edge);

        if (hitType === 1) {
            ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
        } else {
            ctx.fillStyle = `rgb(${Math.floor(r*0.7)}, ${Math.floor(g*0.7)}, ${Math.floor(b*0.7)})`;
        }
        
        let topY = (canvas.height - h) / 2;
        ctx.fillRect(i * w, topY, w + 1, h);

        ctx.fillStyle = `rgba(0,0,0,${Math.min(1, correctedDist/8)})`;
        ctx.fillRect(i * w, topY + h - (h*0.1), w + 1, h*0.1);
    }

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

    // 새로운 귀신 비주얼 렌더링
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
            renderGhost(sx, canvas.height, size, g.stun > 0);
        }
    });

    if (items.knife) {
        ctx.save();
        let attackOffset = isAttacking * 9;
        ctx.fillStyle = '#ccc';
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
