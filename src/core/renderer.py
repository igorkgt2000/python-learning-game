"""
Rendering system for the game.
"""

import pygame
from typing import Tuple, List, Optional
from .config import Config
from .grid import Grid, TileType
from .player import Player
from .level import Level
from .sprite_manager import SpriteManager
from .animation import ParticleSystem

class Renderer:
    """Handles all rendering operations for the game."""
    
    def __init__(self, screen: pygame.Surface, config: Config):
        """Initialize renderer with screen and configuration."""
        self.screen = screen
        self.config = config
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Initialize sprite manager
        self.sprite_manager = SpriteManager()
        
        # Initialize particle system
        self.particle_system = ParticleSystem()
        
        # Animation state
        self.last_update = 0.0
    
    def update(self, dt: float):
        """Update animations."""
        self.sprite_manager.update(dt)
        self.particle_system.update(dt)
        self.last_update += dt
    
    def render_grid(self, grid: Grid):
        """Render the game grid."""
        tile_size = (self.config.TILE_SIZE, self.config.TILE_SIZE)
        
        for y in range(grid.height):
            for x in range(grid.width):
                rect = pygame.Rect(
                    x * self.config.TILE_SIZE,
                    y * self.config.TILE_SIZE,
                    self.config.TILE_SIZE,
                    self.config.TILE_SIZE
                )
                
                # Draw floor tile (use grass for variety)
                floor_type = 'grass' if (x + y) % 3 == 0 else 'floor'
                floor_sprite = self.sprite_manager.get_tile_sprite(floor_type, tile_size)
                if floor_sprite:
                    self.screen.blit(floor_sprite, rect)
                else:
                    # Fallback to colored rectangle
                    pygame.draw.rect(self.screen, self.config.GRID_COLOR, rect)
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
                
                # Draw tile content on top
                self._draw_tile_content(x, y, grid.get_tile(x, y), rect)
    
    def _draw_tile_content(self, x: int, y: int, tile_type: TileType, rect: pygame.Rect):
        """Draw content of a specific tile."""
        tile_size = (self.config.TILE_SIZE, self.config.TILE_SIZE)
        
        if tile_type == TileType.WALL:
            # Draw wall sprite
            wall_sprite = self.sprite_manager.get_tile_sprite('wall', tile_size)
            if wall_sprite:
                self.screen.blit(wall_sprite, rect)
            else:
                pygame.draw.rect(self.screen, self.config.WALL_COLOR, rect)
        
        elif tile_type == TileType.GEM:
            # Draw animated gem sprite
            gem_sprite = self.sprite_manager.get_gem_sprite(tile_size)
            if gem_sprite:
                self.screen.blit(gem_sprite, rect)
            else:
                # Fallback to circle
                center = rect.center
                pygame.draw.circle(self.screen, self.config.GEM_COLOR, center, self.config.TILE_SIZE // 3)
        
        elif tile_type == TileType.GOAL:
            # Draw animated goal sprite
            goal_sprite = self.sprite_manager.get_goal_sprite(tile_size)
            if goal_sprite:
                self.screen.blit(goal_sprite, rect)
            else:
                # Fallback to square
                goal_rect = rect.inflate(-8, -8)
                pygame.draw.rect(self.screen, self.config.GOAL_COLOR, goal_rect)
    
    def render_player(self, player: Player):
        """Render the player character."""
        tile_size = (self.config.TILE_SIZE, self.config.TILE_SIZE)
        rect = pygame.Rect(
            player.x * self.config.TILE_SIZE,
            player.y * self.config.TILE_SIZE,
            self.config.TILE_SIZE,
            self.config.TILE_SIZE
        )
        
        # Draw animated player sprite
        player_sprite = self.sprite_manager.get_player_sprite(player.direction.value, tile_size)
        if player_sprite:
            self.screen.blit(player_sprite, rect)
        else:
            # Fallback to circle with arrow
            x = player.x * self.config.TILE_SIZE + self.config.TILE_SIZE // 2
            y = player.y * self.config.TILE_SIZE + self.config.TILE_SIZE // 2
            pygame.draw.circle(self.screen, self.config.PLAYER_COLOR, (x, y), self.config.TILE_SIZE // 3)
            self._draw_direction_arrow(x, y, player.direction.value)
    
    def _draw_direction_arrow(self, x: int, y: int, direction: str):
        """Draw a small arrow indicating player direction."""
        arrow_size = 8
        points = []
        
        if direction == "north":
            points = [(x, y - arrow_size), (x - arrow_size//2, y), (x + arrow_size//2, y)]
        elif direction == "east":
            points = [(x + arrow_size, y), (x, y - arrow_size//2), (x, y + arrow_size//2)]
        elif direction == "south":
            points = [(x, y + arrow_size), (x - arrow_size//2, y), (x + arrow_size//2, y)]
        elif direction == "west":
            points = [(x - arrow_size, y), (x, y - arrow_size//2), (x, y + arrow_size//2)]
        
        if points:
            pygame.draw.polygon(self.screen, (255, 255, 255), points)
    
    def render_level_objects(self, level: Level):
        """Render level-specific objects (already handled in grid rendering)."""
        pass  # Level objects are rendered as part of the grid
    
    def render_ui(self, player: Player, level: Level = None):
        """Render UI elements."""
        # Player info
        info_text = f"Position: ({player.x}, {player.y}) | Direction: {player.direction.value} | Steps: {player.step_count}"
        text_surface = self.font.render(info_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 10))
        
        # Level info
        if level:
            level_text = f"Level: {level.name if hasattr(level, 'name') else 'Unknown'}"
            level_surface = self.font.render(level_text, True, (0, 0, 0))
            self.screen.blit(level_surface, (10, 40))
            
            # Gems collected
            gems_text = f"Gems: {len(player.collected_gems)}/{level.get_total_gems()}"
            gems_surface = self.font.render(gems_text, True, (0, 0, 0))
            self.screen.blit(gems_surface, (10, 70))
    
    def render_hint(self, hint_text: str):
        """Render hint text."""
        if hint_text:
            # Render hint in a semi-transparent box
            hint_surface = self.small_font.render(hint_text, True, (0, 0, 0))
            hint_rect = hint_surface.get_rect()
            hint_rect.bottomright = (self.screen.get_width() - 10, self.screen.get_height() - 10)
            
            # Background box
            bg_rect = hint_rect.inflate(20, 10)
            bg_surface = pygame.Surface(bg_rect.size)
            bg_surface.set_alpha(200)
            bg_surface.fill((255, 255, 255))
            self.screen.blit(bg_surface, bg_rect.topleft)
            
            # Hint text
            self.screen.blit(hint_surface, hint_rect)
    
    def render_particles(self):
        """Render particle effects."""
        for particle in self.particle_system.get_particles():
            # Draw particle using sprite or circle
            particle_sprite = self.sprite_manager.get_particle_sprite('gem_yellow', (int(particle.size * 2), int(particle.size * 2)))
            if particle_sprite:
                rect = particle_sprite.get_rect(center=(int(particle.x), int(particle.y)))
                self.screen.blit(particle_sprite, rect)
            else:
                # Fallback to circle
                pygame.draw.circle(self.screen, particle.color, (int(particle.x), int(particle.y)), int(particle.size))
    
    def emit_collect_particles(self, x: int, y: int):
        """Emit particles for gem collection."""
        screen_x = x * self.config.TILE_SIZE + self.config.TILE_SIZE // 2
        screen_y = y * self.config.TILE_SIZE + self.config.TILE_SIZE // 2
        self.particle_system.emit(screen_x, screen_y, 15, (241, 196, 15), speed=150)
    
    def render_animation(self, animation_type: str, progress: float):
        """Render animation effects."""
        if animation_type == "move":
            # Animate movement between tiles
            pass  # Can be implemented with position interpolation
        elif animation_type == "collect":
            # Animate gem collection
            pass  # Handled by particle system
