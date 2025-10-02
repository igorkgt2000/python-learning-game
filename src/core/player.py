"""
Player Character System - Core game character with movement and sensing capabilities.

This module defines the Player class which represents the robot character that users
control through Python code. The player exists on a grid-based world and can move
in four cardinal directions, collect gems, and sense the environment.

Architecture:
    - Player maintains position (x, y) on the grid
    - Direction is tracked as an enum (NORTH, EAST, SOUTH, WEST)
    - All actions increment a step counter for scoring
    - Collected gems are tracked by position to prevent duplicates

Usage Example:
    >>> player = Player(0, 0, "north")
    >>> player.move_forward()
    >>> player.turn_right()
    >>> player.collect_gem((1, 0))
    >>> print(player.get_step_count())
    2

Author: Python Learning Game Team
Version: 2.0 (with pixel art graphics)
Last Modified: October 2, 2025
"""

from typing import Tuple, List
from enum import Enum

class Direction(Enum):
    """
    Cardinal direction enumeration for player facing.
    
    The player can face one of four directions which affects movement:
    - NORTH: Move up (decrease y)
    - EAST: Move right (increase x)
    - SOUTH: Move down (increase y)
    - WEST: Move left (decrease x)
    
    Note: Y-axis increases downward (standard screen coordinates)
    """
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"

