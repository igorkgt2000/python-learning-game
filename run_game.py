#!/usr/bin/env python3
"""
Simple Pygame-only game runner for testing levels.

This runs the game WITHOUT the Tkinter UI - just pure Pygame.
Good for testing levels and game mechanics quickly.

Usage:
    python run_game.py           # Start at level 1
    python run_game.py 5         # Start at level 5
"""

import pygame
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core.config import Config
from core.game import Game
from core.player import Player
from core.grid import Grid
from core.level import Level
from levels.level_loader import LevelLoader


def main():
    """Run the game."""
    # Get starting level from command line
    start_level = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    # Initialize
    config = Config()
    pygame.init()
    
    # Create window
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.WINDOW_TITLE)
    
    # Load all levels
    levels_dir = Path(__file__).parent / 'src' / 'levels'
    level_loader = LevelLoader(levels_dir)
    
    print(f"✅ Loaded {level_loader.get_level_count()} levels")
    print(f"🎮 Starting at Level {start_level}")
    print("\n" + "="*60)
    print("CONTROLS:")
    print("  ESC - Quit game")
    print("  R - Reset current level")
    print("  N - Next level")
    print("  P - Previous level")
    print("\nNote: This is a test runner. You can't write code here.")
    print("      Use the full UI (main.py) to write Python code!")
    print("="*60 + "\n")
    
    # Create game
    game = Game(config)
    game.screen = screen
    
    # Load starting level
    current_level_index = start_level - 1
    
    # Main loop
    clock = pygame.Clock()
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # Reset level
                    level = level_loader.get_level(current_level_index)
                    if level:
                        game.current_level = level
                        game.grid.clear()
                        # Set up grid from level
                        for obs in level.obstacles:
                            game.grid.set_tile(obs[0], obs[1], game.grid.TileType.WALL)
                        for gem in level.gems:
                            game.grid.set_tile(gem[0], gem[1], game.grid.TileType.GEM)
                        game.grid.set_tile(level.goal_pos[0], level.goal_pos[1], game.grid.TileType.GOAL)
                        # Reset player
                        game.player.x, game.player.y = level.start_pos
                        game.player.direction = game.player.Direction.NORTH
                        game.player.collected_gems.clear()
                        game.player.step_count = 0
                        print(f"🔄 Reset: {level.name}")
                
                elif event.key == pygame.K_n:
                    # Next level
                    current_level_index = min(current_level_index + 1, level_loader.get_level_count() - 1)
                    level = level_loader.get_level(current_level_index)
                    if level:
                        game.current_level = level
                        game.grid = Grid(level.grid_size, level.grid_size)
                        for obs in level.obstacles:
                            game.grid.set_tile(obs[0], obs[1], game.grid.TileType.WALL)
                        for gem in level.gems:
                            game.grid.set_tile(gem[0], gem[1], game.grid.TileType.GEM)
                        game.grid.set_tile(level.goal_pos[0], level.goal_pos[1], game.grid.TileType.GOAL)
                        game.player = Player(*level.start_pos)
                        print(f"➡️  Next: {level.name}")
                
                elif event.key == pygame.K_p:
                    # Previous level
                    current_level_index = max(current_level_index - 1, 0)
                    level = level_loader.get_level(current_level_index)
                    if level:
                        game.current_level = level
                        game.grid = Grid(level.grid_size, level.grid_size)
                        for obs in level.obstacles:
                            game.grid.set_tile(obs[0], obs[1], game.grid.TileType.WALL)
                        for gem in level.gems:
                            game.grid.set_tile(gem[0], gem[1], game.grid.TileType.GEM)
                        game.grid.set_tile(level.goal_pos[0], level.goal_pos[1], game.grid.TileType.GOAL)
                        game.player = Player(*level.start_pos)
                        print(f"⬅️  Previous: {level.name}")
        
        # Load initial level if needed
        if game.current_level is None:
            level = level_loader.get_level(current_level_index)
            if level:
                game.current_level = level
                game.grid = Grid(level.grid_size, level.grid_size)
                for obs in level.obstacles:
                    game.grid.set_tile(obs[0], obs[1], game.grid.TileType.WALL)
                for gem in level.gems:
                    game.grid.set_tile(gem[0], gem[1], game.grid.TileType.GEM)
                game.grid.set_tile(level.goal_pos[0], level.goal_pos[1], game.grid.TileType.GOAL)
                game.player = Player(*level.start_pos)
                print(f"📚 Loaded: {level.name}")
        
        # Update
        dt = clock.get_time() / 1000.0
        game.renderer.update(dt)
        
        # Render
        screen.fill(config.BACKGROUND_COLOR)
        if game.current_level and game.grid and game.player:
            game.renderer.render_grid(game.grid)
            game.renderer.render_player(game.player)
            game.renderer.render_ui(game.player, game.current_level)
            game.renderer.render_particles()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("\n👋 Thanks for playing!")


if __name__ == "__main__":
    main()

