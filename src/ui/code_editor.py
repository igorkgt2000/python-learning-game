"""
Code editor interface using Tkinter for writing Python robot control code.

This module provides a full-featured code editor with:
- Syntax-highlighted text area (via Tkinter ScrolledText)
- Toolbar with Run, Clear, Save, Load, and Help buttons
- Status bar showing cursor position and messages
- Keyboard shortcuts (Ctrl+R to run, Ctrl+S to save, etc.)
- Threaded code execution to prevent UI freezing
- File save/load functionality
- Built-in help documentation

The editor is designed for beginners learning Python programming
through controlling a robot character in a grid-based world.

Classes:
    CodeEditor: Main code editor widget

Dependencies:
    - tkinter: GUI framework
    - threading: Non-blocking code execution
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from typing import Callable, Optional

class CodeEditor:
    """
    Full-featured code editor widget for writing Python code.
    
    Provides an IDE-like experience with:
    - Multi-line text editing with monospace font
    - Toolbar buttons (Run, Clear, Save, Load, Help)
    - Status bar (messages and cursor position)
    - Keyboard shortcuts for common actions
    - Default code template with instructions
    - File I/O capabilities
    - Non-blocking code execution
    
    The editor executes code by calling a callback function
    (on_code_execute) which connects to the game engine.
    
    Attributes:
        parent: Parent Tkinter widget
        on_code_execute (Callable): Function to call when running code
        frame (ttk.Frame): Main container frame
        text_editor (ScrolledText): Main text editing widget
        run_button (ttk.Button): Execute code button
        status_label (ttk.Label): Status message display
        position_label (ttk.Label): Cursor position display
    
    Example:
        >>> def execute_handler(code: str):
        ...     print(f"Running: {code}")
        >>> editor = CodeEditor(parent_frame, execute_handler)
        >>> code = editor.get_code()
    """
    
    def __init__(self, parent, on_code_execute: Callable[[str], None]):
        """
        Initialize the code editor.
        
        Creates the complete UI including toolbar, text editor,
        and status bar. Inserts default template code and binds
        keyboard shortcuts.
        
        Args:
            parent: Parent Tkinter widget to contain the editor
            on_code_execute (Callable[[str], None]): Callback function
                that receives code string when user clicks Run.
        
        Side Effects:
            - Creates UI widgets in parent
            - Binds keyboard shortcuts
            - Inserts default code template
        
        Example:
            >>> editor = CodeEditor(main_window, game.execute_code)
        """
        self.parent = parent
        self.on_code_execute = on_code_execute  # Callback for running code
        
        # Create main container frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Build UI components
        self._create_toolbar()     # Top: buttons
        self._create_text_editor()  # Middle: code editing area
        self._create_status_bar()   # Bottom: status messages
        
        # Set up keyboard shortcuts
        self._bind_events()
    
    def _create_toolbar(self):
        """
        Create toolbar with action buttons.
        
        Creates a horizontal toolbar with buttons for:
        - Run Code: Execute current code
        - Clear: Delete all code (with confirmation)
        - Save: Save code to .py file
        - Load: Load code from .py file
        - Help: Show available functions and shortcuts
        
        Layout: [Run][Clear][Save][Load] | [Help on right]
        """
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Run button (most important, leftmost)
        self.run_button = ttk.Button(toolbar, text="Run Code", command=self._run_code)
        self.run_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        self.clear_button = ttk.Button(toolbar, text="Clear", command=self._clear_code)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Save button
        self.save_button = ttk.Button(toolbar, text="Save", command=self._save_code)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Load button
        self.load_button = ttk.Button(toolbar, text="Load", command=self._load_code)
        self.load_button.pack(side=tk.LEFT, padx=5)
        
        # Visual separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Help button (rightmost)
        self.help_button = ttk.Button(toolbar, text="Help", command=self._show_help)
        self.help_button.pack(side=tk.RIGHT, padx=5)
    
    def _create_text_editor(self):
        """
        Create the main text editing area.
        
        Creates a scrollable, multi-line text widget with:
        - Monospace font (Consolas 12pt) for code readability
        - Light gray background for reduced eye strain
        - Word wrapping enabled
        - Vertical scrollbar (via ScrolledText)
        - Nice selection colors (VS Code style)
        
        Inserts default template code to help users get started.
        """
        # Container frame for editor
        editor_frame = ttk.Frame(self.frame)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Multi-line text widget with scrollbar
        self.text_editor = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD,                # Wrap at word boundaries
            font=('Consolas', 12),       # Monospace font for code
            bg='#f8f8f8',                # Light gray background
            fg='#333333',                # Dark gray text
            insertbackground='#333333',  # Cursor color
            selectbackground='#0078d4',  # Selection background (blue)
            selectforeground='white'     # Selection text (white)
        )
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Insert helpful default code
        self._insert_default_code()
    
    def _create_status_bar(self):
        """
        Create status bar at bottom of editor.
        
        Shows two pieces of information:
        - Left side: Status messages ("Ready", "Executing", errors)
        - Right side: Cursor position (Line X, Column Y)
        
        The status bar helps users understand what the editor is doing
        and where their cursor is in the code.
        """
        self.status_bar = ttk.Frame(self.frame)
        self.status_bar.pack(fill=tk.X, padx=5, pady=2)
        
        # Status message label (left side)
        self.status_label = ttk.Label(self.status_bar, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        # Cursor position label (right side)
        self.position_label = ttk.Label(self.status_bar, text="Line 1, Column 1")
        self.position_label.pack(side=tk.RIGHT)
    
    def _bind_events(self):
        """
        Bind keyboard shortcuts and event handlers.
        
        Keyboard Shortcuts:
        - Ctrl+R: Run code
        - Ctrl+S: Save code
        - Ctrl+O: Load code
        
        Event Handlers:
        - KeyRelease, Button-1 (click): Update cursor position
        - KeyPress: Handle text changes (for future syntax highlighting)
        
        Note:
            Lambda functions are used to prevent immediate execution
            and to handle the event parameter that Tkinter passes.
        """
        # Keyboard shortcuts (Ctrl+key)
        self.text_editor.bind('<Control-r>', lambda e: self._run_code())
        self.text_editor.bind('<Control-s>', lambda e: self._save_code())
        self.text_editor.bind('<Control-o>', lambda e: self._load_code())
        
        # Cursor position tracking (update on key release and mouse click)
        self.text_editor.bind('<KeyRelease>', self._update_position)
        self.text_editor.bind('<Button-1>', self._update_position)
        
        # Text change tracking (for future syntax highlighting)
        self.text_editor.bind('<KeyPress>', self._on_text_change)
    
    def _insert_default_code(self):
        """
        Insert helpful default code template.
        
        Provides a welcoming message and complete documentation
        of all available robot control functions. This helps
        beginners get started without reading external documentation.
        
        Template includes:
        - Welcome message
        - Movement functions (move_forward, turn_left, etc.)
        - Sensing functions (is_clear, is_gem, etc.)
        - Simple example code
        """
        default_code = """# Welcome to Python Learning Game!
