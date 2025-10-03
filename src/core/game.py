"""
Main Game Engine - Central orchestrator for all game systems.

This module contains the Game class which is the heart of the application.
It coordinates all subsystems (rendering, input, code execution, levels) and
manages the main game loop.

Architecture:
    Game (this class) is the top-level coordinator
    ├── Renderer (graphics and animation)
    ├── Player (character state)
    ├── Grid (world state)
    ├── Level (current level data)
    ├── CodeExecutor (secure code execution)
    └── Pygame (window and event handling)

Game Flow:
    1. User writes Python code in editor
    2. Code is validated for security
    3. Code is executed in sandbox
    4. Player actions are animated
    5. Level completion is checked
    6. Progress to next level or retry

Main Loop:
    while running:
        handle_events()  # Keyboard, mouse, window events
        update()         # Game logic, animations
        render()         # Draw everything
        clock.tick(60)   # Maintain 60 FPS

Usage Example:
    >>> config = Config()
    >>> game = Game(config)
    >>> game.load_level(0)
    >>> game.run()  # Starts main loop

Author: Python Learning Game Team
Version: 2.0
Last Modified: October 2, 2025
"""

import pygame
import sys
from typing import Optional, List, Tuple
from enum import Enum

from .config import Config
from .grid import Grid, TileType
from .player import Player
from .renderer import Renderer
from .level import Level
from .code_executor import CodeExecutor

class GameState(Enum):
    """
    Game state machine enumeration.
    
    The game is always in exactly one state. State determines:
    - What is rendered on screen
    - Which inputs are active
    - What game logic runs
    
    States:
        MENU: Title screen, level selection (not yet implemented)
        PLAYING: Active gameplay, user can write and run code
        LEVEL_COMPLETE: Victory screen after completing a level
        GAME_OVER: Failure screen (if applicable)
        PAUSED: Game paused, awaiting resume (not yet implemented)
    
    State Transitions:
        MENU → PLAYING: Load a level
        PLAYING → LEVEL_COMPLETE: Complete level objectives
        LEVEL_COMPLETE → PLAYING: Load next level
        PLAYING → PAUSED: Press pause button
        PAUSED → PLAYING: Resume
    """
    MENU = "menu"                    # Not in a level yet
    PLAYING = "playing"              # Active gameplay
    LEVEL_COMPLETE = "level_complete"  # Just finished a level
    GAME_OVER = "game_over"          # Failed (not currently used)
    PAUSED = "paused"                # Game paused (not yet implemented)

