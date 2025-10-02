#!/usr/bin/env python3
"""
Sprite Generator for Python Learning Game
Generates pixel art sprites for the game characters, tiles, and objects.
"""

import pygame
import sys
from pathlib import Path

# Initialize Pygame
pygame.init()

# Output directory
SPRITES_DIR = Path(__file__).parent / "assets" / "sprites"
SPRITES_DIR.mkdir(parents=True, exist_ok=True)

# Sprite size
TILE_SIZE = 64  # Base tile size for high quality

# Color palette (cute pixel art style)
COLORS = {
    'player_blue': (52, 152, 219),
    'player_dark': (41, 128, 185),
    'player_light': (174, 214, 241),
    'player_eye': (44, 62, 80),
    'wall_gray': (149, 165, 166),
    'wall_dark': (127, 140, 141),
    'wall_light': (189, 195, 199),
    'floor_light': (236, 240, 241),
    'floor_dark': (189, 195, 199),
    'grass_green': (46, 204, 113),
    'grass_dark': (39, 174, 96),
    'gem_yellow': (241, 196, 15),
    'gem_orange': (243, 156, 18),
    'gem_light': (254, 242, 146),
    'goal_green': (46, 204, 113),
    'goal_dark': (39, 174, 96),
    'goal_light': (125, 206, 160),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'transparent': (255, 0, 255),
}


def draw_pixel_rect(surface, color, x, y, width=1, height=1):
    """Draw a pixel-perfect rectangle."""
    pygame.draw.rect(surface, color, (x, y, width, height))


def create_player_sprite(direction='north', frame=0):
    """Create a cute robot player sprite facing the given direction."""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surface.fill(COLORS['transparent'])
    surface.set_colorkey(COLORS['transparent'])
    
    # Animation offset for idle animation
    bob_offset = 0 if frame == 0 else 1
    
    # Player is a cute robot character
    center_x = TILE_SIZE // 2
    center_y = TILE_SIZE // 2 + bob_offset
    
    # Body (larger rectangle)
    body_width = 24
    body_height = 28
    body_x = center_x - body_width // 2
    body_y = center_y - body_height // 2 + 4
    
    # Main body
    draw_pixel_rect(surface, COLORS['player_blue'], body_x, body_y, body_width, body_height)
    # Body outline
    pygame.draw.rect(surface, COLORS['player_dark'], (body_x, body_y, body_width, body_height), 2)
    # Body highlight
    draw_pixel_rect(surface, COLORS['player_light'], body_x + 4, body_y + 4, 8, 4)
    
    # Head
    head_width = 20
    head_height = 18
    head_x = center_x - head_width // 2
    head_y = body_y - head_height + 4
    
    draw_pixel_rect(surface, COLORS['player_blue'], head_x, head_y, head_width, head_height)
    pygame.draw.rect(surface, COLORS['player_dark'], (head_x, head_y, head_width, head_height), 2)
    
    # Antenna
    antenna_x = center_x - 1
    antenna_y = head_y - 6
    draw_pixel_rect(surface, COLORS['player_dark'], antenna_x, antenna_y, 2, 6)
    pygame.draw.circle(surface, COLORS['gem_yellow'], (antenna_x + 1, antenna_y - 1), 3)
    
    # Eyes based on direction
    if direction == 'north':
        eye_y = head_y + 6
        # Two eyes looking up
        pygame.draw.circle(surface, COLORS['player_eye'], (head_x + 6, eye_y), 3)
        pygame.draw.circle(surface, COLORS['player_eye'], (head_x + 14, eye_y), 3)
        pygame.draw.circle(surface, COLORS['white'], (head_x + 6, eye_y - 1), 1)
        pygame.draw.circle(surface, COLORS['white'], (head_x + 14, eye_y - 1), 1)
    elif direction == 'south':
        eye_y = head_y + 6
        # Two eyes looking down
        pygame.draw.circle(surface, COLORS['player_eye'], (head_x + 6, eye_y), 3)
        pygame.draw.circle(surface, COLORS['player_eye'], (head_x + 14, eye_y), 3)
        pygame.draw.circle(surface, COLORS['white'], (head_x + 6, eye_y + 1), 1)
        pygame.draw.circle(surface, COLORS['white'], (head_x + 14, eye_y + 1), 1)
    elif direction == 'east':
        eye_y = head_y + 6
        # Two eyes looking right
        pygame.draw.circle(surface, COLORS['player_eye'], (head_x + 8, eye_y), 3)
        pygame.draw.circle(surface, COLORS['player_eye'], (head_x + 16, eye_y), 3)
        pygame.draw.circle(surface, COLORS['white'], (head_x + 9, eye_y), 1)
        pygame.draw.circle(surface, COLORS['white'], (head_x + 17, eye_y), 1)
    elif direction == 'west':
        eye_y = head_y + 6
        # Two eyes looking left
        pygame.draw.circle(surface, COLORS['player_eye'], (head_x + 4, eye_y), 3)
        pygame.draw.circle(surface, COLORS['player_eye'], (head_x + 12, eye_y), 3)
        pygame.draw.circle(surface, COLORS['white'], (head_x + 3, eye_y), 1)
        pygame.draw.circle(surface, COLORS['white'], (head_x + 11, eye_y), 1)
    
    # Arms/wheels
    wheel_y = body_y + body_height - 8
    # Left wheel
    pygame.draw.circle(surface, COLORS['player_dark'], (body_x + 6, wheel_y), 5)
    pygame.draw.circle(surface, COLORS['wall_dark'], (body_x + 6, wheel_y), 3)
    # Right wheel
    pygame.draw.circle(surface, COLORS['player_dark'], (body_x + body_width - 6, wheel_y), 5)
    pygame.draw.circle(surface, COLORS['wall_dark'], (body_x + body_width - 6, wheel_y), 3)
    
    return surface