# Write your code here to control the robot

# Available functions:
# move_forward() - move one step forward
# turn_left() - turn left 90 degrees
# turn_right() - turn right 90 degrees
# turn_around() - turn 180 degrees

# Sensing functions:
# is_clear() - check if path ahead is clear
# is_gem() - check if current position has a gem
# is_goal() - check if current position is the goal

# Example:
move_forward()
move_forward()
turn_right()
move_forward()
"""
        self.text_editor.insert(tk.END, default_code)
    
    def _run_code(self):
        """
        Execute code in a background thread.
        
        Process:
        1. Get code from text editor
        2. Validate code is not empty
        3. Disable Run button to prevent multiple executions
        4. Execute code in background thread (prevents UI freeze)
        5. Re-enable Run button when complete
        
        Threading:
            Using daemon thread means thread will exit when main program
            exits, preventing hung threads from keeping app alive.
        
        Error Handling:
            Exceptions are caught and displayed in status bar.
            The finally block ensures Run button is always re-enabled.
        """
        # Get all text from editor
        code = self.text_editor.get(1.0, tk.END).strip()
        
        # Validate there's code to execute
        if not code:
            self._update_status("No code to execute")
            return
        
        # Prevent multiple simultaneous executions
        self.run_button.config(state='disabled')
        self._update_status("Executing code...")
        
        # Execute in background thread to keep UI responsive
        def execute():
            try:
                # Call the game's code execution callback
                self.on_code_execute(code)
            except Exception as e:
                # Schedule UI update on main thread
                self.parent.after(0, lambda: self._update_status(f"Error: {str(e)}"))
            finally:
                # Always re-enable button, even on error
                self.parent.after(0, lambda: self.run_button.config(state='normal'))
        
        # Create and start daemon thread
        thread = threading.Thread(target=execute)
        thread.daemon = True  # Exit when main program exits
        thread.start()
    
    def _clear_code(self):
        """
        Clear all code from editor (with confirmation).
        
        Shows a confirmation dialog to prevent accidental data loss.
        Only clears code if user clicks "Yes".
        """
        # Ask for confirmation
        if messagebox.askyesno("Clear Code", "Are you sure you want to clear all code?"):
            # Delete all text
            self.text_editor.delete(1.0, tk.END)
            self._update_status("Code cleared")
    
    def _save_code(self):
        """
        Save current code to a .py file.
        
        Opens a file save dialog allowing user to choose filename
        and location. Defaults to .py extension for Python files.
        
        Side Effects:
            - Opens file dialog
            - Writes to filesystem
            - Updates status bar
            - Shows error dialog on failure
        """
        from tkinter import filedialog
        
        # Open save dialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".py",  # Default extension
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        
        # User may cancel dialog
        if filename:
            try:
                # Write code to file
                with open(filename, 'w') as f:
                    f.write(self.text_editor.get(1.0, tk.END))
                self._update_status(f"Code saved to {filename}")
            except Exception as e:
                # Show error dialog
                messagebox.showerror("Save Error", f"Could not save file: {str(e)}")
    
    def _load_code(self):
        """
        Load code from a .py file.
        
        Opens a file open dialog. Replaces current editor content
        with the loaded file. Previous content is lost (no undo).
        
        Side Effects:
            - Opens file dialog
            - Reads from filesystem
            - Replaces editor content
            - Updates status bar
            - Shows error dialog on failure
        """
        from tkinter import filedialog
        
        # Open file dialog
        filename = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        
        # User may cancel dialog
        if filename:
            try:
                # Read file content
                with open(filename, 'r') as f:
                    code = f.read()
                
                # Replace editor content
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, code)
                
                self._update_status(f"Code loaded from {filename}")
            except Exception as e:
                # Show error dialog
                messagebox.showerror("Load Error", f"Could not load file: {str(e)}")
    
    def _show_help(self):
        """
        Show help documentation in a popup window.
        
        Creates a new top-level window displaying:
        - All available robot functions
        - Function descriptions
        - Keyboard shortcuts
        - Programming tips
        
        The help text is read-only (disabled state) to prevent editing.
        """
        # Help documentation text
        help_text = """
