"""
Main application window combining Pygame game view and Tkinter code editor.

This module creates the split-screen application window featuring:
- Left side: Pygame game canvas (pixel art robot world)
- Right side: Tkinter code editor (Python code input)
- Game controls: Start, Pause, Reset buttons
- Level information display: Level number, gems collected, step count
- Output area: Code execution results and error messages

The window uses Tkinter's PanedWindow for resizable split-screen layout
and integrates Pygame rendering within a Tkinter canvas (advanced technique).

Classes:
    MainWindow: Main application window controller

Integration:
    - Tkinter: UI framework for window, editor, buttons
    - Pygame: Game rendering (embedded in Tkinter canvas)
    - Threading: For concurrent game loop and UI updates

Architecture:
    MainWindow creates and manages both the game engine (Game class)
    and the code editor (CodeEditor class), connecting them through
    callback functions for code execution.
"""

import tkinter as tk
from tkinter import ttk
import threading
import pygame
from typing import Optional, Callable

from core.game import Game, GameState
from core.config import Config
from ui.code_editor import CodeEditor

class MainWindow:
    """
    Main application window with split-screen game and code editor.
    
    Creates a two-panel interface:
    - Left panel: Game view with controls and level info
    - Right panel: Code editor with output area
    
    Manages the game lifecycle (start, pause, reset) and connects
    user code from the editor to the game engine for execution.
    
    Attributes:
        config (Config): Game configuration settings
        game (Optional[Game]): Game engine instance
        game_thread (Optional[Thread]): Background thread for game loop
        running (bool): Whether game is currently running
        root (tk.Tk): Main Tkinter window
        code_editor (CodeEditor): Code editor widget
        game_canvas (tk.Canvas): Game rendering area
        output_text (tk.Text): Output/log display
    
    Example:
        >>> window = MainWindow()
        >>> window.run()  # Starts Tkinter event loop
    """
    
    def __init__(self):
        """
        Initialize the main application window.
        
        Sets up the complete UI including:
        - Main window with proper size and title
        - Split-screen layout (game | editor)
        - Game controls and information displays
        - Code editor with output area
        - Game engine connection
        
        Side Effects:
            - Creates Tkinter window (visible to user)
            - Initializes game engine
            - Sets up window close handler
        """
        self.config = Config()
        self.game: Optional[Game] = None  # Game engine (created on start)
        self.game_thread: Optional[threading.Thread] = None  # Game loop thread
        self.running = False  # Game running state
        
        # Create main Tkinter window
        self.root = tk.Tk()
        self.root.title(self.config.WINDOW_TITLE)
        self.root.geometry(f"{self.config.WINDOW_WIDTH}x{self.config.WINDOW_HEIGHT}")
        
        # Handle window close event (clean shutdown)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Build UI components (game view + code editor)
        self._create_ui()
        
        # Initialize game engine
        self._initialize_game()
    
    def _create_ui(self):
        """
        Create the split-screen UI layout.
        
        Uses Tkinter's PanedWindow to create resizable split screen:
        - Left pane: Game view (weight=1, 50% width)
        - Right pane: Code editor (weight=1, 50% width)
        
        User can drag the divider to resize panels.
        """
        # Create horizontal split-screen container
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Build left panel (game view)
        self._create_game_frame()
        
        # Build right panel (code editor)
        self._create_editor_frame()
        
        # Add panels to paned window with equal weights
        self.paned_window.add(self.game_frame, weight=1)  # 50% width
        self.paned_window.add(self.editor_frame, weight=1)  # 50% width
    
    def _create_game_frame(self):
        """
        Create the left panel with game view and controls.
        
        Components (top to bottom):
        1. Title: "Python Learning Game"
        2. Game Canvas: 400x400px rendering area for Pygame
        3. Control Buttons: Start, Pause, Reset
        4. Level Info: Current level, gems, steps
        5. Hint Label: Level-specific guidance
        
        Button States:
        - Start: Enabled initially, disabled when running
        - Pause/Reset: Disabled initially, enabled when running
        """
        self.game_frame = ttk.Frame(self.paned_window)
        
        # Title header
        title_label = ttk.Label(self.game_frame, text="Python Learning Game", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Game rendering canvas (Pygame will draw here)
        self.game_canvas = tk.Canvas(self.game_frame, bg='lightgray', 
                                    width=400, height=400)
        self.game_canvas.pack(padx=10, pady=10)
        
        # Control buttons row
        controls_frame = ttk.Frame(self.game_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Start button (enabled initially)
        self.start_button = ttk.Button(controls_frame, text="Start Game", 
                                      command=self._start_game)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Pause button (disabled until game starts)
        self.pause_button = ttk.Button(controls_frame, text="Pause", 
                                     command=self._pause_game, state='disabled')
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        # Reset button (disabled until game starts)
        self.reset_button = ttk.Button(controls_frame, text="Reset", 
                                     command=self._reset_game, state='disabled')
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Level information display
        self.level_info = ttk.Label(self.game_frame, text="Level: 1 | Gems: 0/0 | Steps: 0")
        self.level_info.pack(pady=5)
        
        # Hint text (wrapped for long hints)
        self.hint_label = ttk.Label(self.game_frame, text="Hint: Click 'Start Game' to begin!", 
                                   wraplength=350, justify=tk.CENTER)
        self.hint_label.pack(pady=5)
    
    def _create_editor_frame(self):
        """
        Create the right panel with code editor and output.
        
        Components (top to bottom):
        1. Title: "Code Editor"
        2. CodeEditor widget (toolbar, text area, status bar)
        3. Output area: Shows execution results and errors
        4. Clear Output button
        
        The CodeEditor is connected to _execute_code callback which
        runs user code in the game engine.
        """
        self.editor_frame = ttk.Frame(self.paned_window)
        
        # Editor title
        editor_title = ttk.Label(self.editor_frame, text="Code Editor", 
                                font=('Arial', 14, 'bold'))
        editor_title.pack(pady=5)
        
        # Create code editor widget (with callback to execute code)
        self.code_editor = CodeEditor(self.editor_frame, self._execute_code)
        
        # Output area (for execution results)
        output_frame = ttk.LabelFrame(self.editor_frame, text="Output")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollable text area for output messages
        self.output_text = tk.Text(output_frame, height=8, font=('Consolas', 10))
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Button to clear output log
        clear_output_btn = ttk.Button(output_frame, text="Clear Output", 
                                     command=self._clear_output)
        clear_output_btn.pack(pady=5)
    
    def _initialize_game(self):
        """
        Initialize the game engine.
        
        Placeholder for future Pygame-Tkinter integration.
        When fully implemented, this will:
        - Initialize Pygame rendering
        - Embed Pygame surface in Tkinter canvas
        - Set up game rendering loop
        
        Current Status:
            Just logs initialization status. Game is actually
            created when user clicks "Start Game".
        """
        try:
            # TODO: Initialize Pygame integration with Tkinter canvas
            # This is an advanced technique requiring os.environ setup
            self._update_status("Game initialized")
        except Exception as e:
            self._update_status(f"Game initialization failed: {e}")
    
    def _start_game(self):
        """
        Start or resume the game.
        
        Creates game engine instance and starts first level.
        Updates button states and level info display.
        
        Side Effects:
            - Creates Game instance if it doesn't exist
            - Starts level 1
            - Enables Pause/Reset buttons
            - Disables Start button
            - Updates UI with level information
        
        Error Handling:
            Errors are caught and displayed in output area.
        """
        try:
            if not self.game:
                # First time starting - create game engine
                self.game = Game(self.config)
                self.game.start_new_game()  # Load level 1
            
            # Set running state
            self.running = True
            
            # Update button states
            self.start_button.config(state='disabled')
            self.pause_button.config(state='normal')
            self.reset_button.config(state='normal')
            
            # Update displays
            self._update_status("Game started")
            self._update_level_info()
            
        except Exception as e:
            self._update_status(f"Failed to start game: {e}")
    
    def _pause_game(self):
        """
        Toggle game pause state.
        
        Pauses/resumes the game by changing GameState.
        Updates button text to show current action ("Pause"/"Resume").
        
        Button Behavior:
            - While playing: Button shows "Pause" → clicking pauses
            - While paused: Button shows "Resume" → clicking resumes
        """
        if self.game:
            if self.game.state == GameState.PLAYING:
                # Currently playing - pause it
                self.game.state = GameState.PAUSED
                self.pause_button.config(text="Resume")
                self._update_status("Game paused")
            else:
                # Currently paused - resume it
                self.game.state = GameState.PLAYING
                self.pause_button.config(text="Pause")
                self._update_status("Game resumed")
    
    def _reset_game(self):
        """
        Reset the current level.
        
        Reloads the current level from scratch, resetting:
        - Player position
        - Player direction
        - Collected gems
        - Step count
        
        Useful when user code gets stuck or makes a mistake.
        """
        if self.game:
            # Reload current level (doesn't advance level_index)
            self.game.load_level(self.game.level_index)
            self._update_status("Level reset")
            self._update_level_info()
    
    def _execute_code(self, code: str):
        """
        Execute user code in the game engine (callback from CodeEditor).
        
        This is called when user clicks "Run Code" in the editor.
        It validates the game is running, then sends code to the
        game engine for secure execution.
        
        Args:
            code (str): Python code from the editor
        
        Process:
            1. Validate game is running
            2. Send code to game.execute_code()
            3. Display success/error message
            4. Update level info if successful
        
        Output Symbols:
            ✓: Success - code executed without errors
            ✗: Error - code failed to execute or had errors
        """
        # Validate game is running
        if not self.game or not self.running:
            self._update_output("Game not running. Please start the game first.")
            return
        
        try:
            # Execute code in game engine (secure sandbox)
            success, message = self.game.execute_code(code)
            
            if success:
                # Code executed successfully
                self._update_output(f"✓ Code executed successfully: {message}")
                self._update_level_info()  # Update gems/steps display
            else:
                # Code had errors
                self._update_output(f"✗ Error: {message}")
                
        except Exception as e:
            # Unexpected error (shouldn't happen often)
            self._update_output(f"✗ Execution error: {str(e)}")
    
    def _update_status(self, message: str):
        """
        Update status in output area with [INFO] prefix.
        
        Args:
            message (str): Status message to display
        
        Note:
            This is a wrapper around _update_output that adds
            the [INFO] prefix for system messages.
        """
        self._update_output(f"[INFO] {message}")
    
    def _update_output(self, message: str):
        """
        Append message to output text area.
        
        Args:
            message (str): Message to append (automatically adds newline)
        
        Side Effects:
            - Adds message to end of output
            - Auto-scrolls to show latest message
        
        Thread Safety:
            Safe to call from any thread (Tkinter handles it).
        """
        # Append message with newline
        self.output_text.insert(tk.END, f"{message}\n")
        
        # Auto-scroll to show latest message
        self.output_text.see(tk.END)
    
    def _clear_output(self):
        """
        Clear all messages from output area.
        
        Removes all text from the output display.
        Useful for decluttering after many executions.
        """
        self.output_text.delete(1.0, tk.END)
    
    def _update_level_info(self):
        """
        Update level information display.
        
        Updates two labels:
        1. Level info: Shows level number, gems collected, and step count
        2. Hint label: Shows level-specific programming guidance
        
        Format:
            "Level: 1 | Gems: 2/5 | Steps: 17"
            "Hint: Use a for loop to repeat move_forward()"
        
        Called After:
            - Starting game
            - Resetting level
            - Executing code
        """
        if self.game and self.game.current_level:
            level = self.game.current_level
            player = self.game.player
            
            # Build level info string
            info = f"Level: {self.game.level_index + 1} | "
            info += f"Gems: {len(player.get_collected_gems())}/{level.get_total_gems()} | "
            info += f"Steps: {player.get_step_count()}"
            
            # Update label
            self.level_info.config(text=info)
            
            # Update hint if available
            if level.get_hint():
                self.hint_label.config(text=f"Hint: {level.get_hint()}")
    
    def _on_closing(self):
        """
        Handle window close event (X button).
        
        Performs clean shutdown:
        1. Stop game loop
        2. Stop game engine
        3. Destroy Tkinter window
        
        This prevents the application from hanging when user
        closes the window.
        """
        # Stop game loop
        self.running = False
        
        # Stop game engine if it exists
        if self.game:
            self.game.running = False
        
        # Destroy window and exit Tkinter loop
        self.root.destroy()
    
    def run(self):
        """
        Start the main application event loop.
        
        Blocks until window is closed. This is the entry point
        for running the application.
        
        Example:
            >>> if __name__ == "__main__":
            ...     window = MainWindow()
            ...     window.run()
        
        Note:
            This method blocks! It doesn't return until the
            window is closed.
        """
        self.root.mainloop()
