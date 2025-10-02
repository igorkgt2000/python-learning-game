# 🎨 Getting Started with Pixel Art Sprites

Welcome to your newly upgraded Python Learning Game with beautiful pixel art graphics!

## 🚀 Quick Start

### 1. View the Sprite Showcase

Run the interactive demo to see all sprites in action:

```bash
python sprite_demo.py
```

**What you'll see:**
- ✨ Animated robot character facing all 4 directions
- 🎯 Floor, grass, and wall tiles
- 💎 Sparkling, floating gems
- 🎪 Pulsing goal markers
- 🎆 Particle effects (press SPACE to spawn more!)
- 🏞️ Example mini-level

**Controls:**
- `SPACE` or Click: Spawn particles
- `ESC`: Exit

### 2. View Individual Sprites

Examine any sprite up close:

```bash
# View specific sprite (8x enlarged)
python view_sprite.py player_north_0
python view_sprite.py gem_0
python view_sprite.py tile_wall

# List all available sprites
python view_sprite.py
```

### 3. Run Your Game

The sprites are automatically integrated into your main game:

```bash
python main.py
```

## 📦 What's Included

### Sprites Generated (22 total)

#### 🤖 Player Character (8 sprites)
- `player_north_0.png` / `player_north_1.png` - Looking up
- `player_south_0.png` / `player_south_1.png` - Looking down  
- `player_east_0.png` / `player_east_1.png` - Looking right
- `player_west_0.png` / `player_west_1.png` - Looking left

*Each direction has 2 frames for idle bob animation*

#### 🏗️ Environment Tiles (3 sprites)
- `tile_floor.png` - Clean floor with subtle pattern
- `tile_grass.png` - Grass with individual blades
- `tile_wall.png` - Brick wall with highlights

#### 💎 Gems (4 sprites)
- `gem_0.png` / `gem_1.png` / `gem_2.png` / `gem_3.png`
- 4-frame rotation and bob animation
- Sparkle effects that move position

#### 🎯 Goals (4 sprites)  
- `goal_0.png` / `goal_1.png` / `goal_2.png` / `goal_3.png`
- 4-frame pulse animation
- Glowing effect with star pattern

#### ✨ Particles (3 sprites)
- `particle_gem_yellow.png` - For gem collection
- `particle_goal_green.png` - For goal celebration
- `particle_player_blue.png` - For player effects

## 🎮 Using Sprites in Your Code

### Basic Usage

The sprite system is automatically integrated! Just use the existing game code:

```python
from src.core.game import Game
from src.core.config import Config

# Create and run game
config = Config()
game = Game(config)
game.run()
```

### Advanced: Custom Rendering

If you want to render sprites directly:

```python
from src.core.sprite_manager import SpriteManager
import pygame

# Initialize
sprite_manager = SpriteManager()

# In your game loop:
dt = clock.get_time() / 1000.0
sprite_manager.update(dt)  # Update animations

# Get sprites
player_sprite = sprite_manager.get_player_sprite('north', size=(64, 64))
gem_sprite = sprite_manager.get_gem_sprite(size=(64, 64))
floor_sprite = sprite_manager.get_tile_sprite('floor', size=(64, 64))

# Render
screen.blit(player_sprite, (x, y))
```

### Particle Effects

Emit particles for visual feedback:

```python
from src.core.renderer import Renderer

# In your game code
renderer = Renderer(screen, config)

# When collecting a gem
renderer.emit_collect_particles(grid_x, grid_y)

# In render loop
renderer.render_particles()
```

## 🎨 Customizing Sprites

### Regenerate with Changes

1. **Edit the sprite generator:**
   ```bash
   nano generate_sprites.py
   ```

2. **Modify the code:**
   - Change colors in the `COLORS` dictionary
   - Adjust `TILE_SIZE` for different resolutions
   - Edit individual sprite drawing functions
   - Add new animation frames

3. **Regenerate sprites:**
   ```bash
   python generate_sprites.py
   ```

4. **View changes:**
   ```bash
   python sprite_demo.py
   ```

### Example: Change Player Color

In `generate_sprites.py`, find the `COLORS` dictionary and modify:

