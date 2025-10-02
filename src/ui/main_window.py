"""
Main application window combining game view and code editor.
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
    """Main application window with split-screen layout."""
    
    def __init__(self):
        """Initialize main window."""
        self.config = Config()
        self.game: Optional[Game] = None
        self.game_thread: Optional[threading.Thread] = None
        self.running = False
        
        # Create main window
        self.root = tk.Tk()
        self.root.title(self.config.WINDOW_TITLE)
        self.root.geometry(f"{self.config.WINDOW_WIDTH}x{self.config.WINDOW_HEIGHT}")
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Create UI
        self._create_ui()
        
        # Initialize game
        self._initialize_game()
    
    def _create_ui(self):
        """Create the main UI layout."""
        # Create main paned window for split screen
        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Game view
        self._create_game_frame()
        
        # Right side - Code editor
        self._create_editor_frame()
        
        # Configure paned window
        self.paned_window.add(self.game_frame, weight=1)
        self.paned_window.add(self.editor_frame, weight=1)
    
    def _create_game_frame(self):
        """Create the game view frame."""
        self.game_frame = ttk.Frame(self.paned_window)
        
        # Game title
        title_label = ttk.Label(self.game_frame, text="Python Learning Game", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Game canvas (placeholder for now)
        self.game_canvas = tk.Canvas(self.game_frame, bg='lightgray', 
                                    width=400, height=400)
        self.game_canvas.pack(padx=10, pady=10)
        
        # Game controls
        controls_frame = ttk.Frame(self.game_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_button = ttk.Button(controls_frame, text="Start Game", 
                                      command=self._start_game)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = ttk.Button(controls_frame, text="Pause", 
                                     command=self._pause_game, state='disabled')
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = ttk.Button(controls_frame, text="Reset", 
                                     command=self._reset_game, state='disabled')
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Level info
        self.level_info = ttk.Label(self.game_frame, text="Level: 1 | Gems: 0/0 | Steps: 0")
        self.level_info.pack(pady=5)
        
        # Hint display
        self.hint_label = ttk.Label(self.game_frame, text="Hint: Click 'Start Game' to begin!", 
                                   wraplength=350, justify=tk.CENTER)
        self.hint_label.pack(pady=5)
    
    def _create_editor_frame(self):
        """Create the code editor frame."""
        self.editor_frame = ttk.Frame(self.paned_window)
        
        # Editor title
        editor_title = ttk.Label(self.editor_frame, text="Code Editor", 
                                font=('Arial', 14, 'bold'))
        editor_title.pack(pady=5)
        
        # Create code editor
        self.code_editor = CodeEditor(self.editor_frame, self._execute_code)
        
        # Output area
        output_frame = ttk.LabelFrame(self.editor_frame, text="Output")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = tk.Text(output_frame, height=8, font=('Consolas', 10))
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Clear output button
        clear_output_btn = ttk.Button(output_frame, text="Clear Output", 
                                     command=self._clear_output)
        clear_output_btn.pack(pady=5)
    
    def _initialize_game(self):
        """Initialize the game engine."""
        try:
            # This will be implemented when we integrate pygame with tkinter
            self._update_status("Game initialized")
        except Exception as e:
            self._update_status(f"Game initialization failed: {e}")
    
    def _start_game(self):
        """Start the game."""
        try:
            if not self.game:
                # Initialize game
                self.game = Game(self.config)
                self.game.start_new_game()
            
            self.running = True
            self.start_button.config(state='disabled')
            self.pause_button.config(state='normal')
            self.reset_button.config(state='normal')
            
            self._update_status("Game started")
            self._update_level_info()
            
        except Exception as e:
            self._update_status(f"Failed to start game: {e}")
    
    def _pause_game(self):
        """Pause/resume the game."""
        if self.game:
            if self.game.state == GameState.PLAYING:
                self.game.state = GameState.PAUSED
                self.pause_button.config(text="Resume")
                self._update_status("Game paused")
            else:
                self.game.state = GameState.PLAYING
                self.pause_button.config(text="Pause")
                self._update_status("Game resumed")
    
    def _reset_game(self):
        """Reset the current level."""
        if self.game:
            self.game.load_level(self.game.level_index)
            self._update_status("Level reset")
            self._update_level_info()
    
    def _execute_code(self, code: str):
        """Execute user code."""
        if not self.game or not self.running:
            self._update_output("Game not running. Please start the game first.")
            return
        
        try:
            success, message = self.game.execute_code(code)
            
            if success:
                self._update_output(f"✓ Code executed successfully: {message}")
                self._update_level_info()
            else:
                self._update_output(f"✗ Error: {message}")
                
        except Exception as e:
            self._update_output(f"✗ Execution error: {str(e)}")
    
    def _update_status(self, message: str):
        """Update status in the output area."""
        self._update_output(f"[INFO] {message}")
    
    def _update_output(self, message: str):
        """Update output text area."""
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
    
    def _clear_output(self):
        """Clear output text area."""
        self.output_text.delete(1.0, tk.END)
    
    def _update_level_info(self):
        """Update level information display."""
        if self.game and self.game.current_level:
            level = self.game.current_level
            player = self.game.player
            
            info = f"Level: {self.game.level_index + 1} | "
            info += f"Gems: {len(player.get_collected_gems())}/{level.get_total_gems()} | "
            info += f"Steps: {player.get_step_count()}"
            
            self.level_info.config(text=info)
            
            # Update hint
            if level.get_hint():
                self.hint_label.config(text=f"Hint: {level.get_hint()}")
    
    def _on_closing(self):
        """Handle window closing."""
        self.running = False
        if self.game:
            self.game.running = False
        self.root.destroy()
    
    def run(self):
        """Start the main application loop."""
        self.root.mainloop()
