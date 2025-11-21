# Life of Py - AI Coding Agent Instructions

A Pygame-based 2D life simulation game with persistent character data, economic systems, and tile-based level editing.

## Architecture Overview

### Three Entry Points
- **`game.py`** (Game): Main gameplay loop with character progression, job system, UI management
- **`menu.py`** (Menu): Save/load management, character creation (gender selection, name input)
- **`editor.py`** (Editor): Tile-based map editor for level design (grid-aligned and off-grid tiles)

### Data Flow
1. **Player State** (`scripts/entities.py`): Extends `PhysicsEntity` with attributes (health, energy, hunger, money, job, level)
2. **Persistence**: SQLite database (`data/save/save.db`) via SQLAlchemy ORM
3. **Economy System** (`scripts/economy.py`): Per-player inflation, salary index, tax rates stored in `economy.db`
4. **Asset Loading** (`scripts/utils.py`): Animations and images cached in `game.assets` dict at initialization

### Rendering Pipeline
- **Internal Display**: 512×384 upscaled 2× to 1024×768 window (low-res aesthetic)
- **Shader System** (`scripts/gl_renderer.py`): ModernGL GPU shaders for retro RPG effects (palette reduction, dithering, scanlines, cel shading)
- **Fallback**: Automatic non-shader rendering if GPU incompatible
- **TileMap** (`scripts/tilemap.py`): Grid-aligned tiles + off-grid overlays, physics collision only on PHYSICS_TILES (stone, building, wall, structure)
- **Physics**: Rectangle-based AABB collision on neighboring tile checks

## Critical Patterns

### Animation System
```python
# Assets stored as Animation objects with frame duration
'npc/1/idle': Animation(load_images('entities/npc/npc-1/idle'), img_dur=12)

# Animations copy() for independent state per entity
self.animation = self.game.assets[f"{self.type}/{self.action}"].copy()
```
Set action via `entity.set_action("idle")` to trigger animation change.

### Physics Entity Collision
- X and Y collision checked **separately** to allow sliding
- `PhysicsEntity.update(tile_map, movement)` handles all movement and collision detection
- NPCs and player both inherit `PhysicsEntity`

### UI Patterns (pygame_gui)
- Custom panel subclasses: `AnimatedPanel` (tweened motion/fade), `PopupPanel` (toast notifications)
- Theme managed via `data/gui/themes/theme.json` (ObjectID styling for UI elements)
- All UI managers reference 1024×768 resolution (not internal display size)

### Save System
- Player data: SQLAlchemy ORM to SQLite (name, job, money, level, gender)
- Economy data: Per-player CSV + SQLite for graphs/analytics
- Game saves on quit/manual save; loads via `load_game()` function

## File Organization

| Directory | Purpose |
|-----------|---------|
| `scripts/` | Core logic (entities, physics, jobs, actions, data layer) |
| `subclass/` | Custom UI components (panels, progress bars, tweening animations) |
| `data/images/` | Sprites (player genders, NPCs 1-10, tiles, UI icons) |
| `data/maps/` | JSON tilemap files (home, suburb, town) |
| `data/save/` | Persistent data (SQLite DB, economy CSVs) |
| `credits/` | NPC/player credit text files |

## Key Implementation Details

### Animation Frame Duration
- Most animations: 12 frames per image (each frame displays for 12 game frames)
- `img_dur=24` for slower animations (e.g., npc-5): displays each frame for 24 frames at 60 FPS
- `img_dur=6` for walking animations (twice as fast)
- `loop=False` for hurt/one-shot animations with `.done` flag

### TileMap Rendering
- Only renders tiles within camera viewport (frustum culling)
- Off-grid tiles stored in `off_grid_tiles` list for decoration overlays
- Tile IDs format: `f"{x};{y}"` (semicolon-delimited grid coordinates)

### Gender System
- `player.gender`: 0 = male, 1 = female (integer flag)
- Assets organized as `entities/player/{male|female}/{action}/{frame.png}`

### Economy Mechanics
- `inflation`, `interest_rate`, `salary_index`, `tax_rate` all float multipliers (defaults = 1.0)
- Per-player economy simulation: each player's game instance has unique economy state
- Daily updates with CSV + SQLite persistence for analytics and replay scenarios
- Allows economic sandbox testing with different starting conditions

## Development Workflows

### Running the Game
```bash
python setup_moderngl.py # Install shaders dependencies (first time only)
python game.py           # Start from menu (60 FPS target with retro RPG shader)
python editor.py         # Tile editor (WASD pan, scroll select tile, click place, right-click remove)
                         # Press 'o' to save map to data/maps/{location}.json
```

### In-Game Shader Switching
- Press `1`: Retro RPG (default) - palette reduction + dithering
- Press `2`: Cel Shading - cartoon style with outlines
- Press `3`: Scanlines - CRT monitor effect

### Adding New Features
1. **New NPC**: Add sprite frames to `data/images/entities/npc/npc-N/idle/`, load animation in `game.assets`
2. **New Job**: Define in `scripts/jobs.py`, load via `load_jobs()`, assign to player
3. **New Map**: Create tilemap with `editor.py`, save as JSON to `data/maps/`
4. **New UI Panel**: Subclass `UIPanel` or `AnimatedPanel`, use ObjectID styling from theme.json
5. **New Shader Effect**: Add GLSL file to `scripts/shaders/`, create preset in `gl_renderer.py`

### Debugging
- Physics issues: Check `tile_map.physics_rects_around()` neighbor offsets and PHYSICS_TILES filtering
- Animation glitches: Verify `img_dur` matches sprite frame count; check `.copy()` is called per entity
- Save corruption: Inspect `data/save/save.db` with SQLite browser; check ORM column mappings in `scripts/data.py`

## Common Gotchas
- **Internal vs screen resolution**: Camera operations use 512×384 internally; UI uses 1024×768
- **Animation sharing**: Never use `self.game.assets[key]` directly; always call `.copy()` first
- **JSON tile format**: Must preserve `"type"`, `"variant"`, `"pos"` keys; position in grid coords (not pixels) for on-grid tiles
- **Database paths**: Use `Path.resolve()` + `parents[1]` to correctly locate `data/` relative to scripts location
- **Editor saves**: Maps only persist to disk when 'o' key is pressed; unsaved changes are lost on exit
- **PHYSICS_TILES**: Only tiles in this set are checked for collision; non-physics tiles are rendered but don't block movement