class Game:
    """
    Main game engine that orchestrates all systems.
    
    The Game class is responsible for:
    - Managing game state (menu, playing, complete)
    - Running the main game loop
    - Coordinating subsystems (render, input, code execution)
    - Loading and progressing through levels
    - Animating player actions
    - Checking victory conditions
    
    Attributes:
        config (Config): Game configuration settings
        state (GameState): Current game state
        current_level (Level): Currently loaded level (None if in menu)
        level_index (int): Index of current level (0-based)
        screen (pygame.Surface): Main game window surface
        clock (pygame.time.Clock): FPS regulation clock
        grid (Grid): Game world grid
        player (Player): Player character
        renderer (Renderer): Rendering system
        code_executor (CodeExecutor): Secure code execution system
        running (bool): Main loop flag
        animation_queue (List[str]): Actions waiting to be animated
        animating (bool): True if currently animating actions
    
    Main Loop Flow:
        1. Handle Events (keyboard, mouse, close window)
        2. Update (animations, game logic)
        3. Render (draw everything)
        4. Regulate FPS (60 FPS target)
    
    Example:
        >>> game = Game(Config())
        >>> game.load_level(0)
        >>> game.run()  # Blocks until game closes
    """
    
    def __init__(self, config: Config):
        """
        Initialize the game with all subsystems.
        
        Sets up Pygame, creates the window, and initializes all game
        systems. The game starts in MENU state by default.
        
        Args:
            config (Config): Configuration object with all settings
        
        Side Effects:
            - Initializes Pygame
            - Creates game window
            - Sets window title
            - Creates all subsystem instances
        
        Note:
            This does NOT load a level or start the game loop.
            Call load_level() and run() after initialization.
        
        Example:
            >>> config = Config()
            >>> game = Game(config)
            >>> game.state
            <GameState.MENU: 'menu'>
        """
        # Store configuration for access by all systems
        self.config = config
        
        # Start in menu state (not playing yet)
        self.state = GameState.MENU
        
        # No level loaded initially
        self.current_level: Optional[Level] = None
        self.level_index = 0  # First level is index 0
        
        # ==================== PYGAME INITIALIZATION ====================
        # Initialize Pygame library (required before using any Pygame features)
        pygame.init()
        
        # Set window title (appears in title bar)
        pygame.display.set_caption(config.WINDOW_TITLE)
        
        # Create game window with specified dimensions
        # Returns a Surface object representing the window
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        
        # Create clock for FPS regulation (maintains consistent frame rate)
        self.clock = pygame.time.Clock()
        
        # ==================== GAME SUBSYSTEMS ====================
        # Create instances of all game systems
        
        # Grid: The game world (tiles, walls, gems, goals)
        self.grid = Grid(config.GRID_SIZE, config.GRID_SIZE)
        
        # Player: The character controlled by user code
        # Starts at (0, 0) facing north (will be reset when level loads)
        self.player = Player(0, 0, "north")
        
        # Renderer: Handles all drawing (sprites, particles, UI)
        self.renderer = Renderer(self.screen, config)
        
        # CodeExecutor: Secure execution of user Python code
        # This is the security-critical component
        self.code_executor = CodeExecutor(config)
        
        # ==================== GAME STATE ====================
        # Main loop control
        self.running = True  # Set to False to exit game loop
        
        # Animation system (for smooth action playback)
        self.animation_queue: List[str] = []  # Actions waiting to animate
        self.animating = False  # True while animations are playing
        
    def run(self):
        """
        Main game loop - runs until game is closed.
        
        This is the heart of the game. It continuously cycles through:
        1. Handle events (keyboard, mouse, window)
        2. Update (game logic, animations)
        3. Render (draw everything)
        4. Regulate FPS (maintain 60 FPS)
        
        The loop runs until self.running is set to False (ESC key or close window).
        
        Note:
            This method blocks - it doesn't return until the game exits.
            Call this after loading a level to start playing.
        
        Side Effects:
            - Quits Pygame when loop exits
            - Calls sys.exit() to terminate program
        
        Example:
            >>> game = Game(Config())
            >>> game.load_level(0)
            >>> game.run()  # Blocks until user closes game
        """
        # Main loop continues while running flag is True
        while self.running:
            # Step 1: Process all user input and window events
            self.handle_events()
            
            # Step 2: Update game state, animations, logic
            self.update()
            
            # Step 3: Draw everything to screen
            self.render()
            
            # Step 4: Regulate frame rate to 60 FPS
            # This sleeps for the appropriate time to maintain consistent FPS
            self.clock.tick(60)
        
        # Loop exited - clean up and exit
        pygame.quit()  # Shut down Pygame subsystems
        sys.exit()     # Exit the program
    
    def handle_events(self):
        """
        Process all Pygame events (input, window events).
        
        Called once per frame. Processes all events in the queue including:
        - Window close button (QUIT)
        - Keyboard input (KEYDOWN)
        - Mouse clicks (not yet implemented)
        
        Events are queued by Pygame and must be processed each frame
        to prevent the window from becoming unresponsive.
        
        Side Effects:
            - May set self.running to False (to exit game)
            - Calls handle_keydown() for keyboard events
        
        Note:
            This must be called every frame, even if we don't care about
            events, otherwise the OS will think the window has frozen.
        """
        # Get all events that have occurred since last frame
        for event in pygame.event.get():
            # Check event type to determine how to handle it
            
            if event.type == pygame.QUIT:
                # User clicked window close button (X)
                self.running = False  # Exit main loop
            
            elif event.type == pygame.KEYDOWN:
                # User pressed a key
                self.handle_keydown(event.key)  # Delegate to key handler
    
    def handle_keydown(self, key):
        """
        Handle keyboard key press events.
        
        Called by handle_events() when a key is pressed.
        Different keys trigger different actions based on game state.
        
        Args:
            key: Pygame key constant (e.g., pygame.K_ESCAPE)
        
        Current Key Bindings:
            ESC: Exit game (always)
            SPACE: Execute code (when PLAYING, not yet connected to UI)
        
        TODO:
            - Connect SPACE to code editor's run button
            - Add P for pause
            - Add R for reset level
            - Add N for next level (in LEVEL_COMPLETE state)
        
        Example:
            >>> game.handle_keydown(pygame.K_ESCAPE)
            # Sets game.running = False
        """
        if key == pygame.K_ESCAPE:
            # ESC always exits the game
            self.running = False
        
        elif key == pygame.K_SPACE and self.state == GameState.PLAYING:
            # SPACE runs code when playing
            # TODO: Connect this to code editor UI
            # Will call: self.execute_code(editor.get_code())
            pass  # Not yet implemented
    
    def update(self):
        """
        Update all game logic and animations.
        
        Called once per frame after handle_events() and before render().
        Updates all game systems including:
        - Renderer animations (sprites, particles)
        - Action queue animations
        - Victory condition checking
        
        The update order matters:
        1. Calculate delta time (for smooth animations)
        2. Update renderer (sprite animations, particles)
        3. Update game logic (only when PLAYING)
        
        Performance:
            This runs 60 times per second, so keep it fast!
            Typical update time: < 1ms
        """
        # Calculate time since last frame (in seconds)
        # Used for frame-rate independent animations
        dt = self.clock.get_time() / 1000.0  # Convert milliseconds to seconds
        
        # Update renderer subsystems (sprites, particles)
        # This animates gems, goals, and particle effects
        self.renderer.update(dt)
        
        # Only update game logic when actively playing
        if self.state == GameState.PLAYING:
            # Update action animations (move, turn)
            self.update_animations()
            
            # Check if player has won the level
            self.check_level_completion()
    
    def update_animations(self):
        """
        Update action animation queue.
        
        When user code executes, it generates a list of actions
        (move_forward, turn_left, etc.). This method processes that
        queue and animates each action in sequence.
        
        TODO: Implement smooth action animations
            - Pop action from queue
            - Animate over 0.3-0.5 seconds
            - Move to next action when complete
            - Clear animating flag when queue empty
        
        Current Status:
            Placeholder - animations play instantly for now.
            Will be connected to animation system later.
        """
        if self.animating and self.animation_queue:
            # Process next animation in queue
            # TODO: Implement smooth animation playback
            # This will use the Animation class from animation.py
            pass  # Not yet implemented
    
    def check_level_completion(self):
        """
        Check if player has completed the current level.
        
        Victory requires:
        1. Player is standing on goal tile
        2. Player has collected all gems
        
        Both conditions are checked by level.is_completed().
        
        Side Effects:
            If level is complete:
            - Changes state to LEVEL_COMPLETE
            - Increments level_index for next level
            - TODO: Show victory screen
            - TODO: Save progress
        
        Note:
            Called every frame while PLAYING, so it's very lightweight.
            The actual checking is done in Level class.
        """
        # Check if we have a level loaded and if it's complete
        if self.current_level and self.current_level.is_completed(self.player, self.grid):
            # Level complete! Transition to victory state
            self.state = GameState.LEVEL_COMPLETE
            
            # Increment index for next level
            self.level_index += 1
            
            # TODO: Show victory screen with stats
            # TODO: Save progress to database
            # TODO: Award achievements
    
    def render(self):
        """
        Render everything to the screen.
        
        Called once per frame after update(). Draws everything in layers:
        1. Background (solid color fill)
        2. Grid tiles (floor, grass, walls)
        3. Level objects (gems, goals)
        4. Player character
        5. UI (info text, hints)
        6. Particle effects (on top of everything)
        7. Flip display (show to user)
        
        Rendering Order Matters:
            Items drawn later appear on top of earlier items.
            Particles are drawn last so they appear above everything.
        
        Performance:
            This runs 60 times per second.
            All rendering is hardware-accelerated by Pygame.
            Typical render time: 1-3ms
        
        Note:
            Different things are rendered based on game state.
            Currently only PLAYING state is fully implemented.
        """
        # Layer 1: Clear screen with background color
        self.screen.fill(self.config.BACKGROUND_COLOR)
        
        # Only render game world when in PLAYING state
        if self.state == GameState.PLAYING:
            # Layer 2: Render grid (floor, walls, gems, goals)
            # This draws all tile sprites
            self.renderer.render_grid(self.grid)
            
            # Layer 3: Render player character
            # This draws animated player sprite
            self.renderer.render_player(self.player)
            
            # Layer 4 & 5: Render level-specific content and UI
            if self.current_level:
                # Level objects (already included in grid rendering)
                self.renderer.render_level_objects(self.current_level)
                
                # UI overlay (position, gems, steps)
                self.renderer.render_ui(self.player, self.current_level)
            
            # Layer 6: Render particle effects (on top of everything)
            # This draws gem collection sparkles, etc.
            self.renderer.render_particles()
        
        # Layer 7: Flip display buffer to show on screen
        # This makes everything we drew visible to the user
        # Double-buffering prevents flickering
        pygame.display.flip()
    
    def load_level_from_data(self, level: Level) -> bool:
        """
        Load a level from a Level object (loaded from JSON).
        
        This method takes a pre-constructed Level object and sets up
        the game with it. Used by the UI when loading from LevelLoader.
        
        Args:
            level (Level): Level object to load
        
        Returns:
            bool: True if level loaded successfully
        
        Side Effects:
            - Sets self.current_level
            - Creates new Grid with level's grid_size
            - Resets player to starting position
            - Sets up obstacles and gems in grid
            - Changes state to PLAYING
        
        Example:
            >>> level = Level.from_dict(level_data)
            >>> game.load_level_from_data(level)
            True
        """
        try:
            # Set the current level
            self.current_level = level
            
            # Create new grid with level's size
            self.grid = Grid(level.grid_size, level.grid_size)
            
            # Set up obstacles
            for obstacle in level.obstacles:
                self.grid.set_tile(obstacle[0], obstacle[1], TileType.WALL)
            
            # Set up gems
            for gem in level.gems:
                self.grid.set_tile(gem[0], gem[1], TileType.GEM)
            
            # Set up goal
            self.grid.set_tile(level.goal_pos[0], level.goal_pos[1], TileType.GOAL)
            
            # Reset player to level's starting position
            self.player = Player(level.start_pos[0], level.start_pos[1])
            
            # Set game state to playing
            self.state = GameState.PLAYING
            
            # Reset level index (will be set by caller)
            self.level_index = 0
            
            return True
            
        except Exception as e:
            print(f"Error loading level: {e}")
            return False
    
    def load_level(self, level_index: int) -> bool:
        """
        Load and initialize a specific level.
        
        This method:
        1. Creates or loads level data
        2. Resets player to starting position
        3. Changes game state to PLAYING
        
        Args:
            level_index (int): Zero-based level index to load
        
        Returns:
            bool: True if level loaded successfully, False on error
        
        Side Effects:
            - Sets self.current_level
            - Resets player position and direction
            - Changes state to PLAYING
            - TODO: Will load from JSON files in levels/ directory
        
        Current Implementation:
            Creates a simple test level. Will be replaced with
            level loader that reads from JSON files.
        
        Example:
            >>> game.load_level(0)  # Load first level
            True
            >>> game.state
            <GameState.PLAYING: 'playing'>
        """
        try:
            # TODO: Replace with actual level loading from JSON files
            # This should use LevelLoader to load from src/levels/level_XX.json
            # For now, create a simple test level
            self.current_level = Level(
                start_pos=(0, 0),         # Top-left corner
                goal_pos=(9, 9),          # Bottom-right corner
                obstacles=[],             # No obstacles for test
                gems=[],                  # No gems for test
                grid_size=10,             # 10x10 grid
                hint="Move to the goal!" # Help text
            )
            
            # Reset player to level's starting position
            self.player.x, self.player.y = self.current_level.start_pos
            self.player.direction = "north"  # Always start facing north
            
            # Reset player state
            self.player.collected_gems.clear()
            self.player.step_count = 0
            
            # Change to playing state
            self.state = GameState.PLAYING
            
            return True  # Success
            
        except Exception as e:
            # Handle level loading errors
            print(f"Error loading level {level_index}: {e}")
            return False  # Failure
    
    def execute_code(self, code: str) -> Tuple[bool, str]:
        """
        Validate and execute user-submitted Python code.
        
        This is called when the user clicks "Run" in the code editor.
        It's a high-level wrapper around the secure code executor.
        
        Process:
            1. Validate code for security (AST-based)
            2. Execute in sandboxed environment
            3. Queue actions for animation
            4. Return success/failure message
        
        Args:
            code (str): User's Python code from the editor
        
        Returns:
            Tuple[bool, str]: (success, message)
                - success: True if code ran without errors
                - message: Success message or error description
        
        Side Effects:
            - If successful: Queues actions in animation_queue
            - Sets animating flag to True
            - Player state may be modified by code
        
        Security:
            Uses CodeExecutor which provides multiple layers of protection.
            See code_executor.py for full security model.
        
        Example:
            >>> success, msg = game.execute_code("move_forward()")
            >>> success
            True
            >>> msg
            'Code executed successfully'
        """
        try:
            # STEP 1: Validate code for security (AST-based)
            # This catches dangerous operations BEFORE execution
            if not self.code_executor.validate_code(code):
                return False, "Invalid code: contains forbidden operations"
            
            # STEP 2: Execute code in secure sandbox
            # Player and grid are passed so code can interact with game
            result = self.code_executor.execute_code(code, self.player, self.grid)
            
            # STEP 3: Process execution result
            if result["success"]:
                # Code ran successfully!
                
                # Queue all actions for animation
                # Actions are strings like "move_forward", "turn_left"
                self.animation_queue.extend(result["actions"])
                
                # Start animating if there are actions
                if self.animation_queue:
                    self.animating = True
                
                return True, "Code executed successfully"
            else:
                # Code failed with an error
                return False, result["error"]
                
        except Exception as e:
            # Unexpected error (shouldn't happen if CodeExecutor is working)
            return False, f"Execution error: {str(e)}"
    
    def start_new_game(self):
        """
        Start a new game from the first level.
        
        Resets the game to level 1 (index 0). Used when starting
        a new game from the main menu or restarting after game over.
        
        Side Effects:
            - Sets level_index to 0
            - Loads first level
            - Resets player state
        
        Example:
            >>> game.start_new_game()
            # Level 1 is loaded and ready to play
        """
        # Reset to first level
        self.level_index = 0
        
        # Load level 1
        self.load_level(0)
    
    def next_level(self):
        """
        Advance to the next level in sequence.
        
        Called after completing a level. Attempts to load the next
        level in the progression. If no more levels exist, transitions
        to GAME_OVER state (game complete).
        
        Side Effects:
            - Attempts to load level at current level_index
            - If successful: state becomes PLAYING
            - If failed: state becomes GAME_OVER
        
        Note:
            level_index should already be incremented by check_level_completion()
            before calling this method.
        
        Example:
            >>> game.next_level()  # Load next level
            # Either loads next level or shows game complete
        """
        # Try to load the next level
        if self.load_level(self.level_index):
            # Successfully loaded next level
            self.state = GameState.PLAYING
        else:
            # No more levels - game complete!
            self.state = GameState.GAME_OVER
            # TODO: Show congratulations screen
            # TODO: Display final statistics