```python
COLORS = {
    'player_blue': (255, 100, 100),    # Change to red
    'player_dark': (200, 50, 50),      # Darker red
    # ... rest of colors
}
```

Then run:
```bash
python generate_sprites.py
python sprite_demo.py  # See the changes!
```

## 🎯 Animation System

### How Animations Work

1. **Frame-based**: Multiple sprite files per animation
2. **Timing**: Configurable speed per animation type
3. **Automatic**: SpriteManager handles frame switching
4. **Smooth**: Uses delta time for frame-rate independence

### Animation Speeds

Configured in `src/core/sprite_manager.py`:

```python
self.animation_speeds = {
    'player_north': 0.3,   # 300ms per frame (slower)
    'gem': 0.15,           # 150ms per frame (faster)  
    'goal': 0.2,           # 200ms per frame (medium)
}
```

### Adding New Animations

1. Generate more frames in `generate_sprites.py`
2. Load them in `sprite_manager.py`
3. Add to animations dictionary with speed
4. Use in renderer

## 📊 Performance Tips

### Optimization
- Sprites are cached after loading
- Animations use minimal CPU
- Particle system auto-cleans old particles
- Hardware-accelerated rendering via Pygame

### Recommended Settings
- **Tile Size**: 64x64 (default) for HD displays
- **Particle Count**: 10-20 per effect
- **Animation Speed**: 0.1-0.3 seconds per frame
- **Frame Rate**: 60 FPS

### If Performance Issues
1. Reduce particle count in `emit()` calls
2. Lower tile size in config
3. Decrease animation frame rates
4. Limit number of simultaneous particles

## 🐛 Troubleshooting

### Sprites Not Showing?

**Check 1:** Verify sprites exist
```bash
ls -la assets/sprites/
```
Should show 22 .png files

**Check 2:** Regenerate sprites
```bash
python generate_sprites.py
```

**Check 3:** Check console for errors
Look for sprite loading warnings

### Animations Not Moving?

**Check 1:** Ensure update is called
```python
renderer.update(dt)  # Must be in game loop
```

**Check 2:** Verify delta time
```python
dt = clock.get_time() / 1000.0  # Convert ms to seconds
```

**Check 3:** Check animation speeds
Values too high = very slow animation

### Particles Not Spawning?

**Check 1:** Call emit function
```python
renderer.emit_collect_particles(x, y)
```

**Check 2:** Call render function
```python
renderer.render_particles()  # After other rendering
```

**Check 3:** Update particle system
```python
renderer.update(dt)  # Updates particles too
```

## 🎓 Learning Resources

### Files to Study

1. **`generate_sprites.py`** - Learn pixel art generation
2. **`src/core/sprite_manager.py`** - Understand sprite management
3. **`src/core/renderer.py`** - See rendering implementation
4. **`sprite_demo.py`** - Example of complete usage

### Key Concepts

- **Sprite**: A 2D image/texture
- **Animation Frame**: One image in an animation sequence
- **Delta Time (dt)**: Time between frames in seconds
- **Blit**: Drawing an image onto a surface
- **Alpha**: Transparency value (0=invisible, 255=solid)
- **Particle**: Small visual effect element

## 🎉 Next Steps

1. ✅ **View the demo** - `python sprite_demo.py`
2. ✅ **Explore individual sprites** - `python view_sprite.py player_north_0`
3. ✅ **Run your game** - `python main.py`
4. 🎨 **Customize colors** - Edit `generate_sprites.py`
5. 🎮 **Create levels** - Add more gems and goals
6. ✨ **Add effects** - Use particle system for feedback
7. 📚 **Read docs** - Check `DOCUMENTATION.md` for details

## 📝 Summary

You now have:
- ✨ 22 beautiful pixel art sprites
- 🎬 Smooth animation system
- 💫 Particle effects
- 🎮 Interactive demo
- 🔧 Easy customization tools

Everything is integrated and ready to use!

## 🆘 Need Help?

1. Check `DOCUMENTATION.md` for detailed info
2. Check `PIXEL_ART_CHANGELOG.md` for what changed
3. Run demo to see examples: `python sprite_demo.py`
4. View sprites individually: `python view_sprite.py`

---

**Enjoy your beautiful new pixel art graphics!** 🎨✨🎮

Made with ❤️ using Python and Pygame

