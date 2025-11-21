# Life of Py 🐍

Welcome to **Life of Py**, a retro-inspired 2D life simulation game where you navigate the ups and downs of making a living in a procedurally-managed economy. Work your way up the career ladder, manage your energy and hunger, and watch as inflation and interest rates affect your earnings in real-time.

## Overview

Life of Py is a pixel art simulation game built with Pygame, combining action-RPG exploration with economic simulation mechanics. You'll explore three distinct locations (home, suburbs, and town), take on various jobs, and accumulate wealth while your personal economy interacts with a dynamic game economy.

Think of it as *This Grand Life RPG-style -ps, that was my inspiration*

---

## Game Mechanics

### Character System

When you start a new game, you create a character with:
- **Name**: Your in-game identity
- **Gender**: Male or Female (cosmetic, affects sprite)
- **Starting Stats**:
  - **Health**: 100 (decreases with work, stressful situations)
  - **Energy**: 100 (decreases as you work; sleep to restore)
  - **Hunger**: 100 (decreases over time; eat at burger shops to restore)
  - **Money**: $0 (your primary objective: acquire currency)
  - **Level**: 1 (advances through gameplay, unlocks better jobs)

### Career System

You can pursue one of **7 different jobs**, each with unique salary and requirements:

| Job | Salary | Energy Cost | Level Required |
|-----|--------|------------|-----------------|
| Cashier | $37.50/day | 20 | 1 |
| Salesman | $43.36/day | 20 | 1 |
| Cook | $49.00/day | 25 | 2 |
| Clerk | $56.00/day | 20 | 3 |
| Accountant | $63.00/day | 20 | 5 |
| Programmer | $90.76/day | 25 | 10 |
| Doctor | $105.00/day | 30 | 15 |

**How it works:**
- Select a job you meet the level requirements for
- Each workday costs energy and health
- Your salary is adjusted by the economy's `salary_index` (inflation can reduce your real earnings!)
- You advance in levels by consistently working and maintaining your character

### Economy System

Here's where it gets interesting. Your personal finances exist within a **living, breathing economy** that simulates real-world economic pressure:

#### Economic Indicators (Updated Daily)
- **Inflation**: Affects prices and real wages
- **Interest Rate**: Affects bank deposits
- **Salary Index**: Multiplier applied to your job salary
- **Tax Rate**: Eventually affects your take-home (framework for future expansion)

#### How It Affects You
Your actual daily salary = `base_salary × salary_index × inflation`

If inflation jumps from 1.0 to 1.5, your $50/day job suddenly feels like $33/day in real purchasing power. The economy graph lets you visualize these trends over time.

### Day/Night Cycle

The game operates on a day-based system:
- Each day, you can work one job or perform activities
- Nighttime brings visual changes (darker aesthetic)
- Your stats regenerate overnight (partial energy recovery, hunger reduces)
- Day counter increments, allowing you to track your progress


### Stat Management

Your character's stats decay over time and in specific situations:

| Stat | Decreases | Restores |
|------|-----------|----------|
| **Energy** | Working | Sleep (nighttime rest) |
| **Health** | Working | Time at home, specific items |
| **Hunger** | Each day, more if working | Eating at burger shops |
| **Money** | Purchasing items | Working, finding money |

If any stat hits zero, your character faces consequences:
- **Energy at 0**: Can't work (must sleep)
- **Health at 0**: Game Over
- **Hunger at 0**: Health degrades faster

---

## Controls

### Movement
- **WASD**: Move your character
- **Mouse**: Click to interact with NPCs and UI elements
- **X button**: Serves as the primary action button


### UI
- **ESC**: Pause game / open menu
- **Mouse Click**: Select jobs, make transactions, interact with world

### Save/Load
- Manual save via menu (optional per-day)
- If you fail to save, the economy graph resets to the last existing save point
- Load previous saves from main menu

---

## Progression & Goals

It is a sandbox game, but natural objectives emerge:

1. **Early Game**: Survive the first week, pick a job, start saving, try not to die
2. **Mid Game**: Accumulate $1000+, advance to better jobs (level up through experience)
3. **Late Game**: Exploit economy cycles, maximize salary index, become wealthy
4. **Sandbox**: Watch the economy evolve, experiment with different career paths

Your progress is tracked in **economy CSV files** that record daily inflation, interest rates, and salary multipliers—useful for analyzing what worked and what didn't across runs.

---

## Persistence & Save Data

### Where Saves Are Located

#### Development Mode (Running .py files)
```
Life of Py/
├── data/
│   └── save/
│       ├── save.db              (main player data)
│       ├── economy.db           (economic simulation state)
│       └── {PlayerName}_economy.csv  (daily records)
```

#### If you are running the executable(located in here)
```
C:\Users\{YourUsername}\AppData\Roaming\LifeOfPy\
├── save.db                      (main player data)
├── economy.db                   (economic simulation state)
└── {PlayerName}_economy.csv     (daily records)
```



