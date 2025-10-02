"""
Main game engine for the Python Learning Game.
"""

import pygame
import sys
from typing import Optional, List, Tuple
from enum import Enum

from .config import Config
from .grid import Grid
from .player import Player
from .renderer import Renderer
from .level import Level
from .code_executor import CodeExecutor

class GameState(Enum):
    """Game state enumeration."""
    MENU = "menu"
    PLAYING = "playing"
    LEVEL_COMPLETE = "level_complete"
    GAME_OVER = "game_over"
    PAUSED = "paused"

class Game:
    """Main game class that orchestrates all game systems."""
    
    def __init__(self, config: Config):
        """Initialize the game with configuration."""
        self.config = config
        self.state = GameState.MENU
        self.current_level: Optional[Level] = None
        self.level_index = 0
        
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption(config.WINDOW_TITLE)
        
        # Create game window
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Initialize game systems
        self.grid = Grid(config.GRID_SIZE, config.GRID_SIZE)
        self.player = Player(0, 0, "north")
        self.renderer = Renderer(self.screen, config)
        self.code_executor = CodeExecutor(config)
        
        # Game state
        self.running = True
        self.animation_queue: List[str] = []
        self.animating = False
        
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # 60 FPS
            
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
    
    def handle_keydown(self, key):
        """Handle key press events."""
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_SPACE and self.state == GameState.PLAYING:
            # Space bar to execute code (will be connected to UI)
            pass
    
    def update(self):
        """Update game state."""
        # Calculate delta time
        dt = self.clock.get_time() / 1000.0  # Convert to seconds
        
        # Update renderer animations
        self.renderer.update(dt)
        
        if self.state == GameState.PLAYING:
            self.update_animations()
            self.check_level_completion()
    
    def update_animations(self):
        """Update character animations."""
        if self.animating and self.animation_queue:
            # Process next animation in queue
            # This will be implemented with the animation system
            pass
    
    def check_level_completion(self):
        """Check if current level is completed."""
        if self.current_level and self.current_level.is_completed(self.player, self.grid):
            self.state = GameState.LEVEL_COMPLETE
            self.level_index += 1
    
    def render(self):
        """Render the game."""
        self.screen.fill(self.config.BACKGROUND_COLOR)
        
        if self.state == GameState.PLAYING:
            self.renderer.render_grid(self.grid)
            self.renderer.render_player(self.player)
            if self.current_level:
                self.renderer.render_level_objects(self.current_level)
                self.renderer.render_ui(self.player, self.current_level)
            
            # Render particle effects on top
            self.renderer.render_particles()
        
        pygame.display.flip()
    
    def load_level(self, level_index: int) -> bool:
        """Load a specific level."""
        try:
            # This will load level data from files
            # For now, create a simple test level
            self.current_level = Level(
                start_pos=(0, 0),
                goal_pos=(9, 9),
                obstacles=[],
                gems=[],
                grid_size=10,
                hint="Move to the goal!"
            )
            
            # Reset player position
            self.player.x, self.player.y = self.current_level.start_pos
            self.player.direction = "north"
            
            self.state = GameState.PLAYING
            return True
            
        except Exception as e:
            print(f"Error loading level {level_index}: {e}")
            return False
    
    def execute_code(self, code: str) -> Tuple[bool, str]:
        """Execute user code safely."""
        try:
            # Parse and validate code
            if not self.code_executor.validate_code(code):
                return False, "Invalid code: contains forbidden operations"
            
            # Execute code in safe environment
            result = self.code_executor.execute_code(code, self.player, self.grid)
            
            if result["success"]:
                # Queue animations for player actions
                self.animation_queue.extend(result["actions"])
                self.animating = True
                return True, "Code executed successfully"
            else:
                return False, result["error"]
                
        except Exception as e:
            return False, f"Execution error: {str(e)}"
    
    def start_new_game(self):
        """Start a new game from level 1."""
        self.level_index = 0
        self.load_level(0)
    
    def next_level(self):
        """Advance to next level."""
        if self.load_level(self.level_index):
            self.state = GameState.PLAYING
        else:
            self.state = GameState.GAME_OVER
