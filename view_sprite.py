#!/usr/bin/env python3
"""
Quick sprite viewer - view individual sprites enlarged
Usage: python view_sprite.py [sprite_name]
Example: python view_sprite.py player_north_0
"""

import pygame
import sys
from pathlib import Path

def view_sprite(sprite_name):
    """View a sprite enlarged."""
    pygame.init()
    
    sprites_dir = Path(__file__).parent / "assets" / "sprites"
    sprite_path = sprites_dir / f"{sprite_name}.png"
    
    if not sprite_path.exists():
        print(f"❌ Sprite not found: {sprite_path}")
        print(f"\nAvailable sprites in {sprites_dir}:")
        for sprite_file in sorted(sprites_dir.glob("*.png")):
            print(f"  - {sprite_file.stem}")
        return
    
    # Load sprite
    sprite = pygame.image.load(str(sprite_path))
    original_size = sprite.get_size()
    
    # Scale up for viewing
    scale = 8
    display_size = (original_size[0] * scale, original_size[1] * scale)
    scaled_sprite = pygame.transform.scale(sprite, display_size)
    
    # Create window
    window_size = (display_size[0] + 100, display_size[1] + 150)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption(f"Sprite Viewer: {sprite_name}")
    
    # Fonts
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 24)
    
    # Main loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Render
        screen.fill((40, 44, 52))
        
        # Draw checkered background
        checker_size = 16
        for y in range(0, display_size[1], checker_size):
            for x in range(0, display_size[0], checker_size):
                if (x // checker_size + y // checker_size) % 2 == 0:
                    color = (60, 64, 72)
                else:
                    color = (50, 54, 62)
                pygame.draw.rect(screen, color, (50 + x, 50 + y, checker_size, checker_size))
        
        # Draw sprite
        screen.blit(scaled_sprite, (50, 50))
        
        # Draw border
        pygame.draw.rect(screen, (255, 255, 255), (48, 48, display_size[0] + 4, display_size[1] + 4), 2)
        
        # Info text
        title_text = font.render(sprite_name, True, (255, 255, 255))
        screen.blit(title_text, (50, window_size[1] - 80))
        
        size_text = small_font.render(f"Size: {original_size[0]}x{original_size[1]} px (scaled {scale}x)", True, (149, 165, 166))
        screen.blit(size_text, (50, window_size[1] - 45))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        sprite_name = sys.argv[1]
        # Remove .png extension if provided
        if sprite_name.endswith('.png'):
            sprite_name = sprite_name[:-4]
        view_sprite(sprite_name)
    else:
        print("Sprite Viewer")
        print("=" * 50)
        print("Usage: python view_sprite.py [sprite_name]")
        print("\nExamples:")
        print("  python view_sprite.py player_north_0")
        print("  python view_sprite.py gem_0")
        print("  python view_sprite.py tile_wall")
        print("\nAvailable sprites:")
        
        sprites_dir = Path(__file__).parent / "assets" / "sprites"
        if sprites_dir.exists():
            sprites = sorted(sprites_dir.glob("*.png"))
            
            # Group by category
            categories = {
                'Player': [],
                'Tiles': [],
                'Gems': [],
                'Goals': [],
                'Particles': []
            }
            
            for sprite_file in sprites:
                name = sprite_file.stem
                if name.startswith('player_'):
                    categories['Player'].append(name)
                elif name.startswith('tile_'):
                    categories['Tiles'].append(name)
                elif name.startswith('gem_'):
                    categories['Gems'].append(name)
                elif name.startswith('goal_'):
                    categories['Goals'].append(name)
                elif name.startswith('particle_'):
                    categories['Particles'].append(name)
            
            for category, sprites in categories.items():
                if sprites:
                    print(f"\n{category}:")
                    for sprite in sprites:
                        print(f"  - {sprite}")
        else:
            print(f"\n❌ Sprites directory not found: {sprites_dir}")
            print("Run 'python generate_sprites.py' first!")


if __name__ == "__main__":
    main()