def create_floor_tile():
    """Create a floor tile sprite."""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surface.fill(COLORS['floor_light'])
    
    # Add some subtle pattern
    for i in range(0, TILE_SIZE, 8):
        for j in range(0, TILE_SIZE, 8):
            if (i + j) % 16 == 0:
                draw_pixel_rect(surface, COLORS['floor_dark'], i, j, 4, 4)
    
    # Border
    pygame.draw.rect(surface, COLORS['floor_dark'], (0, 0, TILE_SIZE, TILE_SIZE), 1)
    
    return surface


def create_grass_tile():
    """Create a grass tile sprite (alternative floor)."""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surface.fill(COLORS['grass_green'])
    
    # Add grass blades
    import random
    random.seed(42)  # Consistent grass pattern
    for _ in range(20):
        x = random.randint(2, TILE_SIZE - 4)
        y = random.randint(2, TILE_SIZE - 4)
        draw_pixel_rect(surface, COLORS['grass_dark'], x, y, 2, 3)
    
    # Border
    pygame.draw.rect(surface, COLORS['grass_dark'], (0, 0, TILE_SIZE, TILE_SIZE), 1)
    
    return surface


def create_wall_tile():
    """Create a wall tile sprite."""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surface.fill(COLORS['wall_gray'])
    
    # Brick pattern
    brick_height = TILE_SIZE // 4
    for row in range(4):
        y = row * brick_height
        offset = 0 if row % 2 == 0 else TILE_SIZE // 2
        
        # Draw brick lines
        pygame.draw.line(surface, COLORS['wall_dark'], (0, y), (TILE_SIZE, y), 2)
        pygame.draw.line(surface, COLORS['wall_dark'], (offset, y), (offset, y + brick_height), 2)
    
    # Highlight
    draw_pixel_rect(surface, COLORS['wall_light'], 4, 4, TILE_SIZE - 8, 4)
    
    # Border
    pygame.draw.rect(surface, COLORS['wall_dark'], (0, 0, TILE_SIZE, TILE_SIZE), 2)
    
    return surface


def create_gem_sprite(frame=0):
    """Create a gem sprite with animation frames."""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surface.fill(COLORS['transparent'])
    surface.set_colorkey(COLORS['transparent'])
    
    center_x = TILE_SIZE // 2
    center_y = TILE_SIZE // 2
    
    # Animation: gem rotates and bobs
    bob_offset = [0, -2, -4, -2][frame % 4]
    
    # Gem shape (diamond)
    gem_size = 16
    points = [
        (center_x, center_y - gem_size + bob_offset),  # Top
        (center_x + gem_size, center_y + bob_offset),  # Right
        (center_x, center_y + gem_size + bob_offset),  # Bottom
        (center_x - gem_size, center_y + bob_offset),  # Left
    ]
    
    # Shadow
    shadow_points = [(x, y + 4) for x, y in points]
    pygame.draw.polygon(surface, (0, 0, 0, 50), shadow_points)
    
    # Main gem
    pygame.draw.polygon(surface, COLORS['gem_yellow'], points)
    
    # Highlight
    highlight_points = [
        (center_x, center_y - gem_size + 4 + bob_offset),
        (center_x + gem_size - 4, center_y + bob_offset),
        (center_x, center_y + 4 + bob_offset),
        (center_x - gem_size + 4, center_y + bob_offset),
    ]
    pygame.draw.polygon(surface, COLORS['gem_light'], highlight_points)
    
    # Sparkle (changes position based on frame)
    sparkle_offsets = [(8, -8), (-8, -8), (-8, 8), (8, 8)]
    sparkle_x, sparkle_y = sparkle_offsets[frame % 4]
    pygame.draw.circle(surface, COLORS['white'], 
                      (center_x + sparkle_x, center_y + sparkle_y + bob_offset), 2)
    
    # Outline
    pygame.draw.polygon(surface, COLORS['gem_orange'], points, 2)
    
    return surface


