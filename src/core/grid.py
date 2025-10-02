"""
Grid System - 2D tile-based world representation.

This module defines the Grid class which represents the game world as a 2D array
of tiles. Each tile can be empty, a wall, a gem, or a goal. The grid handles
collision detection, gem collection, and pathfinding support.

Architecture:
    - Grid is a 2D list indexed as grid[y][x] (row-major order)
    - Special tiles (gems, goals) are tracked in separate lists for efficiency
    - Coordinate system matches screen coordinates (0,0 = top-left)
    - Out-of-bounds positions are treated as walls for safety

Data Structure:
    tiles[y][x] = TileType enum value
    
    Example 3x3 grid:
    tiles[0] = [EMPTY, WALL,  EMPTY]  <- Row 0 (y=0)
    tiles[1] = [GEM,   EMPTY, EMPTY]  <- Row 1 (y=1)
    tiles[2] = [EMPTY, EMPTY, GOAL]   <- Row 2 (y=2)
               ^       ^      ^
               x=0     x=1    x=2

Usage Example:
    >>> grid = Grid(10, 10)
    >>> grid.set_tile(5, 5, TileType.WALL)
    >>> grid.is_wall(5, 5)
    True
    >>> grid.set_tile(3, 3, TileType.GEM)
    >>> grid.collect_gem(3, 3)
    True

Author: Python Learning Game Team
Version: 2.0
Last Modified: October 2, 2025
"""

from typing import List, Tuple, Optional
from enum import Enum

class TileType(Enum):
    """
    Enumeration of all possible tile types in the game world.
    
    Each tile in the grid has exactly one type. The type determines:
    - Visual appearance (which sprite to render)
    - Collision behavior (can player move through it?)
    - Interaction behavior (what happens when player enters?)
    
    Tile Types:
        EMPTY: Walkable empty space, default tile type
        WALL: Solid obstacle, blocks player movement
        GEM: Collectible item, removed when player walks over it
        GOAL: Victory condition, level completes when reached
    
    Note:
        Player position is NOT stored in the grid. The Player object
        maintains its own (x, y) coordinates which reference grid tiles.
    """
    EMPTY = "empty"  # Default walkable tile
    WALL = "wall"    # Impassable obstacle
    GEM = "gem"      # Collectible item
    GOAL = "goal"    # Level objective

