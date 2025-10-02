# 🚀 Quick Start Guide

## Running the Game

### Option 1: Simple Game Viewer (No Code Editor)
```bash
python run_game.py              # Start at level 1
python run_game.py 5            # Start at level 5
```

**Controls:**
- `ESC` - Quit
- `R` - Reset level
- `N` - Next level
- `P` - Previous level

**Note:** This is just for viewing levels. You can't write code here!

---

### Option 2: Full Game with Code Editor (Coming Soon)
```bash
python main.py
```

This will open the full split-screen interface with:
- Left: Game view
- Right: Python code editor

---

## Testing Levels

### Preview Levels (ASCII art)
```bash
python preview_levels.py           # All levels
python preview_levels.py 10        # Just level 10
python preview_levels.py 6-15      # Range of levels
```

---

## Project Structure

```
python_learning_game/
├── src/
│   ├── core/          # Game engine
│   ├── levels/        # Level JSON files (30 levels!)
│   └── ui/            # Tkinter UI
├── assets/
│   └── sprites/       # Pixel art (run generate_sprites.py first!)
├── run_game.py        # Simple Pygame viewer
├── preview_levels.py  # Level ASCII preview
├── generate_sprites.py # Create pixel art assets
└── main.py           # Full game with editor (WIP)
```

---

## First Time Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Generate sprites:**
```bash
python generate_sprites.py
```

3. **Preview a level:**
```bash
python preview_levels.py 1
```

4. **Run the game:**
```bash
python run_game.py
```

---

## Development Status

✅ **COMPLETE:**
- All 30 levels (beginner to expert)
- Comprehensive documentation
- Pixel art sprites
- Level preview tool
- Simple game viewer

🔄 **IN PROGRESS:**
- Full UI integration (Pygame + Tkinter)
- Code editor connection
- Smooth animations

⏳ **COMING SOON:**
- Save/load progress
- Achievements
- Hints system
- Tutorial overlay

---

## Troubleshooting

### "No module named 'pygame'"
```bash
pip install pygame
```

### "Sprites directory not found"
```bash
python generate_sprites.py
```

### "No levels found"
Levels should be in `src/levels/`. They're already there! Check:
```bash
ls src/levels/*.json | wc -l    # Should show 30
```

---

Happy coding! 🎮🐍

