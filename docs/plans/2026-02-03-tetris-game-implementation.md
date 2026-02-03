# 테트리스 게임 구현 플랜

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**목표:** PixiJS를 사용한 클래식 테트리스 게임 구현

**아키텍처:** 단일 HTML 파일에 4개 핵심 클래스(Tetris, Board, Tetromino, Renderer)를 인라인 JavaScript로 구현. 수동 테스트로 검증.

**기술 스택:** PixiJS v8 (CDN), Vanilla JavaScript, HTML5

---

## Task 1: HTML 기본 구조 및 PixiJS 설정

**Files:**
- Create: `index.html`

**Step 1: HTML 구조 작성**

`index.html` 파일 생성:

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>테트리스</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #1a1a2e;
            font-family: 'Courier New', monospace;
        }
        #game-container {
            position: relative;
        }
    </style>
</head>
<body>
    <div id="game-container"></div>
    <script src="https://cdn.jsdelivr.net/npm/pixi.js@8/dist/pixi.min.js"></script>
    <script>
        // 게임 코드가 여기에 들어갑니다
        console.log('PixiJS loaded:', typeof PIXI !== 'undefined');
    </script>
</body>
</html>
```

**Step 2: 브라우저에서 확인**

실행: 브라우저에서 `index.html` 열기
예상: 콘솔에 "PixiJS loaded: true" 출력

**Step 3: 커밋**

```bash
git add index.html
git commit -m "feat: HTML 기본 구조 및 PixiJS CDN 추가"
```

---

## Task 2: 상수 및 유틸리티 정의

**Files:**
- Modify: `index.html` (script 태그 내부)

**Step 1: 게임 상수 정의**

`<script>` 태그 내부에 추가:

```javascript
// 게임 상수
const BLOCK_SIZE = 32;
const BOARD_WIDTH = 10;
const BOARD_HEIGHT = 20;
const COLORS = {
    I: 0x00F0F0,
    O: 0xF0F000,
    T: 0xA000F0,
    S: 0x00F000,
    Z: 0xF00000,
    J: 0x0000F0,
    L: 0xF0A000
};

// 테트로미노 모양 정의
const SHAPES = {
    I: [[0,0,0,0], [1,1,1,1], [0,0,0,0], [0,0,0,0]],
    O: [[1,1], [1,1]],
    T: [[0,1,0], [1,1,1], [0,0,0]],
    S: [[0,1,1], [1,1,0], [0,0,0]],
    Z: [[1,1,0], [0,1,1], [0,0,0]],
    J: [[1,0,0], [1,1,1], [0,0,0]],
    L: [[0,0,1], [1,1,1], [0,0,0]]
};

const SHAPE_NAMES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L'];

// 게임 상태
const GameState = {
    PLAYING: 'PLAYING',
    PAUSED: 'PAUSED',
    GAME_OVER: 'GAME_OVER'
};

console.log('Constants defined');
```

**Step 2: 브라우저에서 확인**

실행: 브라우저에서 새로고침
예상: 콘솔에 "Constants defined" 출력

**Step 3: 커밋**

```bash
git add index.html
git commit -m "feat: 게임 상수 및 테트로미노 모양 정의"
```

---

## Task 3: Tetromino 클래스 구현

**Files:**
- Modify: `index.html` (script 태그 내부)

**Step 1: Tetromino 클래스 작성**

상수 정의 다음에 추가:

```javascript
class Tetromino {
    constructor(type) {
        this.type = type;
        this.shape = SHAPES[type];
        this.color = COLORS[type];
        this.x = Math.floor(BOARD_WIDTH / 2) - Math.floor(this.shape[0].length / 2);
        this.y = 0;
        this.rotation = 0;
    }

    rotate() {
        // 시계방향 90도 회전: 전치 후 각 행 뒤집기
        const newShape = [];
        const size = this.shape.length;

        for (let i = 0; i < size; i++) {
            newShape[i] = [];
            for (let j = 0; j < size; j++) {
                newShape[i][j] = this.shape[size - 1 - j][i];
            }
        }

        return newShape;
    }

    getBlocks() {
        // 현재 피스가 차지하는 절대 좌표 반환
        const blocks = [];
        for (let y = 0; y < this.shape.length; y++) {
            for (let x = 0; x < this.shape[y].length; x++) {
                if (this.shape[y][x]) {
                    blocks.push({ x: this.x + x, y: this.y + y });
                }
            }
        }
        return blocks;
    }
}