class Grid:
    """
    2D tile-based world representation.
    
    The Grid stores the game world as a 2D array of TileType values.
    It handles collision detection, gem collection, and provides
    utilities for pathfinding and level validation.
    
    Attributes:
        width (int): Number of tiles horizontally (X-axis)
        height (int): Number of tiles vertically (Y-axis)
        tiles (List[List[TileType]]): 2D array of tile types [y][x]
        gems (List[Tuple[int, int]]): Positions of all remaining gems
        goals (List[Tuple[int, int]]): Positions of all goal tiles
    
    Coordinate System:
        (0,0) is top-left corner
        X increases rightward (columns)
        Y increases downward (rows)
        Access pattern: tiles[y][x]
    
    Performance:
        - Tile lookup: O(1) - direct array access
        - Gem count: O(1) - tracked in separate list
        - Neighbor lookup: O(1) - maximum 4 neighbors
    
    Example:
        >>> grid = Grid(10, 10)
        >>> grid.set_tile(5, 3, TileType.WALL)
        >>> grid.is_valid_position(5, 3)
        True
        >>> grid.is_wall(5, 3)
        True
    """
    
    def __init__(self, width: int, height: int):
        """
        Initialize a new grid with all tiles set to EMPTY.
        
        Creates a 2D array of tiles initialized to EMPTY type.
        Also initializes tracking lists for gems and goals.
        
        Args:
            width (int): Number of tiles horizontally (must be > 0)
            height (int): Number of tiles vertically (must be > 0)
        
        Raises:
            No explicit validation, but width/height should be positive.
            Typical range: 5-20 tiles per dimension.
        
        Example:
            >>> grid = Grid(10, 10)  # Standard 10x10 grid
            >>> grid.width
            10
            >>> grid.height
            10
        """
        self.width = width    # Number of columns (X-axis)
        self.height = height  # Number of rows (Y-axis)
        
        # Create 2D array: height rows, each with width columns
        # List comprehension: [[EMPTY, EMPTY, ...], [EMPTY, EMPTY, ...], ...]
        # Inner loop creates a row of width tiles
        # Outer loop creates height rows
        self.tiles = [[TileType.EMPTY for _ in range(width)] for _ in range(height)]
        
        # Track special tile positions for fast lookups
        # These lists are kept in sync with the tiles array
        self.gems: List[Tuple[int, int]] = []   # Positions of collectible gems
        self.goals: List[Tuple[int, int]] = []  # Positions of goal tiles
    
    def get_tile(self, x: int, y: int) -> TileType:
        """
        Get the tile type at the specified position.
        
        Returns the TileType enum value for the tile at (x, y).
        Out-of-bounds positions are treated as WALL for safety
        (prevents player from moving off the grid).
        
        Args:
            x (int): X coordinate (column)
            y (int): Y coordinate (row)
        
        Returns:
            TileType: The type of tile at position (x, y),
                     or TileType.WALL if position is out of bounds
        
        Example:
            >>> grid = Grid(10, 10)
            >>> grid.get_tile(5, 5)
            <TileType.EMPTY: 'empty'>
            >>> grid.get_tile(100, 100)  # Out of bounds
            <TileType.WALL: 'wall'>
        """
        # Check if position is within grid boundaries
        if self.is_valid_position(x, y):
            # Access tiles using [row][column] = [y][x] indexing
            return self.tiles[y][x]
        
        # Out of bounds positions are treated as walls
        # This prevents player from moving off the grid edge
        return TileType.WALL
    
    def set_tile(self, x: int, y: int, tile_type: TileType):
        """
        Set the tile type at the specified position.
        
        Updates the tile at (x, y) to the new type. Also updates
        the special tracking lists (gems, goals) to stay in sync.
        
        Important: Setting a tile to EMPTY will remove it from gem/goal lists.
        This is how gem collection works - the tile becomes EMPTY.
        
        Args:
            x (int): X coordinate (column)
            y (int): Y coordinate (row)
            tile_type (TileType): New type for the tile
        
        Side Effects:
            - Updates self.tiles[y][x]
            - Updates self.gems list if adding/removing gem
            - Updates self.goals list if adding/removing goal
        
        Note:
            Does nothing if position is out of bounds (fails silently).
        
        Example:
            >>> grid = Grid(10, 10)
            >>> grid.set_tile(5, 5, TileType.WALL)
            >>> grid.set_tile(3, 3, TileType.GEM)
            >>> grid.get_gem_count()
            1
        """
        # Only modify if position is within grid boundaries
        if self.is_valid_position(x, y):
            # Update the tile type in the 2D array
            self.tiles[y][x] = tile_type
            
            # Keep special tracking lists synchronized with tile array
            # This allows O(1) gem counting and fast iteration over goals
            
            if tile_type == TileType.GEM:
                # Adding a gem - add to tracking list if not already present
                if (x, y) not in self.gems:
                    self.gems.append((x, y))
            elif tile_type == TileType.GOAL:
                # Adding a goal - add to tracking list if not already present
                if (x, y) not in self.goals:
                    self.goals.append((x, y))
            else:
                # Changing to EMPTY or WALL - remove from special lists
                # This happens when gems are collected (GEM → EMPTY)
                if (x, y) in self.gems:
                    self.gems.remove((x, y))  # No longer a gem
                if (x, y) in self.goals:
                    self.goals.remove((x, y))  # No longer a goal
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """
        Check if the given position is within grid boundaries.
        
        Returns True if (x, y) is a valid tile position, False otherwise.
        This is used extensively for collision detection and bounds checking.
        
        Args:
            x (int): X coordinate to check
            y (int): Y coordinate to check
        
        Returns:
            bool: True if position is within bounds, False otherwise
        
        Example:
            >>> grid = Grid(10, 10)
            >>> grid.is_valid_position(5, 5)
            True
            >>> grid.is_valid_position(-1, 5)
            False
            >>> grid.is_valid_position(10, 10)  # 10 is out of range (0-9)
            False
        """
        # Check X and Y are both within valid ranges
        # X must be: 0 <= x < width
        # Y must be: 0 <= y < height
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_wall(self, x: int, y: int) -> bool:
        """
        Check if the tile at (x, y) is a wall.
        
        Used for collision detection - player cannot move through walls.
        Out-of-bounds positions are treated as walls by get_tile().
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
        
        Returns:
            bool: True if tile is a wall, False otherwise
        
        Example:
            >>> grid = Grid(10, 10)
            >>> grid.set_tile(5, 5, TileType.WALL)
            >>> grid.is_wall(5, 5)
            True
        """
        return self.get_tile(x, y) == TileType.WALL
    
    def is_gem(self, x: int, y: int) -> bool:
        """
        Check if there's a gem at position (x, y).
        
        Used by game logic to check if player should collect a gem
        when entering this tile.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
        
        Returns:
            bool: True if tile has a gem, False otherwise
        
        Example:
            >>> grid = Grid(10, 10)
            >>> grid.set_tile(3, 3, TileType.GEM)
            >>> grid.is_gem(3, 3)
            True
        """
        return self.get_tile(x, y) == TileType.GEM
    
    def is_goal(self, x: int, y: int) -> bool:
        """
        Check if the tile at (x, y) is a goal.
        
        Used for victory condition checking - level completes when
        player reaches a goal tile (and all gems are collected).
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
        
        Returns:
            bool: True if tile is a goal, False otherwise
        
        Example:
            >>> grid = Grid(10, 10)
            >>> grid.set_tile(9, 9, TileType.GOAL)
            >>> grid.is_goal(9, 9)
            True
        """
        return self.get_tile(x, y) == TileType.GOAL
    
    def collect_gem(self, x, y: int) -> bool:
        """
        Collect the gem at position (x, y) if one exists.
        
        Removes the gem by changing the tile to EMPTY. This automatically
        updates the gems tracking list via set_tile().
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
        
        Returns:
            bool: True if a gem was collected, False if no gem was there
        
        Side Effects:
            - Changes tile from GEM to EMPTY if gem exists
            - Removes position from self.gems list
        
        Example:
            >>> grid = Grid(10, 10)
            >>> grid.set_tile(3, 3, TileType.GEM)
            >>> grid.collect_gem(3, 3)
            True
            >>> grid.collect_gem(3, 3)  # Already collected
            False
        """
        # Check if there's actually a gem at this position
        if self.is_gem(x, y):
            # Remove gem by changing tile to empty
            # set_tile() handles updating the gems list
            self.set_tile(x, y, TileType.EMPTY)
            return True  # Gem was collected
        return False  # No gem to collect
    
    def get_gem_count(self) -> int:
        """
        Get the number of gems remaining in the grid.
        
        This is O(1) because we track gems in a separate list.
        Used for victory condition checking and UI display.
        
        Returns:
            int: Number of uncollected gems
        
        Example:
            >>> grid = Grid(10, 10)
            >>> grid.set_tile(1, 1, TileType.GEM)
            >>> grid.set_tile(2, 2, TileType.GEM)
            >>> grid.get_gem_count()
            2
            >>> grid.collect_gem(1, 1)
            True
            >>> grid.get_gem_count()
            1
        """
        # gems list is kept in sync with tile array by set_tile()
        return len(self.gems)
    
    def clear(self):
        """
        Reset the entire grid to empty state.
        
        Sets all tiles to EMPTY and clears the tracking lists.
        Used when loading a new level or resetting current level.
        
        Side Effects:
            - All tiles set to TileType.EMPTY
            - gems list cleared
            - goals list cleared
        
        Example:
            >>> grid = Grid(10, 10)
            >>> grid.set_tile(5, 5, TileType.WALL)
            >>> grid.clear()
            >>> grid.get_tile(5, 5)
            <TileType.EMPTY: 'empty'>
        """
        # Recreate tiles array with all EMPTY tiles
        # This is faster than iterating and setting each tile individually
        self.tiles = [[TileType.EMPTY for _ in range(self.width)] for _ in range(self.height)]
        
        # Clear tracking lists
        self.gems.clear()   # Remove all gem positions
        self.goals.clear()  # Remove all goal positions
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get all valid neighboring positions (up, down, left, right).
        
        Returns positions of tiles adjacent to (x, y) in cardinal directions.
        Only includes neighbors that are within grid bounds. Used for
        pathfinding algorithms and maze generation.
        
        Args:
            x (int): X coordinate of center tile
            y (int): Y coordinate of center tile
        
        Returns:
            List[Tuple[int, int]]: List of (x, y) positions of valid neighbors
                                  (0-4 neighbors depending on position)
        
        Note:
            Does NOT include diagonal neighbors. Only cardinal directions:
            north, east, south, west.
        
        Example:
            >>> grid = Grid(10, 10)
            >>> grid.get_neighbors(5, 5)  # Middle of grid
            [(5, 6), (6, 5), (5, 4), (4, 5)]  # 4 neighbors
            >>> grid.get_neighbors(0, 0)  # Corner
            [(0, 1), (1, 0)]  # Only 2 neighbors
        """
        neighbors = []
        
        # Check all four cardinal directions
        # Format: (dx, dy) offset from current position
        directions = [
            (0, 1),   # South (down): same X, Y+1
            (1, 0),   # East (right): X+1, same Y
            (0, -1),  # North (up): same X, Y-1
            (-1, 0)   # West (left): X-1, same Y
        ]
        
        for dx, dy in directions:
            # Calculate neighbor position
            nx, ny = x + dx, y + dy
            
            # Only include if within grid bounds
            if self.is_valid_position(nx, ny):
                neighbors.append((nx, ny))
        
        return neighbors
