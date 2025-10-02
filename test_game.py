#!/usr/bin/env python3
"""
Test script for the Python Learning Game.
"""

import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from core.config import Config
        from core.grid import Grid, TileType
        from core.player import Player
        from core.level import Level
        from core.code_executor import CodeExecutor
        print("✓ All core modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic game functionality."""
    try:
        from core.config import Config
        from core.grid import Grid, TileType
        from core.player import Player
        from core.level import Level
        
        # Test configuration
        config = Config()
        print(f"✓ Config created: {config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        
        # Test grid
        grid = Grid(5, 5)
        grid.set_tile(2, 2, TileType.WALL)
        assert grid.is_wall(2, 2)
        print("✓ Grid system working")
        
        # Test player
        player = Player(0, 0, "north")
        player.move_forward()
        assert player.get_position() == (0, -1)
        print("✓ Player movement working")
        
        # Test level
        level = Level(
            start_pos=(0, 0),
            goal_pos=(4, 4),
            obstacles=[(2, 2)],
            gems=[(1, 1)],
            grid_size=5,
            hint="Test level"
        )
        assert level.get_total_gems() == 1
        print("✓ Level system working")
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

def test_code_execution():
    """Test code execution system."""
    try:
        from core.config import Config
        from core.code_executor import CodeExecutor
        from core.player import Player
        from core.grid import Grid
        
        config = Config()
        executor = CodeExecutor(config)
        player = Player(0, 0, "north")
        grid = Grid(5, 5)
        
        # Test valid code
        valid_code = "move_forward()\nturn_right()"
        assert executor.validate_code(valid_code)
        print("✓ Code validation working")
        
        # Test invalid code
        invalid_code = "import os"
        assert not executor.validate_code(invalid_code)
        print("✓ Code security working")
        
        return True
        
    except Exception as e:
        print(f"✗ Code execution test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Python Learning Game...")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_code_execution
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! Game is ready to run.")
        print("Run 'python main.py' to start the game.")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