## Technical Details

### Architecture

- **Framework**: Pygame-CE 2.5.5 + pygame_gui 0.6.0+
- **Database**: SQLAlchemy ORM with SQLite
- **Physics**: Simple AABB tile-based collision detection
- **Resolution**: 512×384 internal (2× upscaled to 1024×768)
- **Performance**: Targets 60 FPS on modest hardware (Intel HD 4400+)



---

## Known Quirks & Features

### Features
- **Dynamic Economy**: Inflation actually affects your salary (not just cosmetic)
- **Gender-Specific Sprites**: Character appearance changes based on gender selection
- **NPC System**: NPCs with idle animations populate the world (10 different NPCs)
- **Day Counter**: Persistent day tracking across saves
- **Audio Design**: Ambient sounds, click feedback, work SFX

### Limitations
- No multiplayer (single-player only)
- Limited NPC dialogue (they're there but don't talk much)
- Economy doesn't fully respond to player actions yet (planned for future versions)
- No permadeath (health at 0 = restart, but saves remain)

---

## Tips & Tricks

### Money Management
- **Start small**: Pick Cashier or Salesman, build a safety net of $500
- **Watch the economy**: If salary_index drops, consider taking higher-cost jobs
- **Bank deposits**: Use the bank to earn interest (though rates fluctuate)

### Leveling Up
- **Consistency pays**: Work the same job repeatedly to advance levels
- **Higher levels = better jobs**: Level 15 unlocks Doctor job ($105/day!)
- **Respec**: You can switch jobs at any time (no permanent commitment)

### Stat Management
- **Plan your day**: Check energy before committing to work
- **Eat proactively**: Burger shops are lifesavers when hunger approaches zero
- **Sleep schedule**: Rest at home before your energy drops too low
- **Health is currency**: Protect it like money—once it's gone, run's over

### Economy Reading
- **Graph the trends**: Open the economy graph to see what's coming
- **Inflation spikes**: When inflation rises, wages stay the same but feel smaller
- **Interest rates**: Low rates = your bank deposits earn less
- **Plan ahead**: If you see inflation rising, save aggressively beforehand

---

## Troubleshooting

### Saves Not Appearing
**Problem**: You created a save but it doesn't show in Load menu.
**Solution**: Ensure you're saving with a unique name. Check `AppData\Local\LifeOfPy\` to verify files exist.

### Game Crashes on Startup
**Problem**: "Cannot find theme.json" or similar error.
**Solution**: If using the .exe, ensure the `data/` folder exists in the same directory. Rebuild with PyInstaller if needed.

### Performance Issues
**Problem**: Game feels choppy or slow.
**Solution**: 
- Close background applications
- Update GPU drivers
- Lower the FPS cap (default 120—edit `scripts/utils.py` if needed)

### Database Corruption
**Problem**: Game won't load a specific save.
**Solution**: Delete the corrupted save from the menu. If `economy.db` is the issue, it's usually safe to delete (will regenerate on next save).

---

## Development & Modding

### Editing Maps
Use the included map editor:
```bash
python editor.py
```
**When creating custom maps:**
- Change `self.location` to something other than `'home'`, `'suburb'`, or `'town'` to avoid overwriting existing maps
- Pick a cool pixel art background image and use stone tiles to create borders (like the existing maps)
- **WASD**: Pan camera
- **Scroll**: Select tile
- **Click**: Place tile
- **Right-click**: Remove tile
- **O**: Save map

### Modifying Jobs
Edit `scripts/jobs.py`:
```python
def load_jobs():
    job = Job(name="CEO", base_salary=200.0, energy_cost=15, lvl_required=20)
    # Replace in return list
```

### Creating NPCs
Add sprite folders to `data/images/entities/npc/npc-N/` and  `data/images/tiles/spawners`then place them using the editor.py lastly reference in `game.py` assets.

### Custom Economy Rules
Modify `scripts/economy.py` to change how inflation/interest rates are calculated.
Don't go too crazy...

---

## Credits & Thanks

**Life of Py** was built with:
- **Pygame-CE**: Community-maintained Pygame fork
- **pygame_gui**: Modern UI framework for Pygame
- **SQLAlchemy**: Elegant database ORM
- **Seaborn/Matplotlib**: Data visualization
- **Pixel-Art**: All sprites were made from https://liberatedpixelcup.github.io/Universal-LPC-Spritesheet-Character-Generator/


---

## License & Support

This is a passion project built as a learning exercise. Play it, break it, mod it—the code is relatively clean and well-commented.

If you find bugs or have ideas, feel free to open an issue or submit a pull request!

---

## About This Project

I'm a first-year Software Engineering student. This was a fun learning project that took about a month to complete. It heavily leverages OOP principles, database management with SQLAlchemy, data visualization with matplotlib/seaborn, game event scripting, and some creative problem-solving along the way.

The goal was to combine economic simulation with an engaging gameplay loop.