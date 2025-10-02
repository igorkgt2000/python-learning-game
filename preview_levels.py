#!/usr/bin/env python3
"""
Level Preview Tool - Visualize all levels before playing

Shows ASCII art representation of each level:
- P = Player start
- G = Goal
- # = Wall/Obstacle
- * = Gem
- . = Empty floor

Usage:
    python preview_levels.py           # Show all levels
    python preview_levels.py 6         # Show only level 6
    python preview_levels.py 6-10      # Show levels 6 through 10
"""

import json
import sys
from pathlib import Path

def load_level(level_num):
    """Load a level JSON file."""
    level_path = Path(f"src/levels/level_{level_num:02d}.json")
    if not level_path.exists():
        return None
    
    with open(level_path, 'r') as f:
        return json.load(f)

def visualize_level(level_data, level_num):
    """Create ASCII visualization of a level."""
    if not level_data:
        return f"❌ Level {level_num} not found"
    
    grid_size = level_data['grid_size']
    start = tuple(level_data['start_pos'])
    goal = tuple(level_data['goal_pos'])
    obstacles = [tuple(obs) for obs in level_data.get('obstacles', [])]
    gems = [tuple(gem) for gem in level_data.get('gems', [])]
    
    # Build grid
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Place elements
    for x, y in obstacles:
        if 0 <= x < grid_size and 0 <= y < grid_size:
            grid[y][x] = '#'
    
    for x, y in gems:
        if 0 <= x < grid_size and 0 <= y < grid_size:
            grid[y][x] = '*'
    
    # Place goal (may overwrite gem)
    grid[goal[1]][goal[0]] = 'G'
    
    # Place player start (may overwrite goal if same position)
    if start == goal:
        grid[start[1]][start[0]] = 'S'  # Start and goal same
    else:
        grid[start[1]][start[0]] = 'P'
    
    # Create output
    output = []
    output.append("=" * 60)
    output.append(f"📚 {level_data['name']}")
    output.append("=" * 60)
    output.append("")
    
    # Grid with borders
    output.append("  +" + "-" * (grid_size * 2 - 1) + "+")
    for row in grid:
        output.append("  |" + " ".join(row) + "|")
    output.append("  +" + "-" * (grid_size * 2 - 1) + "+")
    output.append("")
    
    # Legend
    output.append("Legend:")
    output.append("  P = Player Start")
    output.append("  G = Goal")
    output.append("  # = Wall/Obstacle")
    output.append("  * = Gem")
    output.append("  . = Empty floor")
    if start == goal:
        output.append("  S = Start & Goal (same position)")
    output.append("")
    
    # Stats
    output.append("📊 Level Stats:")
    output.append(f"  Grid Size: {grid_size}x{grid_size}")
    output.append(f"  Obstacles: {len(obstacles)}")
    output.append(f"  Gems: {len(gems)}")
    output.append(f"  Distance: {abs(goal[0]-start[0]) + abs(goal[1]-start[1])} tiles (Manhattan)")
    output.append("")
    
    # Hint
    output.append("💡 Hint:")
    output.append(f"  {level_data.get('hint', 'No hint available')}")
    output.append("")
    
    return "\n".join(output)

def preview_range(start, end):
    """Preview a range of levels."""
    output = []
    output.append("\n" + "=" * 60)
    output.append("🎮 PYTHON LEARNING GAME - LEVEL PREVIEW")
    output.append("=" * 60)
    output.append("")
    
    for level_num in range(start, end + 1):
        level_data = load_level(level_num)
        if level_data:
            output.append(visualize_level(level_data, level_num))
        else:
            output.append(f"⏭️  Level {level_num} not found (skipping)\n")
    
    # Summary
    total_found = sum(1 for i in range(start, end + 1) if load_level(i) is not None)
    output.append("=" * 60)
    output.append(f"✅ Previewed {total_found} levels ({start}-{end})")
    output.append("=" * 60)
    
    return "\n".join(output)

def main():
    """Main entry point."""
    if len(sys.argv) == 1:
        # Show all levels
        print(preview_range(1, 30))
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if '-' in arg:
            # Range (e.g., "6-10")
            start, end = map(int, arg.split('-'))
            print(preview_range(start, end))
        else:
            # Single level
            level_num = int(arg)
            level_data = load_level(level_num)
            print(visualize_level(level_data, level_num))
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()

