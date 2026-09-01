import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="어둠 속의 생존 - 3D 무기 시스템", layout="wide")

st.title("🗡️ 어둠 속의 생존 (3D 아이템 & 무기 시스템)")
st.caption("WASD: 이동 | 마우스: 시점 회전 | 좌클릭: 무기 공격 | 1~3: 아이템 사용 | Shift: 달리기")

game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background-color: #000; font-family: sans-serif; user-select: none; }
        #canvas { width: 100%; height: 520px; display: block; }
        #ui { position: absolute; top: 10px; left: 10px; color: white; text-shadow: 1px 1px 3px black; font-size: 15px; }
        #inventory { position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; }
        .slot { width: 50px; height: 50px; border: 2px solid #555; background: rgba(0,0,0,0.7); color: white; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; border-radius: 5px; }
        .active { border-color: gold; }
        #msg { position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); color: red; font-size: 30px; font-weight: bold; text-align: center; text-shadow: 2px 2px 4px black; }
    </style>
</head>
<body>
    <div id="ui">
        <div>체력: <span id="hp" style="color:red;">100</span> / 100</div>
        <div>스테미나: <span id="stamina" style="color:lightgreen;">100</span>%</div>
        <div>장착 무기: <span id="weapon" style="color:cyan;">맨손</span></div>
    </div>
    
    <div id="inventory">
        <div class="slot" id="slot1">[1]<br>포션</div>
        <div class="slot" id="slot2">[2]<br>건전지</div>
        <div class="slot" id="slot3">[3]<br>부적</div>
        <div class="slot" id="slot4">[4]<br>열쇠</div>
    </div>

    <div id="msg"></div>
    <canvas id="canvas"></canvas>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 520;

// 맵 (1: 벽, 0: 통로, 2: 열쇠, 4: 단검, 5: 체력포션, 6: 배터리, 3: 출구)
const map = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,5,0,1,0,4,0,2,1],
    [1,0,1,0,1,0,1,1,0,1],
    [1,0,1,0,6,0,0,1,0,1],
    [1,0,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,1],
    [1,0,6,0,0,0,5,1,0,1],
    [1,3,1,1,1,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
];

// 플레이어 속성
let px = 2.5, py = 2.5;
let angle = 0;
let hp = 100;
let stamina = 100;
let flashRange = 8;
let gameOver = false;

// 인벤토리 & 무기
let items = { potion: 0, battery: 0, talisman: 1, key: false, knife: false };
let isAttacking = 0; // 공격 애니메이션 타이머

// 귀신 속성
let gx = 7.5, gy = 7.5;
let ghostHp = 100;
let ghostStun = 0;

// 키 입력 & 마우스 조작
const keys = {};
window.addEventListener('keydown', e => {
    keys[e.key.toLowerCase()] = true;
    
    // 아이템 사용 키
    if (e.key === '1' && items.potion > 0) {
        hp = Math.min(100, hp + 40);
        items.potion--;
        updateUI();
    }
    if (e.key === '2' && items.battery > 0) {
        flashRange = 10;
        items.battery--;
        updateUI();
    }
    if (e.key === '3' && items.talisman > 0) {
        ghostStun = 150; // 귀신 5초간 마비
        items.talisman--;
        updateUI();
    }
});
window.addEventListener('keyup', e => keys[e.key.toLowerCase()] = false);

// 마우스 클릭 시 무기 공격
canvas.addEventListener('click', () => {
    if (document.pointerLockElement !== canvas) {
        canvas.requestPointerLock();
    } else if (items.knife && isAttacking === 0 && !gameOver) {
        isAttacking = 10; // 공격 찌르기 모션 시작
        checkAttackHit();
    }
});

window.addEventListener('mousemove', e => {
    if (document.pointerLockElement === canvas && !gameOver) {
        angle += e.movementX * 0.003;
    }
});

function checkAttackHit() {
    let gdx = gx - px, gdy = gy - py;
    let dist = Math.sqrt(gdx*gdx + gdy*gdy);
    let gAngle = Math.atan2(gdy, gdx) - angle;
    while (gAngle < -Math.PI) gAngle += 2 * Math.PI;
    while (gAngle > Math.PI) gAngle -= 2 * Math.PI;

    // 근접거리 내에서 바라보고 공격할 때 타격
    if (dist < 1.8 && Math.abs(gAngle) < 0.5) {
        ghostHp -= 40;
        ghostStun = 30; // 1초간 멈춤
        if (ghostHp <= 0) {
            gx = -10; gy = -10; // 귀신 소멸
        }
    }
}

function updateUI() {
    document.getElementById('hp').innerText = Math.max(0, Math.floor(hp));
    document.getElementById('stamina').innerText = Math.floor(stamina);
    document.getElementById('weapon').innerText = items.knife ? "녹슨 단검 (클릭: 공격)" : "맨손";
    
    document.getElementById('slot1').style.borderColor = items.potion > 0 ? "lime" : "#555";
    document.getElementById('slot2').style.borderColor = items.battery > 0 ? "yellow" : "#555";
    document.getElementById('slot3').style.borderColor = items.talisman > 0 ? "cyan" : "#555";
    document.getElementById('slot4').style.borderColor = items.key ? "gold" : "#555";
}

