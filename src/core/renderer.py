"""
Rendering system for the pixel art Python learning game.

This module handles ALL drawing operations, including:
- Grid tiles (floor, grass, walls)
- Game objects (gems, goals)
- Player character with animations
- Particle effects (gem collection sparkles)
- UI overlays (position, gems, steps)

The renderer uses hardware-accelerated Pygame surfaces and manages
sprite animations, particle systems, and UI text rendering.

Classes:
    Renderer: Main rendering engine

Dependencies:
    - SpriteManager: Loads and animates pixel art sprites
    - ParticleSystem: Manages particle effects
    - Pygame: For drawing and surface management
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
    """
    Main rendering engine for the game.
    
    Handles all visual output including tiles, sprites, particles, and UI.
    Uses pixel art sprites loaded by SpriteManager and animated particle
    effects from ParticleSystem.
    
    Rendering Pipeline:
        1. Grid (floor, walls)
        2. Game objects (gems, goals)
        3. Player character
        4. UI text overlays
        5. Particle effects
    
    Attributes:
        screen (pygame.Surface): Main display surface to draw on
        config (Config): Configuration with colors, sizes, paths
        font (pygame.font.Font): Large font for UI text (24pt)
        small_font (pygame.font.Font): Small font for labels (18pt)
        sprite_manager (SpriteManager): Manages sprite loading and animation
        particle_system (ParticleSystem): Manages particle effects
        last_update (float): Accumulated time for animations
    """
    
    def __init__(self, screen: pygame.Surface, config: Config):
        """
        Initialize the rendering system.
        
        Sets up fonts, sprite manager, and particle system.
        All rendering will be done to the provided screen surface.
        
        Args:
            screen (pygame.Surface): The main display surface (from pygame.display.set_mode)
            config (Config): Game configuration with tile sizes, colors, etc.
        
        Example:
            >>> screen = pygame.display.set_mode((800, 600))
            >>> renderer = Renderer(screen, Config())
        """
        self.screen = screen
        self.config = config
        
        # Initialize fonts for UI text
        self.font = pygame.font.Font(None, 24)  # Normal text
        self.small_font = pygame.font.Font(None, 18)  # Small labels
        
        # Initialize sprite manager for pixel art
        # This loads all sprites from assets/sprites/
        self.sprite_manager = SpriteManager()
        
        # Initialize particle system for visual effects
        # Handles gem collection sparkles, explosions, etc.
        self.particle_system = ParticleSystem()
        
        # Animation state tracking
        self.last_update = 0.0  # Accumulated delta time
    
    def update(self, dt: float):
        """
        Update all animations and visual effects.
        
        Called once per frame before rendering. Updates:
        - Sprite animations (gems pulsing, goals glowing)
        - Particle effects (movement, fading, physics)
        
        Args:
            dt (float): Delta time in seconds since last frame
        
        Performance:
            Very fast - just updates animation timers.
            Typical time: < 0.1ms
        
        Example:
            >>> dt = clock.get_time() / 1000.0
            >>> renderer.update(dt)
        """
        # Update sprite animations (gems, goals, etc.)
        self.sprite_manager.update(dt)
        
        # Update particle physics and lifetimes
        self.particle_system.update(dt)
        
        # Track total elapsed time (for potential future use)
        self.last_update += dt
    
    def render_grid(self, grid: Grid):
        """
        Render the entire game grid with all tiles.
        
        Draws a 2D grid of tiles including:
        - Floor/grass tiles (background)
        - Walls, gems, goals (on top of floor)
        
        Uses checkerboard pattern for variety (grass every 3rd tile).
        All sprites are scaled to TILE_SIZE and drawn as pixel art.
        
        Args:
            grid (Grid): The game grid containing tile data
        
        Performance:
            This is called 60 times per second. For a 10x10 grid,
            that's 6000 tile draws per second. Pygame optimizes this
            with hardware acceleration.
        """
        # Calculate tile size for sprite scaling
        tile_size = (self.config.TILE_SIZE, self.config.TILE_SIZE)
        
        # Loop through every tile in the grid
        for y in range(grid.height):
            for x in range(grid.width):
                # Calculate screen position for this tile
                rect = pygame.Rect(
                    x * self.config.TILE_SIZE,  # Left edge
                    y * self.config.TILE_SIZE,  # Top edge
                    self.config.TILE_SIZE,      # Width
                    self.config.TILE_SIZE       # Height
                )
                
                # LAYER 1: Draw floor tile (with grass for variety)
                # Use checkerboard pattern: grass every 3rd tile
                floor_type = 'grass' if (x + y) % 3 == 0 else 'floor'
                floor_sprite = self.sprite_manager.get_tile_sprite(floor_type, tile_size)
                
                if floor_sprite:
                    # Draw pixel art sprite
                    self.screen.blit(floor_sprite, rect)
                else:
                    # Fallback if sprite fails to load
                    pygame.draw.rect(self.screen, self.config.GRID_COLOR, rect)
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Border
                
                # LAYER 2: Draw tile content (walls, gems, goals)
                self._draw_tile_content(x, y, grid.get_tile(x, y), rect)
    
    def _draw_tile_content(self, x: int, y: int, tile_type: TileType, rect: pygame.Rect):
        """
        Draw the content of a specific tile (walls, gems, goals).
        
        Called by render_grid() for each tile. Draws different sprites
        based on tile type. All non-EMPTY tiles are drawn on top of
        the floor sprite.
        
        Args:
            x (int): Tile grid x coordinate
            y (int): Tile grid y coordinate
            tile_type (TileType): What type of tile to draw
            rect (pygame.Rect): Screen rectangle to draw in
        
        Note:
            EMPTY tiles don't draw anything (floor is already drawn).
            This is a private helper method (indicated by _ prefix).
        """
        tile_size = (self.config.TILE_SIZE, self.config.TILE_SIZE)
        
        if tile_type == TileType.WALL:
            # Draw stone wall sprite
            wall_sprite = self.sprite_manager.get_tile_sprite('wall', tile_size)
            if wall_sprite:
                self.screen.blit(wall_sprite, rect)
            else:
                # Fallback: solid color rectangle
                pygame.draw.rect(self.screen, self.config.WALL_COLOR, rect)
        
        elif tile_type == TileType.GEM:
            # Draw animated gem sprite (pulsing animation)
            gem_sprite = self.sprite_manager.get_gem_sprite(tile_size)
            if gem_sprite:
                self.screen.blit(gem_sprite, rect)
            else:
                # Fallback: yellow circle
                center = rect.center
                pygame.draw.circle(self.screen, self.config.GEM_COLOR, center, self.config.TILE_SIZE // 3)
        
        elif tile_type == TileType.GOAL:
            # Draw animated goal sprite (glowing animation)
            goal_sprite = self.sprite_manager.get_goal_sprite(tile_size)
            if goal_sprite:
                self.screen.blit(goal_sprite, rect)
            else:
                # Fallback: green square
                goal_rect = rect.inflate(-8, -8)  # Smaller than tile
                pygame.draw.rect(self.screen, self.config.GOAL_COLOR, goal_rect)
    
    def render_player(self, player: Player):
        """
        Render the player character sprite.
        
        Draws the robot character sprite facing the correct direction.
        The sprite is automatically selected based on player.direction
        and includes idle animations.
        
        Args:
            player (Player): The player to render
        
        Note:
            Player is drawn AFTER the grid so it appears on top of tiles.
            Position is in grid coordinates (x, y) not screen pixels.
        """
        tile_size = (self.config.TILE_SIZE, self.config.TILE_SIZE)
        
        # Calculate screen rectangle for player
        rect = pygame.Rect(
            player.x * self.config.TILE_SIZE,  # Convert grid to screen
            player.y * self.config.TILE_SIZE,
            self.config.TILE_SIZE,
            self.config.TILE_SIZE
        )
        
        # Draw animated player sprite facing correct direction
        player_sprite = self.sprite_manager.get_player_sprite(player.direction.value, tile_size)
        
        if player_sprite:
            # Draw pixel art robot sprite
            self.screen.blit(player_sprite, rect)
        else:
            # Fallback: circle with directional arrow
            x = player.x * self.config.TILE_SIZE + self.config.TILE_SIZE // 2
            y = player.y * self.config.TILE_SIZE + self.config.TILE_SIZE // 2
            pygame.draw.circle(self.screen, self.config.PLAYER_COLOR, (x, y), self.config.TILE_SIZE // 3)
            self._draw_direction_arrow(x, y, player.direction.value)
    
    def _draw_direction_arrow(self, x: int, y: int, direction: str):
        """
        Draw a directional arrow (fallback when sprites fail).
        
        Used only if player sprite fails to load. Draws a simple
        triangle pointing in the player's direction.
        
        Args:
            x (int): Screen x coordinate (center)
            y (int): Screen y coordinate (center)
            direction (str): Direction string ("north", "east", "south", "west")
        """
        arrow_size = 8  # Arrow extends 8 pixels from center
        points = []  # Triangle vertices
        
        # Calculate triangle points based on direction
        if direction == "north":
            points = [(x, y - arrow_size), (x - arrow_size//2, y), (x + arrow_size//2, y)]
        elif direction == "east":
            points = [(x + arrow_size, y), (x, y - arrow_size//2), (x, y + arrow_size//2)]
        elif direction == "south":
            points = [(x, y + arrow_size), (x - arrow_size//2, y), (x + arrow_size//2, y)]
        elif direction == "west":
            points = [(x - arrow_size, y), (x, y - arrow_size//2), (x, y + arrow_size//2)]
        
        # Draw white triangle
        if points:
            pygame.draw.polygon(self.screen, (255, 255, 255), points)
    
    def render_level_objects(self, level: Level):
        """
        Render level-specific objects.
        
        Currently a placeholder since all level objects (gems, goals)
        are stored in the Grid and rendered by render_grid().
        
        Args:
            level (Level): The current level
        
        Note:
            This method exists for future expansion. Later levels might
            have special objects that aren't grid-based (e.g., moving
            platforms, collectible keys, switches).
        """
        pass  # Level objects are currently rendered as part of the grid
    
    def render_ui(self, player: Player, level: Level = None):
        """
        Render UI text overlays (position, gems, steps).
        
        Draws informational text in the top-left corner including:
        - Player position and direction
        - Step count
        - Level name (if available)
        - Gems collected vs total gems
        
        Args:
            player (Player): Player to show stats for
            level (Level, optional): Current level for level-specific info
        
        Text Color:
            Uses black text (0, 0, 0) for good contrast on the game board.
        """
        # Line 1: Player position, direction, and steps
        info_text = f"Position: ({player.x}, {player.y}) | Direction: {player.direction.value} | Steps: {player.step_count}"
        text_surface = self.font.render(info_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (10, 10))  # Top-left corner
        
        # Additional lines if level is available
        if level:
            # Line 2: Level name
            level_text = f"Level: {level.name if hasattr(level, 'name') else 'Unknown'}"
            level_surface = self.font.render(level_text, True, (0, 0, 0))
            self.screen.blit(level_surface, (10, 40))
            
            # Line 3: Gems collected out of total
            gems_text = f"Gems: {len(player.collected_gems)}/{level.get_total_gems()}"
            gems_surface = self.font.render(gems_text, True, (0, 0, 0))
            self.screen.blit(gems_surface, (10, 70))
    
    def render_hint(self, hint_text: str):
        """
        Render hint text in bottom-right corner.
        
        Displays helpful hints in a semi-transparent white box.
        Used for level instructions or programming tips.
        
        Args:
            hint_text (str): Text to display (or empty string for no hint)
        
        Visual Design:
            - Small font (18pt)
            - Semi-transparent white background (alpha 200)
            - Black text
            - 10px padding
            - Bottom-right corner position
        """
        if hint_text:
            # Render text
            hint_surface = self.small_font.render(hint_text, True, (0, 0, 0))
            hint_rect = hint_surface.get_rect()
            hint_rect.bottomright = (self.screen.get_width() - 10, self.screen.get_height() - 10)
            
            # Draw background box (semi-transparent white)
            bg_rect = hint_rect.inflate(20, 10)  # Add padding
            bg_surface = pygame.Surface(bg_rect.size)
            bg_surface.set_alpha(200)  # Semi-transparent
            bg_surface.fill((255, 255, 255))
            self.screen.blit(bg_surface, bg_rect.topleft)
            
            # Draw text on top of background
            self.screen.blit(hint_surface, hint_rect)
    
    def render_particles(self):
        """
        Render all active particle effects.
        
        Draws each particle in the particle system. Particles are drawn
        LAST so they appear on top of everything else (grid, player, UI).
        
        Used for visual feedback when collecting gems, explosions, etc.
        
        Performance:
            Particles are small sprites (8-16px). Even with 50+ particles,
            rendering is very fast (< 0.5ms).
        """
        # Get all active particles from particle system
        for particle in self.particle_system.get_particles():
            # Try to draw with particle sprite
            particle_sprite = self.sprite_manager.get_particle_sprite(
                'gem_yellow',  # Gem sparkle sprite
                (int(particle.size * 2), int(particle.size * 2))  # Scale to particle size
            )
            
            if particle_sprite:
                # Draw sprite centered on particle position
                rect = particle_sprite.get_rect(center=(int(particle.x), int(particle.y)))
                self.screen.blit(particle_sprite, rect)
            else:
                # Fallback: simple colored circle
                pygame.draw.circle(
                    self.screen,
                    particle.color,  # Particle color
                    (int(particle.x), int(particle.y)),  # Position
                    int(particle.size)  # Radius
                )
    
    def emit_collect_particles(self, x: int, y: int):
        """
        Emit particle burst for gem collection.
        
        Creates a burst of 15 yellow particles that explode outward
        from the gem position. Provides satisfying visual feedback.
        
        Args:
            x (int): Grid x coordinate of collected gem
            y (int): Grid y coordinate of collected gem
        
        Particle Properties:
            - Count: 15 particles
            - Color: Gold/yellow (241, 196, 15)
            - Speed: 150 pixels/second
            - Lifetime: 0.8 seconds
            - Physics: Gravity and drag
        """
        # Convert grid coordinates to screen pixels (center of tile)
        screen_x = x * self.config.TILE_SIZE + self.config.TILE_SIZE // 2
        screen_y = y * self.config.TILE_SIZE + self.config.TILE_SIZE // 2
        
        # Emit burst of golden particles
        self.particle_system.emit(
            screen_x,              # X position
            screen_y,              # Y position
            15,                    # Number of particles
            (241, 196, 15),       # Gold color
            speed=150              # Initial speed
        )
    
    def render_animation(self, animation_type: str, progress: float):
        """
        Render smooth animations (future feature).
        
        Placeholder for future smooth animation system. Will interpolate
        player movement between tiles and animate other actions.
        
        Args:
            animation_type (str): Type of animation ("move", "collect", etc.)
            progress (float): Animation progress from 0.0 to 1.0
        
        TODO:
            - Implement smooth movement interpolation
            - Add turn animation (rotation)
            - Add bounce on landing
            - Integrate with Animation class from animation.py
        """
        if animation_type == "move":
            # TODO: Animate player movement between tiles
            # Interpolate position from old_pos to new_pos using progress
            pass  # Not yet implemented
        
        elif animation_type == "collect":
            # Gem collection animation is handled by particle system
            pass  # Already working
