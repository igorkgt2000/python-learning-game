#!/usr/bin/env python3
"""
Demo script for the Python Learning Game.
Shows the game features and capabilities.
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def demo_core_features():
    """Demonstrate core game features."""
    print("🎮 Python Learning Game - Core Features Demo")
    print("=" * 50)
    
    from core.config import Config
    from core.grid import Grid, TileType
    from core.player import Player
    from core.level import Level
    from core.code_executor import CodeExecutor
    
    # Initialize game components
    config = Config()
    grid = Grid(5, 5)
    player = Player(0, 0, "north")
    executor = CodeExecutor(config)
    
    print(f"✓ Game initialized with {config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT} window")
    print(f"✓ Grid size: {config.GRID_SIZE}x{config.GRID_SIZE}")
    print(f"✓ Player starts at position {player.get_position()} facing {player.get_direction().value}")
    
    # Demo level creation
    level = Level(
        start_pos=(0, 0),
        goal_pos=(4, 4),
        obstacles=[(2, 2), (2, 3)],
        gems=[(1, 1), (3, 3)],
        grid_size=5,
        hint="Navigate around obstacles and collect gems!"
    )
    
    print(f"✓ Level created: {level.name}")
    print(f"  - Start: {level.start_pos}")
    print(f"  - Goal: {level.goal_pos}")
    print(f"  - Obstacles: {len(level.obstacles)}")
    print(f"  - Gems: {len(level.gems)}")
    print(f"  - Hint: {level.get_hint()}")
    
    # Demo player movement
    print("\n🤖 Player Movement Demo:")
    print(f"  Initial position: {player.get_position()}")
    
    player.move_forward()
    print(f"  After move_forward(): {player.get_position()}")
    
    player.turn_right()
    print(f"  After turn_right(): facing {player.get_direction().value}")
    
    player.move_forward()
    print(f"  After another move_forward(): {player.get_position()}")
    
    # Demo code execution
    print("\n💻 Code Execution Demo:")
    
    # Valid code
    valid_code = """
# Simple movement sequence
move_forward()
turn_right()
move_forward()
"""
    
    print("  Testing valid code:")
    print("  " + valid_code.strip().replace('\n', '\n  '))
    
    result = executor.execute_code(valid_code, player, grid)
    if result["success"]:
        print("  ✓ Code executed successfully!")
        print(f"  Actions performed: {result['actions']}")
    else:
        print(f"  ✗ Code execution failed: {result['error']}")
    
    # Invalid code
    invalid_code = "import os\nos.system('rm -rf /')"
    print("\n  Testing invalid code (security test):")
    print("  " + invalid_code)
    
    if executor.validate_code(invalid_code):
        print("  ✗ Security check failed!")
    else:
        print("  ✓ Security check passed - dangerous code blocked!")

def demo_level_system():
    """Demonstrate the level system."""
    print("\n📚 Level System Demo:")
    print("=" * 30)
    
    from levels.level_loader import LevelLoader
    
    # Create level loader
    levels_dir = Path(__file__).parent / "src" / "levels"
    loader = LevelLoader(levels_dir)
    
    print(f"✓ Loaded {loader.get_level_count()} levels")
    
    # Show first few levels
    for i in range(min(3, loader.get_level_count())):
        level = loader.get_level(i)
        if level:
            print(f"  Level {i+1}: {level.name}")
            print(f"    Hint: {level.get_hint()}")

def demo_ui_features():
    """Demonstrate UI features."""
    print("\n🖥️  UI Features Demo:")
    print("=" * 25)
    
    print("✓ Split-screen interface:")
    print("  - Left: Game view with grid and player")
    print("  - Right: Code editor with syntax highlighting")
    print("✓ Code editor features:")
    print("  - Syntax highlighting")
    print("  - Run/Clear/Save/Load buttons")
    print("  - Keyboard shortcuts (Ctrl+R, Ctrl+S, etc.)")
    print("  - Help system with function reference")
    print("✓ Game controls:")
    print("  - Start/Pause/Reset buttons")
    print("  - Real-time level info display")
    print("  - Hint system")
    print("✓ Output console:")
    print("  - Code execution results")
    print("  - Error messages")
    print("  - Status updates")

def demo_educational_features():
    """Demonstrate educational features."""
    print("\n🎓 Educational Features Demo:")
    print("=" * 35)
    
    print("✓ Progressive Learning Path:")
    print("  - 60+ levels from beginner to expert")
    print("  - Sequential command learning")
    print("  - Loop introduction (for/while)")
    print("  - Conditional logic (if/else)")
    print("  - Function definition")
    print("  - Data structures (lists, dicts)")
    print("  - Advanced algorithms")
    
    print("✓ Safe Code Execution:")
    print("  - AST-based code validation")
    print("  - Whitelisted functions only")
    print("  - No file system access")
    print("  - No network access")
    print("  - No dangerous imports")
    
    print("✓ Learning Tools:")
    print("  - Interactive hints")
    print("  - Step-by-step tutorials")
    print("  - Code examples")
    print("  - Achievement system")
    print("  - Progress tracking")

def main():
    """Run the complete demo."""
    print("🚀 Python Learning Game - Complete Demo")
    print("=" * 50)
    print("A comprehensive Python learning game with progressive levels")
    print("from beginner to expert, featuring safe code execution")
    print("and interactive gameplay.")
    print()
    
    try:
        demo_core_features()
        demo_level_system()
        demo_ui_features()
        demo_educational_features()
        
        print("\n🎉 Demo completed successfully!")
        print("\nTo run the actual game:")
        print("  python main.py")
        print("\nTo run tests:")
        print("  python test_game.py")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