console.log('Tetromino class defined');
```

**Step 2: 콘솔에서 테스트**

브라우저 콘솔에서 실행:

```javascript
const piece = new Tetromino('T');
console.log('Initial blocks:', piece.getBlocks());
console.log('Rotated shape:', piece.rotate());
```

예상: 블록 좌표와 회전된 모양이 출력됨

**Step 3: 커밋**

```bash
git add index.html
git commit -m "feat: Tetromino 클래스 구현 (회전, 블록 좌표)"
```

---

## Task 4: Board 클래스 구현 - 그리드 및 충돌 감지

**Files:**
- Modify: `index.html` (script 태그 내부)

**Step 1: Board 클래스 작성**

Tetromino 클래스 다음에 추가:

```javascript
class Board {
    constructor() {
        this.grid = [];
        for (let y = 0; y < BOARD_HEIGHT; y++) {
            this.grid[y] = new Array(BOARD_WIDTH).fill(0);
        }
    }

    checkCollision(tetromino, offsetX = 0, offsetY = 0) {
        const blocks = tetromino.getBlocks();

        for (const block of blocks) {
            const newX = block.x + offsetX;
            const newY = block.y + offsetY;

            // 벽 충돌
            if (newX < 0 || newX >= BOARD_WIDTH) return true;

            // 바닥 충돌
            if (newY >= BOARD_HEIGHT) return true;

            // 상단은 허용 (스폰 위치)
            if (newY < 0) continue;

            // 블록 충돌
            if (this.grid[newY][newX] !== 0) return true;
        }

        return false;
    }

    placePiece(tetromino) {
        const blocks = tetromino.getBlocks();

        for (const block of blocks) {
            if (block.y >= 0 && block.y < BOARD_HEIGHT) {
                this.grid[block.y][block.x] = tetromino.type;
            }
        }
    }

    clearLines() {
        let linesCleared = 0;

        for (let y = BOARD_HEIGHT - 1; y >= 0; y--) {
            if (this.grid[y].every(cell => cell !== 0)) {
                // 줄 제거
                this.grid.splice(y, 1);
                this.grid.unshift(new Array(BOARD_WIDTH).fill(0));
                linesCleared++;
                y++; // 같은 y를 다시 체크
            }
        }

        return linesCleared;
    }

    isGameOver() {
        // 최상단 행에 블록이 있으면 게임오버
        return this.grid[0].some(cell => cell !== 0);
    }
}

console.log('Board class defined');
```

**Step 2: 콘솔에서 테스트**

브라우저 콘솔에서 실행:

```javascript
const board = new Board();
const piece = new Tetromino('I');
piece.y = 18;
console.log('Collision at bottom:', board.checkCollision(piece, 0, 1));
console.log('No collision at current:', board.checkCollision(piece));
board.placePiece(piece);
console.log('Grid after placement:', board.grid[18]);
```

예상: 충돌 감지 및 피스 배치가 올바르게 작동

**Step 3: 커밋**

```bash
git add index.html
git commit -m "feat: Board 클래스 구현 (충돌 감지, 피스 배치, 줄 제거)"
```

---

## Task 5: Renderer 클래스 구현

**Files:**
- Modify: `index.html` (script 태그 내부)

**Step 1: Renderer 클래스 작성**

Board 클래스 다음에 추가:

```javascript
class Renderer {
    constructor() {
        this.app = new PIXI.Application();
        this.boardContainer = new PIXI.Container();
        this.pieceContainer = new PIXI.Container();
        this.uiContainer = new PIXI.Container();

        this.scoreText = null;
        this.levelText = null;
        this.linesText = null;
        this.gameOverText = null;
    }

    async init() {
        await this.app.init({
            width: BOARD_WIDTH * BLOCK_SIZE + 200,
            height: BOARD_HEIGHT * BLOCK_SIZE,
            backgroundColor: 0x16213e
        });

        document.getElementById('game-container').appendChild(this.app.canvas);

        this.app.stage.addChild(this.boardContainer);
        this.app.stage.addChild(this.pieceContainer);
        this.app.stage.addChild(this.uiContainer);

        this.createUI();
    }

