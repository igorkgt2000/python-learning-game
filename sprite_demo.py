#!/usr/bin/env python3
"""
Sprite Demo - Showcases all pixel art sprites with animations
"""

import pygame
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.sprite_manager import SpriteManager
from core.animation import ParticleSystem

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
TILE_SIZE = 64
FPS = 60

# Colors
BG_COLOR = (40, 44, 52)
TEXT_COLOR = (255, 255, 255)
LABEL_COLOR = (149, 165, 166)

class SpriteDemo:
    """Demo application to showcase all sprites."""
    
    def __init__(self):
        """Initialize demo."""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Python Learning Game - Sprite Showcase")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize sprite manager
        self.sprite_manager = SpriteManager()
        
        # Initialize particle system
        self.particle_system = ParticleSystem()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.label_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Animation state
        self.particle_timer = 0.0
        self.particle_spawn_interval = 0.5  # seconds
        
    def run(self):
        """Main demo loop."""
        while self.running:
            dt = self.clock.get_time() / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        """Handle events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Emit particles on spacebar
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.particle_system.emit(mouse_x, mouse_y, 20, (241, 196, 15), speed=200)
    
    def update(self, dt):
        """Update animations."""
        self.sprite_manager.update(dt)
        self.particle_system.update(dt)
        
        # Auto-spawn particles
        self.particle_timer += dt
        if self.particle_timer >= self.particle_spawn_interval:
            self.particle_timer = 0.0
            # Spawn particles at gem location
            self.particle_system.emit(450, 350, 10, (241, 196, 15), speed=100)
    
    def render(self):
        """Render the demo."""
        self.screen.fill(BG_COLOR)
        
        # Title
        title = self.title_font.render("🎨 Python Learning Game - Pixel Art Showcase", True, TEXT_COLOR)
        self.screen.blit(title, (50, 30))
        
        # Instructions
        instructions = self.small_font.render("Press SPACE or click to spawn particles | ESC to exit", True, LABEL_COLOR)
        self.screen.blit(instructions, (50, 90))
        
        # Section 1: Player Characters
        self.draw_section_label("Player Character (Animated)", 50, 130)
        directions = ['north', 'south', 'east', 'west']
        for i, direction in enumerate(directions):
            x = 80 + i * 150
            y = 200
            sprite = self.sprite_manager.get_player_sprite(direction, (TILE_SIZE, TILE_SIZE))
            if sprite:
                self.screen.blit(sprite, (x, y))
                label = self.label_font.render(direction.capitalize(), True, LABEL_COLOR)
                self.screen.blit(label, (x, y + TILE_SIZE + 10))
        
        # Section 2: Tiles
        self.draw_section_label("Tiles", 50, 320)
        tiles = [('floor', 'Floor'), ('grass', 'Grass'), ('wall', 'Wall')]
        for i, (tile_type, label_text) in enumerate(tiles):
            x = 80 + i * 150
            y = 390
            sprite = self.sprite_manager.get_tile_sprite(tile_type, (TILE_SIZE, TILE_SIZE))
            if sprite:
                self.screen.blit(sprite, (x, y))
                label = self.label_font.render(label_text, True, LABEL_COLOR)
                self.screen.blit(label, (x, y + TILE_SIZE + 10))
        
        # Section 3: Objects
        self.draw_section_label("Collectibles & Goal (Animated)", 650, 130)
        
        # Gem
        gem_x, gem_y = 700, 200
        gem_sprite = self.sprite_manager.get_gem_sprite((TILE_SIZE, TILE_SIZE))
        if gem_sprite:
            self.screen.blit(gem_sprite, (gem_x, gem_y))
            label = self.label_font.render("Gem", True, LABEL_COLOR)
            self.screen.blit(label, (gem_x, gem_y + TILE_SIZE + 10))
        
        # Goal
        goal_x, goal_y = 850, 200
        goal_sprite = self.sprite_manager.get_goal_sprite((TILE_SIZE, TILE_SIZE))
        if goal_sprite:
            self.screen.blit(goal_sprite, (goal_x, goal_y))
            label = self.label_font.render("Goal", True, LABEL_COLOR)
            self.screen.blit(label, (goal_x, goal_y + TILE_SIZE + 10))
        
        # Section 4: Example Level
        self.draw_section_label("Example Level", 650, 320)
        self.render_example_level(700, 390)
        
        # Render particles
        self.render_particles()
        
        # Stats
        stats_text = f"Sprites Loaded: {len(self.sprite_manager.sprites)} | Active Particles: {len(self.particle_system.particles)}"
        stats = self.small_font.render(stats_text, True, LABEL_COLOR)
        self.screen.blit(stats, (50, WINDOW_HEIGHT - 40))
        
        pygame.display.flip()
    
    def draw_section_label(self, text, x, y):
        """Draw a section label."""
        label = self.label_font.render(text, True, TEXT_COLOR)
        self.screen.blit(label, (x, y))
        # Underline
        pygame.draw.line(self.screen, TEXT_COLOR, (x, y + 30), (x + label.get_width(), y + 30), 2)
    
    def render_example_level(self, start_x, start_y):
        """Render a small example level."""
        # 5x5 mini level
        level_data = [
            ['floor', 'floor', 'wall', 'floor', 'floor'],
            ['floor', 'gem', 'wall', 'gem', 'floor'],
            ['floor', 'floor', 'floor', 'floor', 'floor'],
            ['wall', 'floor', 'player', 'floor', 'wall'],
            ['floor', 'floor', 'goal', 'floor', 'floor'],
        ]
        
        mini_tile = 48  # Smaller tiles for demo
        
        for row_idx, row in enumerate(level_data):
            for col_idx, tile_type in enumerate(row):
                x = start_x + col_idx * mini_tile
                y = start_y + row_idx * mini_tile
                
                # Background
                bg_type = 'grass' if (col_idx + row_idx) % 2 == 0 else 'floor'
                bg_sprite = self.sprite_manager.get_tile_sprite(bg_type, (mini_tile, mini_tile))
                if bg_sprite:
                    self.screen.blit(bg_sprite, (x, y))
                
                # Objects
                if tile_type == 'wall':
                    sprite = self.sprite_manager.get_tile_sprite('wall', (mini_tile, mini_tile))
                    if sprite:
                        self.screen.blit(sprite, (x, y))
                elif tile_type == 'gem':
                    sprite = self.sprite_manager.get_gem_sprite((mini_tile, mini_tile))
                    if sprite:
                        self.screen.blit(sprite, (x, y))
                elif tile_type == 'goal':
                    sprite = self.sprite_manager.get_goal_sprite((mini_tile, mini_tile))
                    if sprite:
                        self.screen.blit(sprite, (x, y))
                elif tile_type == 'player':
                    sprite = self.sprite_manager.get_player_sprite('south', (mini_tile, mini_tile))
                    if sprite:
                        self.screen.blit(sprite, (x, y))
    
    def render_particles(self):
        """Render particle effects."""
        for particle in self.particle_system.get_particles():
            # Draw particle
            particle_sprite = self.sprite_manager.get_particle_sprite('gem_yellow', (int(particle.size * 2), int(particle.size * 2)))
            if particle_sprite:
                rect = particle_sprite.get_rect(center=(int(particle.x), int(particle.y)))
                # Apply alpha based on lifetime
                alpha = int(255 * (particle.lifetime / particle.max_lifetime))
                particle_sprite.set_alpha(alpha)
                self.screen.blit(particle_sprite, rect)
            else:
                pygame.draw.circle(self.screen, particle.color, (int(particle.x), int(particle.y)), int(particle.size))


def main():
    """Run the sprite demo."""
    print("🎮 Starting Sprite Showcase Demo...")
    print("   Press SPACE or click to spawn particles")
    print("   Press ESC to exit")
    
    demo = SpriteDemo()
    demo.run()


if __name__ == "__main__":
    main()