Python Learning Game - Help

Available Functions:
• move_forward() - Move one step forward
• turn_left() - Turn left 90 degrees  
• turn_right() - Turn right 90 degrees
• turn_around() - Turn 180 degrees

Sensing Functions:
• is_clear() - Check if path ahead is clear
• is_gem() - Check if current position has a gem
• is_goal() - Check if current position is the goal
• get_position() - Get current (x, y) position
• get_direction() - Get current direction
• get_gem_count() - Get number of gems remaining

Keyboard Shortcuts:
• Ctrl+R - Run code
• Ctrl+S - Save code
• Ctrl+O - Load code

Tips:
• Use loops (for, while) to repeat actions
• Use if/else for decision making
• Define functions to organize your code
• Check the hint for level-specific guidance
        """
        
        # Create popup window
        help_window = tk.Toplevel(self.parent)
        help_window.title("Help")
        help_window.geometry("500x400")
        
        # Create scrollable text widget for help
        help_text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.config(state=tk.DISABLED)  # Read-only
    
    def _update_status(self, message: str):
        """
        Update status bar message.
        
        Args:
            message (str): Status message to display
        """
        self.status_label.config(text=message)
    
    def _update_position(self, event=None):
        """
        Update cursor position display in status bar.
        
        Calculates current line and column from cursor position.
        Column is 1-indexed for user-friendliness (most editors
        use 1-indexed columns, not 0-indexed).
        
        Args:
            event: Tkinter event (unused but required by binding)
        """
        # Get cursor position (format: "line.column")
        cursor_pos = self.text_editor.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        
        # Update label (add 1 to column for 1-indexed display)
        self.position_label.config(text=f"Line {line}, Column {int(col)+1}")
    
    def _on_text_change(self, event=None):
        """
        Handle text change events.
        
        Placeholder for future features like:
        - Real-time syntax highlighting
        - Auto-indentation
        - Bracket matching
        - Code suggestions
        
        Args:
            event: Tkinter event (unused)
        """
        # TODO: Add syntax highlighting
        # Could use Pygments or custom regex-based highlighting
        pass
    
    def get_code(self) -> str:
        """
        Get current code from editor.
        
        Returns:
            str: All code in editor, stripped of trailing whitespace
        
        Example:
            >>> code = editor.get_code()
            >>> print(code)
            move_forward()
            turn_left()
        """
        return self.text_editor.get(1.0, tk.END).strip()
    
    def set_code(self, code: str):
        """
        Replace all code in editor.
        
        Args:
            code (str): New code content
        
        Warning:
            Replaces all existing content. Previous code is lost.
        
        Example:
            >>> editor.set_code("move_forward()\nturn_right()")
        """
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(1.0, code)
    
    def insert_code(self, code: str, position: str = tk.END):
        """
        Insert code at specified position.
        
        Args:
            code (str): Code to insert
            position (str): Tkinter text index (default: tk.END = end of file)
        
        Example:
            >>> editor.insert_code("move_forward()\n")  # Append
            >>> editor.insert_code("# Header\n", "1.0")  # Prepend
        """
        self.text_editor.insert(position, code)
