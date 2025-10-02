"""
Code editor interface using Tkinter.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from typing import Callable, Optional

class CodeEditor:
    """Code editor widget for writing Python code."""
    
    def __init__(self, parent, on_code_execute: Callable[[str], None]):
        """Initialize code editor."""
        self.parent = parent
        self.on_code_execute = on_code_execute
        
        # Create main frame
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create toolbar
        self._create_toolbar()
        
        # Create text editor
        self._create_text_editor()
        
        # Create status bar
        self._create_status_bar()
        
        # Bind events
        self._bind_events()
    
    def _create_toolbar(self):
        """Create toolbar with buttons."""
        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Run button
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
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Help button
        self.help_button = ttk.Button(toolbar, text="Help", command=self._show_help)
        self.help_button.pack(side=tk.RIGHT, padx=5)
    
    def _create_text_editor(self):
        """Create the main text editor."""
        # Create frame for text editor
        editor_frame = ttk.Frame(self.frame)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create text widget with syntax highlighting
        self.text_editor = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD,
            font=('Consolas', 12),
            bg='#f8f8f8',
            fg='#333333',
            insertbackground='#333333',
            selectbackground='#0078d4',
            selectforeground='white'
        )
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Add some default code
        self._insert_default_code()
    
    def _create_status_bar(self):
        """Create status bar."""
        self.status_bar = ttk.Frame(self.frame)
        self.status_bar.pack(fill=tk.X, padx=5, pady=2)
        
        self.status_label = ttk.Label(self.status_bar, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        # Line/column info
        self.position_label = ttk.Label(self.status_bar, text="Line 1, Column 1")
        self.position_label.pack(side=tk.RIGHT)
    
    def _bind_events(self):
        """Bind keyboard and mouse events."""
        # Keyboard shortcuts
        self.text_editor.bind('<Control-r>', lambda e: self._run_code())
        self.text_editor.bind('<Control-s>', lambda e: self._save_code())
        self.text_editor.bind('<Control-o>', lambda e: self._load_code())
        
        # Cursor position tracking
        self.text_editor.bind('<KeyRelease>', self._update_position)
        self.text_editor.bind('<Button-1>', self._update_position)
        
        # Text change tracking
        self.text_editor.bind('<KeyPress>', self._on_text_change)
    
    def _insert_default_code(self):
        """Insert default code template."""
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
        """Execute the code in the editor."""
        code = self.text_editor.get(1.0, tk.END).strip()
        
        if not code:
            self._update_status("No code to execute")
            return
        
        # Disable run button during execution
        self.run_button.config(state='disabled')
        self._update_status("Executing code...")
        
        # Execute code in separate thread to prevent UI freezing
        def execute():
            try:
                self.on_code_execute(code)
            except Exception as e:
                self.parent.after(0, lambda: self._update_status(f"Error: {str(e)}"))
            finally:
                self.parent.after(0, lambda: self.run_button.config(state='normal'))
        
        thread = threading.Thread(target=execute)
        thread.daemon = True
        thread.start()
    
    def _clear_code(self):
        """Clear the text editor."""
        if messagebox.askyesno("Clear Code", "Are you sure you want to clear all code?"):
            self.text_editor.delete(1.0, tk.END)
            self._update_status("Code cleared")
    
    def _save_code(self):
        """Save code to file."""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.text_editor.get(1.0, tk.END))
                self._update_status(f"Code saved to {filename}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file: {str(e)}")
    
    def _load_code(self):
        """Load code from file."""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    code = f.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(1.0, code)
                self._update_status(f"Code loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Load Error", f"Could not load file: {str(e)}")
    
    def _show_help(self):
        """Show help dialog."""
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
        
        help_window = tk.Toplevel(self.parent)
        help_window.title("Help")
        help_window.geometry("500x400")
        
        help_text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        help_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        help_text_widget.insert(1.0, help_text)
        help_text_widget.config(state=tk.DISABLED)
    
    def _update_status(self, message: str):
        """Update status bar message."""
        self.status_label.config(text=message)
    
    def _update_position(self, event=None):
        """Update cursor position in status bar."""
        cursor_pos = self.text_editor.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        self.position_label.config(text=f"Line {line}, Column {int(col)+1}")
    
    def _on_text_change(self, event=None):
        """Handle text changes."""
        # Could add syntax highlighting here
        pass
    
    def get_code(self) -> str:
        """Get current code content."""
        return self.text_editor.get(1.0, tk.END).strip()
    
    def set_code(self, code: str):
        """Set code content."""
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(1.0, code)
    
    def insert_code(self, code: str, position: str = tk.END):
        """Insert code at specified position."""
        self.text_editor.insert(position, code)