function update() {
    if (gameOver) return;

    // 이동 처리
    let speed = 0.04;
    if (keys['shift'] && stamina > 5) {
        speed = 0.08;
        stamina = Math.max(0, stamina - 0.6);
    } else {
        stamina = Math.min(100, stamina + 0.2);
    }

    let dx = 0, dy = 0;
    if (keys['w']) { dx += Math.cos(angle) * speed; dy += Math.sin(angle) * speed; }
    if (keys['s']) { dx -= Math.cos(angle) * speed; dy -= Math.sin(angle) * speed; }
    if (keys['a']) { dx += Math.sin(angle) * speed; dy -= Math.cos(angle) * speed; }
    if (keys['d']) { dx -= Math.sin(angle) * speed; dy += Math.cos(angle) * speed; }

    if (map[Math.floor(py)][Math.floor(px + dx)] === 0) px += dx;
    if (map[Math.floor(py + dy)][Math.floor(px)] === 0) py += dy;

    // 맵 아이템 습득
    let ix = Math.floor(px), iy = Math.floor(py);
    let cell = map[iy][ix];
    if (cell === 2) { items.key = true; map[iy][ix] = 0; }
    else if (cell === 4) { items.knife = true; map[iy][ix] = 0; }
    else if (cell === 5) { items.potion++; map[iy][ix] = 0; }
    else if (cell === 6) { items.battery++; map[iy][ix] = 0; }
    else if (cell === 3 && items.key) {
        gameOver = true;
        document.getElementById('msg').innerText = "🏆 생존 성공! 탈출했습니다.";
        document.getElementById('msg').style.color = "cyan";
    }
    updateUI();

    // 귀신 AI
    if (ghostHp > 0) {
        if (ghostStun > 0) {
            ghostStun--;
        } else {
            let gdx = px - gx, gdy = py - gy;
            let dist = Math.sqrt(gdx*gdx + gdy*gdy);
            if (dist > 0.1) {
                gx += (gdx / dist) * 0.022;
                gy += (gdy / dist) * 0.022;
            }
            if (dist < 0.6) {
                hp -= 1.5; // 지속 피해
                if (hp <= 0) {
                    gameOver = true;
                    document.getElementById('msg').innerText = "💀 귀신에게 처단당했습니다...";
                }
            }
        }
    }

    if (isAttacking > 0) isAttacking--;
}

function render() {
    ctx.fillStyle = '#050505';
    ctx.fillRect(0, 0, canvas.width, canvas.height/2);
    ctx.fillStyle = '#111111';
    ctx.fillRect(0, canvas.height/2, canvas.width, canvas.height/2);

    const fov = Math.PI / 3;
    const numRays = 120;
    const w = canvas.width / numRays;

    // 3D 벽 레이캐스팅
    for (let i = 0; i < numRays; i++) {
        let rayAngle = (angle - fov / 2) + (i / numRays) * fov;
        let distance = 0;
        let hit = false;

        while (!hit && distance < flashRange) {
            distance += 0.05;
            let tx = Math.floor(px + Math.cos(rayAngle) * distance);
            let ty = Math.floor(py + Math.sin(rayAngle) * distance);

            if (tx < 0 || tx >= 10 || ty < 0 || ty >= 10 || map[ty][tx] === 1) {
                hit = true;
            }
        }

        let correctedDist = distance * Math.cos(rayAngle - angle);
        let h = Math.min(canvas.height, canvas.height / (correctedDist + 0.0001));
        let shade = Math.max(0, Math.floor(200 - correctedDist * (200 / flashRange)));

        ctx.fillStyle = `rgb(${shade}, ${Math.floor(shade*0.1)}, ${Math.floor(shade*0.1)})`;
        ctx.fillRect(i * w, (canvas.height - h) / 2, w + 1, h);
    }

    // 귀신 렌더링
    if (ghostHp > 0) {
        let gdx = gx - px, gdy = gy - py;
        let gDist = Math.sqrt(gdx*gdx + gdy*gdy);
        let gAngle = Math.atan2(gdy, gdx) - angle;

        while (gAngle < -Math.PI) gAngle += 2 * Math.PI;
        while (gAngle > Math.PI) gAngle -= 2 * Math.PI;

        if (Math.abs(gAngle) < fov / 2 && gDist < flashRange) {
            let sx = (canvas.width / 2) + Math.tan(gAngle) * (canvas.width / 2);
            let size = Math.min(300, canvas.height / gDist);

            ctx.fillStyle = ghostStun > 0 ? '#5588aa' : '#e0e0e0';
            ctx.beginPath();
            ctx.arc(sx, canvas.height/2, size/3, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = 'red';
            ctx.beginPath();
            ctx.arc(sx - size/8, canvas.height/2 - size/10, size/15, 0, Math.PI * 2);
            ctx.arc(sx + size/8, canvas.height/2 - size/10, size/15, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    // 1인칭 단검(무기) 화면 렌더링
    if (items.knife) {
        ctx.save();
        let attackOffset = isAttacking * 8; // 공격 시 찌르는 모션
        ctx.fillStyle = '#aaa';
        ctx.beginPath();
        ctx.moveTo(canvas.width/2 + 80 - attackOffset, canvas.height - 20 - attackOffset);
        ctx.lineTo(canvas.width/2 + 130 - attackOffset, canvas.height - 120 - attackOffset);
        ctx.lineTo(canvas.width/2 + 150 - attackOffset, canvas.height - 100 - attackOffset);
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

components.html(game_html, height=540)