class Player:
    """
    Robot character controlled by user's Python code.
    
    The Player represents the main character that users program to navigate
    levels, collect gems, and reach goals. It maintains state including position,
    direction, collected items, and action history.
    
    Attributes:
        x (int): Current grid X position (0-based, left to right)
        y (int): Current grid Y position (0-based, top to bottom)
        direction (Direction): Current facing direction (affects movement)
        collected_gems (List[Tuple[int, int]]): List of collected gem positions
        step_count (int): Total actions taken (for scoring/optimization)
    
    Coordinate System:
        (0,0) is top-left corner of grid
        X increases rightward
        Y increases downward
        
        Example 3x3 grid:
        (0,0) (1,0) (2,0)
        (0,1) (1,1) (2,1)
        (0,2) (1,2) (2,2)
    
    Example:
        >>> player = Player(5, 5, "north")
        >>> player.move_forward()  # Moves to (5, 4)
        >>> player.turn_right()    # Now facing east
        >>> player.move_forward()  # Moves to (6, 4)
    """
    
    def __init__(self, x: int, y: int, direction: str = "north"):
        """
        Initialize player at starting position with given direction.
        
        Sets up the player's initial state including position, direction,
        and empty collection lists. This is called at the start of each level
        or when resetting the player.
        
        Args:
            x (int): Starting X coordinate on the grid (0-based)
            y (int): Starting Y coordinate on the grid (0-based)
            direction (str): Starting direction as string ("north", "east", 
                           "south", or "west"). Defaults to "north".
        
        Raises:
            ValueError: If direction string is not a valid Direction value
        
        Example:
            >>> player = Player(0, 0)  # Start at top-left facing north
            >>> player = Player(5, 3, "east")  # Custom start position
        """
        # Store grid position (will be validated by game logic)
        self.x = x
        self.y = y
        
        # Convert string direction to enum for type safety
        # This will raise ValueError if direction is invalid
        self.direction = Direction(direction)
        
        # Track gems collected by position (prevents duplicate collection)
        # Each tuple is (x, y) position of a gem
        self.collected_gems: List[Tuple[int, int]] = []
        
        # Count every action taken (move, turn) for optimization scoring
        # Lower step count = more efficient solution
        self.step_count = 0
    
    def get_position(self) -> Tuple[int, int]:
        """
        Get player's current grid position.
        
        Returns the current (x, y) coordinates as a tuple. Useful for
        checking if player has reached a goal or for debugging.
        
        Returns:
            Tuple[int, int]: Current position as (x, y)
        
        Example:
            >>> player = Player(3, 5)
            >>> player.get_position()
            (3, 5)
        """
        return (self.x, self.y)
    
    def get_direction(self) -> Direction:
        """
        Get player's current facing direction.
        
        Returns:
            Direction: Current direction enum (NORTH, EAST, SOUTH, or WEST)
        
        Example:
            >>> player = Player(0, 0, "north")
            >>> player.get_direction()
            <Direction.NORTH: 'north'>
        """
        return self.direction
    
    def move_forward(self) -> Tuple[int, int]:
        """
        Move player one tile forward in the current facing direction.
        
        This is the primary movement function called by user code. The player
        moves exactly one tile in whatever direction they're currently facing.
        Movement happens instantly at the logic level, but the renderer can
        animate it smoothly.
        
        Direction Behavior:
            - NORTH: Decreases Y (moves up)
            - EAST: Increases X (moves right)
            - SOUTH: Increases Y (moves down)
            - WEST: Decreases X (moves left)
        
        Note: This function does NOT check for collisions or boundaries.
        The Game class must validate the move before calling this.
        
        Returns:
            Tuple[int, int]: New position after moving as (x, y)
        
        Side Effects:
            - Updates self.x and/or self.y
            - Increments self.step_count by 1
        
        Example:
            >>> player = Player(5, 5, "north")
            >>> player.move_forward()
            (5, 4)  # Moved up one tile
            >>> player.step_count
            1
        """
        # Store old position (could be used for animation or undo)
        old_x, old_y = self.x, self.y
        
        # Update position based on facing direction
        # Y-axis increases downward in screen coordinates
        if self.direction == Direction.NORTH:
            self.y -= 1  # Move up (decrease Y)
        elif self.direction == Direction.EAST:
            self.x += 1  # Move right (increase X)
        elif self.direction == Direction.SOUTH:
            self.y += 1  # Move down (increase Y)
        elif self.direction == Direction.WEST:
            self.x -= 1  # Move left (decrease X)
        
        # Increment step counter for scoring
        # Every action counts toward optimization metrics
        self.step_count += 1
        
        return (self.x, self.y)
    
    def turn_left(self):
        """
        Rotate player 90 degrees counter-clockwise (left).
        
        Changes the player's facing direction without moving position.
        This is one of the basic commands available to user code.
        
        Direction Changes:
            NORTH → WEST
            WEST  → SOUTH
            SOUTH → EAST
            EAST  → NORTH
        
        Side Effects:
            - Updates self.direction
            - Increments self.step_count by 1
        
        Example:
            >>> player = Player(0, 0, "north")
            >>> player.turn_left()
            >>> player.get_direction()
            <Direction.WEST: 'west'>
        """
        # Map each direction to its 90-degree counter-clockwise result
        # Using a dictionary lookup is cleaner than if/elif chain
        direction_map = {
            Direction.NORTH: Direction.WEST,   # North → West
            Direction.EAST: Direction.NORTH,   # East → North
            Direction.SOUTH: Direction.EAST,   # South → East
            Direction.WEST: Direction.SOUTH    # West → South
        }
        self.direction = direction_map[self.direction]
        
        # Turning counts as an action for optimization scoring
        self.step_count += 1
    
    def turn_right(self):
        """
        Rotate player 90 degrees clockwise (right).
        
        Changes the player's facing direction without moving position.
        This is one of the basic commands available to user code.
        
        Direction Changes:
            NORTH → EAST
            EAST  → SOUTH
            SOUTH → WEST
            WEST  → NORTH
        
        Side Effects:
            - Updates self.direction
            - Increments self.step_count by 1
        
        Example:
            >>> player = Player(0, 0, "north")
            >>> player.turn_right()
            >>> player.get_direction()
            <Direction.EAST: 'east'>
        """
        # Map each direction to its 90-degree clockwise result
        direction_map = {
            Direction.NORTH: Direction.EAST,   # North → East
            Direction.EAST: Direction.SOUTH,   # East → South
            Direction.SOUTH: Direction.WEST,   # South → West
            Direction.WEST: Direction.NORTH    # West → North
        }
        self.direction = direction_map[self.direction]
        
        # Turning counts as an action for optimization scoring
        self.step_count += 1
    
    def turn_around(self):
        """
        Rotate player 180 degrees to face opposite direction.
        
        This is a convenience function equivalent to turning left twice
        or turning right twice, but counts as only one action.
        
        Direction Changes:
            NORTH ↔ SOUTH
            EAST  ↔ WEST
        
        Side Effects:
            - Updates self.direction
            - Increments self.step_count by 1
        
        Example:
            >>> player = Player(0, 0, "north")
            >>> player.turn_around()
            >>> player.get_direction()
            <Direction.SOUTH: 'south'>
        """
        # Map each direction to its opposite (180-degree rotation)
        direction_map = {
            Direction.NORTH: Direction.SOUTH,  # North ↔ South
            Direction.EAST: Direction.WEST,    # East ↔ West
            Direction.SOUTH: Direction.NORTH,  # South ↔ North
            Direction.WEST: Direction.EAST     # West ↔ East
        }
        self.direction = direction_map[self.direction]
        
        # 180-degree turn counts as one action (more efficient than 2 turns)
        self.step_count += 1
    
    def collect_gem(self, gem_position: Tuple[int, int]):
        """
        Collect a gem at the specified grid position.
        
        Adds a gem to the collected list if not already collected.
        This prevents double-counting gems if the player walks over
        the same spot multiple times.
        
        Args:
            gem_position (Tuple[int, int]): Position of gem as (x, y)
        
        Side Effects:
            - Adds position to self.collected_gems if not already present
            - Does NOT increment step_count (collection is automatic)
        
        Note:
            This is typically called automatically by the Game class when
            the player moves onto a tile with a gem. User code doesn't
            call this directly.
        
        Example:
            >>> player = Player(0, 0)
            >>> player.collect_gem((2, 3))
            >>> player.collect_gem((2, 3))  # Duplicate ignored
            >>> len(player.get_collected_gems())
            1
        """
        # Only add if not already collected (prevents duplicates)
        # Using 'not in' on a list is O(n), but gem counts are small
        if gem_position not in self.collected_gems:
            self.collected_gems.append(gem_position)
    
    def get_collected_gems(self) -> List[Tuple[int, int]]:
        """
        Get list of all collected gem positions.
        
        Returns a copy of the list to prevent external modification
        of the player's internal state.
        
        Returns:
            List[Tuple[int, int]]: Copy of collected gem positions
        
        Example:
            >>> player = Player(0, 0)
            >>> player.collect_gem((1, 1))
            >>> player.collect_gem((2, 2))
            >>> player.get_collected_gems()
            [(1, 1), (2, 2)]
        """
        # Return a copy to prevent external code from modifying our list
        return self.collected_gems.copy()
    
    def get_step_count(self) -> int:
        """
        Get total number of actions taken by player.
        
        The step count includes all movements and turns. It's used
        for optimization scoring - players are rewarded for finding
        solutions with fewer steps.
        
        Returns:
            int: Total steps taken (moves + turns)
        
        Example:
            >>> player = Player(0, 0)
            >>> player.move_forward()
            >>> player.turn_right()
            >>> player.move_forward()
            >>> player.get_step_count()
            3
        """
        return self.step_count
    
    def reset(self, x: int, y: int, direction: str = "north"):
        """
        Reset player to initial state for a new level attempt.
        
        This is called when restarting a level or loading a new level.
        All progress (collected gems, steps) is cleared and the player
        is repositioned to the starting location.
        
        Args:
            x (int): New starting X position
            y (int): New starting Y position
            direction (str): New starting direction (default "north")
        
        Side Effects:
            - Updates self.x and self.y
            - Updates self.direction
            - Clears self.collected_gems list
            - Resets self.step_count to 0
        
        Example:
            >>> player = Player(0, 0)
            >>> player.move_forward()
            >>> player.collect_gem((0, 1))
            >>> player.reset(5, 5, "east")
            >>> player.get_position()
            (5, 5)
            >>> player.get_step_count()
            0
        """
        # Set new starting position
        self.x = x
        self.y = y
        
        # Set new starting direction (converts string to enum)
        self.direction = Direction(direction)
        
        # Clear all collected gems from previous attempt
        self.collected_gems.clear()
        
        # Reset step counter for fresh optimization score
        self.step_count = 0
    
    def get_next_position(self) -> Tuple[int, int]:
        """
        Calculate the position player would move to if moving forward.
        
        This is a "look-ahead" function that doesn't actually move the player.
        It's useful for collision detection and pathfinding - the Game class
        can check if the next position is valid before committing to the move.
        
        Returns:
            Tuple[int, int]: Position after hypothetical forward move as (x, y)
        
        Note:
            This does NOT modify player state. It only calculates and returns
            what the new position WOULD be.
        
        Example:
            >>> player = Player(5, 5, "north")
            >>> player.get_next_position()
            (5, 4)  # Would move up
            >>> player.get_position()
            (5, 5)  # Player hasn't actually moved
        """
        # Calculate next position based on current direction
        # Same logic as move_forward() but without modifying state
        if self.direction == Direction.NORTH:
            return (self.x, self.y - 1)  # Moving up
        elif self.direction == Direction.EAST:
            return (self.x + 1, self.y)  # Moving right
        elif self.direction == Direction.SOUTH:
            return (self.x, self.y + 1)  # Moving down
        elif self.direction == Direction.WEST:
            return (self.x - 1, self.y)  # Moving left
        
        # Should never reach here since Direction enum covers all cases
        # Return current position as fallback (no movement)
        return (self.x, self.y)