    createUI() {
        // 점수
        this.scoreText = new PIXI.Text({
            text: '점수: 0',
            style: { fill: 0xffffff, fontSize: 20 }
        });
        this.scoreText.x = BOARD_WIDTH * BLOCK_SIZE + 20;
        this.scoreText.y = 200;
        this.uiContainer.addChild(this.scoreText);

        // 레벨
        this.levelText = new PIXI.Text({
            text: '레벨: 1',
            style: { fill: 0xffffff, fontSize: 20 }
        });
        this.levelText.x = BOARD_WIDTH * BLOCK_SIZE + 20;
        this.levelText.y = 240;
        this.uiContainer.addChild(this.levelText);

        // 줄 수
        this.linesText = new PIXI.Text({
            text: '줄: 0',
            style: { fill: 0xffffff, fontSize: 20 }
        });
        this.linesText.x = BOARD_WIDTH * BLOCK_SIZE + 20;
        this.linesText.y = 280;
        this.uiContainer.addChild(this.linesText);
    }

    drawBoard(board) {
        this.boardContainer.removeChildren();

        // 그리드 선
        const grid = new PIXI.Graphics();
        grid.rect(0, 0, BOARD_WIDTH * BLOCK_SIZE, BOARD_HEIGHT * BLOCK_SIZE);
        grid.stroke({ width: 2, color: 0x0f3460 });
        this.boardContainer.addChild(grid);

        // 보드 블록
        for (let y = 0; y < BOARD_HEIGHT; y++) {
            for (let x = 0; x < BOARD_WIDTH; x++) {
                if (board.grid[y][x] !== 0) {
                    const block = new PIXI.Graphics();
                    const color = COLORS[board.grid[y][x]];
                    block.rect(x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1,
                               BLOCK_SIZE - 2, BLOCK_SIZE - 2);
                    block.fill(color);
                    this.boardContainer.addChild(block);
                }
            }
        }
    }

    drawPiece(tetromino) {
        this.pieceContainer.removeChildren();

        const blocks = tetromino.getBlocks();
        for (const block of blocks) {
            if (block.y >= 0) {
                const graphic = new PIXI.Graphics();
                graphic.rect(block.x * BLOCK_SIZE + 1, block.y * BLOCK_SIZE + 1,
                            BLOCK_SIZE - 2, BLOCK_SIZE - 2);
                graphic.fill(tetromino.color);
                this.pieceContainer.addChild(graphic);
            }
        }
    }

    updateUI(score, level, lines) {
        this.scoreText.text = `점수: ${score}`;
        this.levelText.text = `레벨: ${level}`;
        this.linesText.text = `줄: ${lines}`;
    }

    showGameOver() {
        if (!this.gameOverText) {
            this.gameOverText = new PIXI.Text({
                text: 'GAME OVER\n\nR: 재시작',
                style: {
                    fill: 0xff0000,
                    fontSize: 32,
                    align: 'center'
                }
            });
            this.gameOverText.x = BOARD_WIDTH * BLOCK_SIZE / 2 - 100;
            this.gameOverText.y = BOARD_HEIGHT * BLOCK_SIZE / 2 - 50;
        }
        this.uiContainer.addChild(this.gameOverText);
    }

    hideGameOver() {
        if (this.gameOverText) {
            this.uiContainer.removeChild(this.gameOverText);
        }
    }
}

console.log('Renderer class defined');
```

**Step 2: 브라우저에서 확인**

실행: 브라우저에서 새로고침
예상: 콘솔에 "Renderer class defined" 출력

**Step 3: 커밋**

```bash
git add index.html
git commit -m "feat: Renderer 클래스 구현 (PixiJS 렌더링)"
```

---

## Task 6: 7-bag 랜덤 시스템 구현

**Files:**
- Modify: `index.html` (script 태그 내부)

**Step 1: 랜덤 생성기 함수 작성**

Renderer 클래스 다음에 추가:

```javascript
class PieceBag {
    constructor() {
        this.bag = [];
        this.refill();
    }

    refill() {
        // 7개 피스를 모두 넣고 섞음
        this.bag = [...SHAPE_NAMES];
        for (let i = this.bag.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.bag[i], this.bag[j]] = [this.bag[j], this.bag[i]];
        }
    }

    next() {
        if (this.bag.length === 0) {
            this.refill();
        }
        return this.bag.pop();
    }
}