def create_goal_sprite(frame=0):
    """Create a goal tile sprite with animation."""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    surface.fill(COLORS['transparent'])
    surface.set_colorkey(COLORS['transparent'])
    
    center_x = TILE_SIZE // 2
    center_y = TILE_SIZE // 2
    
    # Pulsing animation
    pulse = [0, 2, 4, 2][frame % 4]
    size = 24 + pulse
    
    # Outer glow
    for i in range(3):
        alpha_size = size + (3 - i) * 4
        s = pygame.Surface((alpha_size * 2, alpha_size * 2))
        s.fill(COLORS['transparent'])
        s.set_colorkey(COLORS['transparent'])
        s.set_alpha(50 - i * 15)
        pygame.draw.circle(s, COLORS['goal_light'], (alpha_size, alpha_size), alpha_size)
        surface.blit(s, (center_x - alpha_size, center_y - alpha_size))
    
    # Main goal
    pygame.draw.circle(surface, COLORS['goal_green'], (center_x, center_y), size)
    pygame.draw.circle(surface, COLORS['goal_dark'], (center_x, center_y), size, 3)
    
    # Inner star/checkmark pattern
    star_points = []
    import math
    for i in range(5):
        angle = math.pi * 2 * i / 5 - math.pi / 2
        x = center_x + math.cos(angle) * (size - 8)
        y = center_y + math.sin(angle) * (size - 8)
        star_points.append((x, y))
    
    pygame.draw.polygon(surface, COLORS['goal_light'], star_points)
    pygame.draw.polygon(surface, COLORS['goal_dark'], star_points, 2)
    
    return surface


def create_particle_sprite(color_name='gem_yellow'):
    """Create a small particle sprite."""
    surface = pygame.Surface((8, 8))
    surface.fill(COLORS['transparent'])
    surface.set_colorkey(COLORS['transparent'])
    
    pygame.draw.circle(surface, COLORS[color_name], (4, 4), 3)
    pygame.draw.circle(surface, COLORS['white'], (3, 3), 1)
    
    return surface


def main():
    """Generate all sprite assets."""
    print("🎨 Generating pixel art sprites for Python Learning Game...")
    
    # Player sprites (4 directions × 2 animation frames)
    directions = ['north', 'south', 'east', 'west']
    for direction in directions:
        for frame in range(2):
            sprite = create_player_sprite(direction, frame)
            filename = f"player_{direction}_{frame}.png"
            pygame.image.save(sprite, SPRITES_DIR / filename)
            print(f"  ✓ Created {filename}")
    
    # Tile sprites
    tiles = [
        ('floor', create_floor_tile()),
        ('grass', create_grass_tile()),
        ('wall', create_wall_tile()),
    ]
    
    for name, sprite in tiles:
        filename = f"tile_{name}.png"
        pygame.image.save(sprite, SPRITES_DIR / filename)
        print(f"  ✓ Created {filename}")
    
    # Gem sprites (4 animation frames)
    for frame in range(4):
        sprite = create_gem_sprite(frame)
        filename = f"gem_{frame}.png"
        pygame.image.save(sprite, SPRITES_DIR / filename)
        print(f"  ✓ Created {filename}")
    
    # Goal sprites (4 animation frames)
    for frame in range(4):
        sprite = create_goal_sprite(frame)
        filename = f"goal_{frame}.png"
        pygame.image.save(sprite, SPRITES_DIR / filename)
        print(f"  ✓ Created {filename}")
    
    # Particle sprites
    particle_colors = ['gem_yellow', 'goal_green', 'player_blue']
    for color in particle_colors:
        sprite = create_particle_sprite(color)
        filename = f"particle_{color}.png"
        pygame.image.save(sprite, SPRITES_DIR / filename)
        print(f"  ✓ Created {filename}")
    
    print(f"\n✨ All sprites generated successfully in {SPRITES_DIR}")
    print(f"📊 Total sprites created: {len(list(SPRITES_DIR.glob('*.png')))}")


if __name__ == "__main__":
    main()

