# Tetris Game Design

**Date:** 2026-02-03
**Type:** Classic Tetris with PixiJS
**Approach:** Single HTML file with inline JavaScript

## Requirements

- Classic tetris with 7 tetromino pieces (I, O, T, S, Z, J, L)
- Basic rotation, line clearing, scoring
- Simple colored blocks (no textures)
- Single HTML file using PixiJS CDN
- Quick prototype for PixiJS testing

## Architecture

### Core Classes

1. **`Tetris`** (Main Game)
   - Game loop management
   - State management: `MENU`, `PLAYING`, `PAUSED`, `GAME_OVER`
   - PixiJS app initialization
   - Keyboard input handling

2. **`Board`**
   - 10x20 grid representation (2D array)
   - Block placement and collision detection
   - Line clearing logic
   - Game over detection

3. **`Tetromino`**
   - 7 piece definitions (4x4 matrices)
   - Rotation logic (clockwise 90°)
   - Movement (left, right, down)
   - Position and color tracking

4. **`Renderer`**
   - PixiJS Graphics rendering
   - Board visualization (32x32 pixel blocks)
   - Current piece rendering
   - UI elements (score, level, lines, next piece preview)

### Game States

- `MENU`: Initial screen (optional, can start directly)
- `PLAYING`: Active gameplay
- `PAUSED`: Game paused (P key)
- `GAME_OVER`: Game ended, awaiting restart (R key)

## Data Structures

### Board Grid
```javascript
grid: number[][]  // 10 columns x 20 rows
// 0 = empty cell
// 1-7 = occupied cell with tetromino color
```

### Tetromino Shapes
```javascript
SHAPES = {
  I: [[0,0,0,0], [1,1,1,1], [0,0,0,0], [0,0,0,0]],
  O: [[1,1], [1,1]],
  T: [[0,1,0], [1,1,1], [0,0,0]],
  S: [[0,1,1], [1,1,0], [0,0,0]],
  Z: [[1,1,0], [0,1,1], [0,0,0]],
  J: [[1,0,0], [1,1,1], [0,0,0]],
  L: [[0,0,1], [1,1,1], [0,0,0]]
}
```

### Color Palette
- I: Cyan (#00F0F0)
- O: Yellow (#F0F000)
- T: Purple (#A000F0)
- S: Green (#00F000)
- Z: Red (#F00000)
- J: Blue (#0000F0)
- L: Orange (#F0A000)

## Game Logic

### Game Loop
1. Every frame: Move current piece down after time interval
2. On collision: Lock piece to board, check line clears, spawn new piece
3. Score calculation: 1 line=100, 2 lines=300, 3 lines=500, 4 lines=800
4. Level up: Every 10 lines, increase fall speed
5. Game over: When new piece cannot spawn

### Collision Detection
```javascript
checkCollision(tetromino, x, y):
  - Wall collision: x < 0 or x + width > 10
  - Floor collision: y + height > 20
  - Block collision: grid[y][x] !== 0
  - Return: boolean
```

### Rotation with Wall Kick
- Default: Rotate clockwise 90°
- If collision after rotation: Try shifting 1 cell left/right
- If still colliding: Cancel rotation

### Random System
- 7-bag randomizer: Shuffle all 7 pieces, dispense in order
- Ensures fair distribution of pieces

## Controls

- **Arrow Left/Right**: Move piece horizontally
- **Arrow Up**: Rotate piece
- **Arrow Down**: Soft drop (faster fall)
- **Space**: Hard drop (instant fall) - optional
- **P**: Pause/unpause
- **R**: Restart (game over only)

## UI Layout

```
┌─────────────────┬─────────┐
│                 │ NEXT    │
│   GAME BOARD    │ [□□]    │
│   (10x20)       │ [□□]    │
│                 │         │
│                 │ SCORE   │
│                 │ 0       │
│                 │ LEVEL 1 │
│                 │ LINES 0 │
└─────────────────┴─────────┘
```

## Rendering

### Board Rendering
- Each cell: 32x32 pixels
- Grid lines for boundaries
- PixiJS Graphics for drawing rectangles

### Piece Rendering
- Draw each occupied cell of current tetromino
- Use corresponding color from palette

### UI Rendering
- PixiJS Text for score/level/lines
- Small preview area for next piece (4x4 grid)

## Error Handling

### Edge Cases
- **Rotation near wall**: Wall kick mechanism
- **Fast input**: Debounce repeated key events (except down arrow)
- **Game over**: Detect when spawn position is blocked
- **Pause during game over**: Ignore pause input

### Input Handling
- Use `keydown` event
- Track key state to prevent repeat
- Exception: Down arrow allows continuous press

## Implementation Order

1. **Basic Setup** (~10 min)
   - HTML structure
   - PixiJS CDN integration
   - Canvas initialization
   - Empty board rendering

2. **Tetromino Class** (~15 min)
   - Define 7 shapes
   - Rotation logic
   - Manual console testing

3. **Board + Collision** (~20 min)
   - Grid creation
   - `placePiece()` method
   - `checkCollision()` method
   - Test piece placement

4. **Game Loop** (~15 min)
   - Automatic falling
   - Keyboard input
   - New piece generation

5. **Line Clearing + Score** (~10 min)
   - `clearLines()` method
   - Score calculation
   - Level progression

6. **UI + Next Piece** (~10 min)
   - Score/level display
   - Next piece preview

7. **Game Over + Restart** (~5 min)
   - Game over detection
   - Restart functionality

**Total estimated time:** ~1.5 hours
**Expected code size:** ~400-500 lines (including HTML)

## Testing Checklist

Manual testing:
- [ ] All 7 pieces rotate correctly
- [ ] Wall, floor, block collision detection works
- [ ] Line clearing removes full rows
- [ ] Score calculation: 1 line, 4 lines (tetris)
- [ ] Level increases every 10 lines
- [ ] Fall speed increases with level
- [ ] Game over when spawn blocked
- [ ] Restart clears state properly
- [ ] Pause/unpause works
- [ ] Next piece preview shows correct piece

## Performance Considerations

- Use `requestAnimationFrame` for game loop
- Optional: Dirty flag for render optimization (only redraw on change)
- Keep grid operations O(n) where possible

## Future Enhancements (Out of Scope)

- Hold piece functionality
- Ghost piece (preview landing position)
- Particle effects on line clear
- Sound effects
- Touch controls for mobile
- High score persistence