console.log('PieceBag class defined');
```

**Step 2: 콘솔에서 테스트**

브라우저 콘솔에서 실행:

```javascript
const bag = new PieceBag();
const pieces = [];
for (let i = 0; i < 14; i++) {
    pieces.push(bag.next());
}
console.log('14 pieces:', pieces);
```

예상: 7개 피스가 2번 반복되며 각 세트는 섞여있음

**Step 3: 커밋**

```bash
git add index.html
git commit -m "feat: 7-bag 랜덤 피스 생성 시스템"
```

---

## Task 7: Tetris 메인 게임 클래스 - 초기화

**Files:**
- Modify: `index.html` (script 태그 내부)

**Step 1: Tetris 클래스 기본 구조**

PieceBag 클래스 다음에 추가:

```javascript
class Tetris {
    constructor() {
        this.board = new Board();
        this.renderer = new Renderer();
        this.pieceBag = new PieceBag();

        this.currentPiece = null;
        this.nextPiece = null;

        this.score = 0;
        this.level = 1;
        this.lines = 0;

        this.state = GameState.PLAYING;
        this.dropCounter = 0;
        this.dropInterval = 1000; // 1초
        this.lastTime = 0;

        this.keysPressed = {};
    }

    async init() {
        await this.renderer.init();
        this.spawnPiece();
        this.setupInput();
        this.start();
    }

    spawnPiece() {
        if (!this.nextPiece) {
            this.nextPiece = this.pieceBag.next();
        }

        this.currentPiece = new Tetromino(this.nextPiece);
        this.nextPiece = this.pieceBag.next();

        // 스폰 위치에서 충돌하면 게임오버
        if (this.board.checkCollision(this.currentPiece)) {
            this.state = GameState.GAME_OVER;
            this.renderer.showGameOver();
        }
    }

    start() {
        const gameLoop = (time = 0) => {
            if (this.state === GameState.PLAYING) {
                const deltaTime = time - this.lastTime;
                this.lastTime = time;
                this.update(deltaTime);
            }
            requestAnimationFrame(gameLoop);
        };
        requestAnimationFrame(gameLoop);
    }

    update(deltaTime) {
        // 다음 태스크에서 구현
    }

    setupInput() {
        // 다음 태스크에서 구현
    }
}

console.log('Tetris class defined');
```

**Step 2: 게임 시작 코드 추가**

Tetris 클래스 다음에 추가:

```javascript
// 게임 초기화 및 시작
const game = new Tetris();
game.init();
```

**Step 3: 브라우저에서 확인**

실행: 브라우저에서 새로고침
예상: PixiJS 캔버스가 표시되고, 빈 보드와 UI가 렌더링됨

**Step 4: 커밋**

```bash
git add index.html
git commit -m "feat: Tetris 메인 클래스 초기화 및 게임 루프"
```

---

## Task 8: 자동 낙하 및 렌더링 구현

**Files:**
- Modify: `index.html` - Tetris 클래스의 `update` 메서드

**Step 1: update 메서드 구현**

Tetris 클래스의 `update` 메서드를 다음으로 교체:

```javascript
update(deltaTime) {
    this.dropCounter += deltaTime;

    if (this.dropCounter > this.dropInterval) {
        this.moveDown();
        this.dropCounter = 0;
    }

    this.render();
}

moveDown() {
    if (!this.board.checkCollision(this.currentPiece, 0, 1)) {
        this.currentPiece.y++;
    } else {
        // 피스를 보드에 고정
        this.board.placePiece(this.currentPiece);

        // 줄 제거
        const linesCleared = this.board.clearLines();
        if (linesCleared > 0) {
            this.lines += linesCleared;
            this.updateScore(linesCleared);
        }

        // 새 피스 생성
        this.spawnPiece();
    }
}

updateScore(linesCleared) {
    const points = [0, 100, 300, 500, 800];
    this.score += points[linesCleared] * this.level;

    // 레벨업 (10줄마다)
    const newLevel = Math.floor(this.lines / 10) + 1;
    if (newLevel > this.level) {
        this.level = newLevel;
        this.dropInterval = Math.max(100, 1000 - (this.level - 1) * 100);
    }
}

