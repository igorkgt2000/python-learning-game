# 🔧 Troubleshooting Guide

Quick fixes for common issues!

---

## ❌ Problem: Black Screen / Game Won't Load

**Symptoms:**
- Window opens but game area is black/gray
- "Start Game" button doesn't work
- Console shows: `Error loading level: name 'TileType' is not defined`

**Solution:**
✅ **FIXED!** This was a missing import. Update your code:
```bash
git pull origin main
python3 main.py
```

---

## ❌ Problem: "No module named 'PIL'"

**Symptoms:**
```
ImportError: No module named 'PIL'
```

**Solution:**
```bash
pip install Pillow
python3 main.py
```

---

## ❌ Problem: "No module named 'pygame'"

**Solution:**
```bash
pip install pygame
python3 main.py
```

---

## ❌ Problem: Code Doesn't Execute

**Symptoms:**
- Click "Run Code" but nothing happens
- No error message

**Solution:**
1. Make sure you clicked **"Start Game"** first!
2. The game must be loaded before running code
3. Check output area for error messages

---

## ❌ Problem: "No levels found"

**Symptoms:**
```
No levels found!
```

**Solution:**
Check that level files exist:
```bash
ls src/levels/level_*.json | wc -l
# Should show 30
```

If missing, they're already in the repo - just pull:
```bash
git pull origin main
```

---

## ✅ Quick Test Commands

### Test 1: Can you preview levels?
```bash
python3 preview_levels.py 1
```
**Expected:** ASCII art of Level 1

### Test 2: Can you run the standalone game?
```bash
python3 run_game.py
```
**Expected:** Pygame window opens with game

### Test 3: Can you launch the full UI?
```bash
python3 main.py
```
**Expected:** Split-screen window (game + editor)

---

## 🎮 How to Actually Play

1. **Launch:** `python3 main.py`
2. **Click:** "Start Game" button
3. **Wait:** 1-2 seconds for level to load
4. **See:** Game should appear in left panel
5. **Write:** Code in right panel:
   ```python
   move_forward()
   move_forward()
   ```
6. **Click:** "Run Code" button
7. **Watch:** Player moves to goal!

---

## 🐛 Still Not Working?

### Check Python Version
```bash
python3 --version
# Should be 3.8 or higher
```

### Reinstall Dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Check for Errors
```bash
python3 main.py 2>&1 | tee error.log
# Check error.log for issues
```

### Try Standalone Version First
```bash
python3 run_game.py
# If this works, UI integration issue
# If this fails, core game issue
```

---

## 💡 Common Questions

### Q: Game window is tiny?
**A:** The game canvas is 400x400px by design. You can resize the window!

### Q: Where do I write code?
**A:** Right side panel (Code Editor section)

### Q: How do I know if code executed?
**A:** Check the "Output" area below the editor for success/error messages

### Q: Can I skip levels?
**A:** Not in the UI yet, but you can modify `main_window.py` to start at a different level

### Q: Game is laggy?
**A:** Check if other programs are using CPU. Game targets 60 FPS.

---

## 🚀 Performance Tips

### Reduce Lag
1. Close other applications
2. Make sure you have Pillow installed (faster rendering)
3. Check terminal for warnings

### Faster Startup
- Sprites are pre-generated in `assets/sprites/`
- If slow, check disk space

---

## 📞 Need More Help?

1. **Check the docs:**
   - `IT_WORKS.md` - Complete guide
   - `QUICK_START.md` - Getting started
   - `DOCUMENTATION.md` - Technical details

2. **Check the code:**
   - All files are extensively commented
   - Read any `.py` file to understand it

3. **Check GitHub:**
   - Latest fixes at: https://github.com/igorkgt2000/python-learning-game

---

## ✅ Verification Checklist

Before reporting an issue, verify:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Latest code (`git pull origin main`)
- [ ] Sprites generated (`ls assets/sprites/ | wc -l` shows 50+)
- [ ] Levels exist (`ls src/levels/*.json | wc -l` shows 30)
- [ ] Tried `run_game.py` standalone

---

**Most issues are fixed by updating dependencies or pulling latest code!** 🎉