render() {
    this.renderer.drawBoard(this.board);
    if (this.currentPiece) {
        this.renderer.drawPiece(this.currentPiece);
    }
    this.renderer.updateUI(this.score, this.level, this.lines);
}
```

**Step 2: 브라우저에서 확인**

실행: 브라우저에서 새로고침
예상: 피스가 자동으로 떨어지고 바닥에 도달하면 새 피스가 생성됨

**Step 3: 커밋**

```bash
git add index.html
git commit -m "feat: 자동 낙하 및 피스 고정 로직"
```

---

## Task 9: 키보드 입력 처리

**Files:**
- Modify: `index.html` - Tetris 클래스의 `setupInput` 메서드

**Step 1: setupInput 메서드 구현**

Tetris 클래스의 `setupInput` 메서드를 다음으로 교체:

```javascript
setupInput() {
    document.addEventListener('keydown', (e) => {
        if (this.keysPressed[e.key]) return; // 키 반복 방지
        this.keysPressed[e.key] = true;

        if (this.state === GameState.GAME_OVER) {
            if (e.key === 'r' || e.key === 'R') {
                this.restart();
            }
            return;
        }

        if (this.state === GameState.PAUSED) {
            if (e.key === 'p' || e.key === 'P') {
                this.state = GameState.PLAYING;
            }
            return;
        }

        switch(e.key) {
            case 'ArrowLeft':
                this.moveLeft();
                break;
            case 'ArrowRight':
                this.moveRight();
                break;
            case 'ArrowDown':
                this.moveDown();
                break;
            case 'ArrowUp':
                this.rotate();
                break;
            case 'p':
            case 'P':
                this.state = GameState.PAUSED;
                break;
        }
    });

    document.addEventListener('keyup', (e) => {
        this.keysPressed[e.key] = false;
    });
}

moveLeft() {
    if (!this.board.checkCollision(this.currentPiece, -1, 0)) {
        this.currentPiece.x--;
    }
}

moveRight() {
    if (!this.board.checkCollision(this.currentPiece, 1, 0)) {
        this.currentPiece.x++;
    }
}

rotate() {
    const originalShape = this.currentPiece.shape;
    const rotatedShape = this.currentPiece.rotate();
    this.currentPiece.shape = rotatedShape;

    // 충돌 체크
    if (this.board.checkCollision(this.currentPiece)) {
        // 벽 킥 시도: 왼쪽으로 1칸
        this.currentPiece.x--;
        if (this.board.checkCollision(this.currentPiece)) {
            // 오른쪽으로 2칸
            this.currentPiece.x += 2;
            if (this.board.checkCollision(this.currentPiece)) {
                // 회전 취소
                this.currentPiece.x--;
                this.currentPiece.shape = originalShape;
            }
        }
    }
}

restart() {
    this.board = new Board();
    this.pieceBag = new PieceBag();
    this.score = 0;
    this.level = 1;
    this.lines = 0;
    this.dropInterval = 1000;
    this.state = GameState.PLAYING;
    this.nextPiece = null;
    this.renderer.hideGameOver();
    this.spawnPiece();
}
```

**Step 2: 브라우저에서 테스트**

실행: 브라우저에서 새로고침
테스트:
- 화살표 좌/우: 피스 이동
- 화살표 위: 피스 회전
- 화살표 아래: 빠른 낙하
- P: 일시정지
- R (게임오버 후): 재시작

예상: 모든 키 입력이 올바르게 작동

**Step 3: 커밋**

```bash
git add index.html
git commit -m "feat: 키보드 입력 처리 (이동, 회전, 일시정지, 재시작)"
```

---

## Task 10: 다음 피스 미리보기 추가

**Files:**
- Modify: `index.html` - Renderer 클래스

**Step 1: 미리보기 렌더링 메서드 추가**

Renderer 클래스의 `createUI` 메서드 뒤에 추가:

```javascript
drawNextPiece(nextPieceType) {
    // 기존 미리보기 제거
    if (this.nextPieceContainer) {
        this.uiContainer.removeChild(this.nextPieceContainer);
    }

    this.nextPieceContainer = new PIXI.Container();
    this.uiContainer.addChild(this.nextPieceContainer);

    // "다음" 텍스트
    const label = new PIXI.Text({
        text: '다음',
        style: { fill: 0xffffff, fontSize: 20 }
    });
    label.x = BOARD_WIDTH * BLOCK_SIZE + 20;
    label.y = 50;
    this.nextPieceContainer.addChild(label);

    // 다음 피스 그리기
    const shape = SHAPES[nextPieceType];
    const color = COLORS[nextPieceType];
    const offsetX = BOARD_WIDTH * BLOCK_SIZE + 20;
    const offsetY = 90;

    for (let y = 0; y < shape.length; y++) {
        for (let x = 0; x < shape[y].length; x++) {
            if (shape[y][x]) {
                const block = new PIXI.Graphics();
                block.rect(offsetX + x * 24, offsetY + y * 24, 22, 22);
                block.fill(color);
                this.nextPieceContainer.addChild(block);
            }
        }
    }
}
```

**Step 2: render 메서드에 미리보기 추가**

Tetris 클래스의 `render` 메서드를 다음으로 수정:

```javascript
render() {
    this.renderer.drawBoard(this.board);
    if (this.currentPiece) {
        this.renderer.drawPiece(this.currentPiece);
    }
    this.renderer.updateUI(this.score, this.level, this.lines);
    if (this.nextPiece) {
        this.renderer.drawNextPiece(this.nextPiece);
    }
}
```

**Step 3: 브라우저에서 확인**

실행: 브라우저에서 새로고침
예상: 오른쪽 상단에 "다음" 텍스트와 함께 다음 피스가 표시됨

**Step 4: 커밋**

```bash
git add index.html
git commit -m "feat: 다음 피스 미리보기 UI"
```

---

## Task 11: 일시정지 UI 추가

**Files:**
- Modify: `index.html` - Renderer 클래스

**Step 1: 일시정지 텍스트 메서드 추가**

Renderer 클래스에 추가:

```javascript
showPaused() {
    if (!this.pausedText) {
        this.pausedText = new PIXI.Text({
            text: 'PAUSED\n\nP: 계속',
            style: {
                fill: 0xffff00,
                fontSize: 32,
                align: 'center'
            }
        });
        this.pausedText.x = BOARD_WIDTH * BLOCK_SIZE / 2 - 80;
        this.pausedText.y = BOARD_HEIGHT * BLOCK_SIZE / 2 - 50;
    }
    this.uiContainer.addChild(this.pausedText);
}

hidePaused() {
    if (this.pausedText && this.uiContainer.children.includes(this.pausedText)) {
        this.uiContainer.removeChild(this.pausedText);
    }
}
```

**Step 2: Tetris 클래스의 render 메서드 수정**

```javascript
render() {
    this.renderer.drawBoard(this.board);
    if (this.currentPiece) {
        this.renderer.drawPiece(this.currentPiece);
    }
    this.renderer.updateUI(this.score, this.level, this.lines);
    if (this.nextPiece) {
        this.renderer.drawNextPiece(this.nextPiece);
    }

    if (this.state === GameState.PAUSED) {
        this.renderer.showPaused();
    } else {
        this.renderer.hidePaused();
    }
}
```

**Step 3: 브라우저에서 테스트**

실행: 브라우저에서 새로고침
테스트: P 키를 눌러 일시정지
예상: "PAUSED" 텍스트가 중앙에 표시되고, P 키로 다시 재개됨

**Step 4: 커밋**

```bash
git add index.html
git commit -m "feat: 일시정지 상태 UI"
```

---

## Task 12: 최종 테스트 및 완성

**Files:**
- None (수동 테스트만)

**Step 1: 전체 기능 테스트**

브라우저에서 다음 항목들을 확인:

1. [ ] I, O, T, S, Z, J, L 피스가 모두 나타남
2. [ ] 화살표 키로 피스 이동 가능
3. [ ] 화살표 위 키로 피스 회전
4. [ ] 벽 킥이 작동함 (벽 근처에서 회전)
5. [ ] 줄이 가득 차면 제거됨
6. [ ] 1줄 제거 시 100점, 4줄 제거 시 800점
7. [ ] 10줄마다 레벨 증가
8. [ ] 레벨 증가 시 낙하 속도 빨라짐
9. [ ] 최상단에 블록이 쌓이면 게임오버
10. [ ] R 키로 재시작 가능
11. [ ] P 키로 일시정지/재개 가능
12. [ ] 다음 피스 미리보기가 올바르게 표시됨

**Step 2: 버그 발견 시**

발견된 버그가 있다면 수정하고 커밋:

```bash
git add index.html
git commit -m "fix: [버그 설명]"
```

**Step 3: 최종 커밋**

```bash
git add index.html
git commit -m "docs: 테트리스 게임 완성 및 테스트 완료"
```

---

## 수동 테스트 체크리스트

게임이 완성되면 다음 항목들을 확인:

- [ ] 7개 피스가 모두 올바르게 회전
- [ ] 벽, 바닥, 블록 충돌 감지 작동
- [ ] 줄 제거가 가득 찬 행을 제거
- [ ] 점수 계산: 1줄, 4줄 (테트리스)
- [ ] 레벨이 10줄마다 증가
- [ ] 낙하 속도가 레벨에 따라 증가
- [ ] 생성이 막혔을 때 게임 오버
- [ ] 재시작이 상태를 올바르게 초기화
- [ ] 일시정지/재개 작동
- [ ] 다음 피스 미리보기가 올바른 피스 표시

---

## 구현 완료 후

모든 테스트가 통과하면:

1. 메인 브랜치로 돌아가기
2. superpowers:finishing-a-development-branch 스킬 사용
3. PR 생성 또는 머지 결정
