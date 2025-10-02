"""
Sprite management system for loading and animating pixel art sprites.
"""

import pygame
from pathlib import Path
from typing import Dict, Tuple, Optional
from enum import Enum


class SpriteManager:
    """Manages loading, caching, and animating sprites."""
    
    def __init__(self, assets_path: Optional[Path] = None):
        """Initialize sprite manager."""
        if assets_path is None:
            # Default to assets/sprites in project root
            assets_path = Path(__file__).parent.parent.parent / "assets" / "sprites"
        
        self.assets_path = Path(assets_path)
        self.sprites: Dict[str, pygame.Surface] = {}
        self.animations: Dict[str, list] = {}
        self.animation_speeds: Dict[str, float] = {}
        self.animation_timers: Dict[str, float] = {}
        self.current_frames: Dict[str, int] = {}
        
        # Load all sprites
        self._load_sprites()
    
    def _load_sprites(self):
        """Load all sprite assets."""
        if not self.assets_path.exists():
            print(f"Warning: Sprites directory not found at {self.assets_path}")
            return
        
        # Load player sprites
        for direction in ['north', 'south', 'east', 'west']:
            animation_frames = []
            for frame in range(2):  # 2 frames per direction
                sprite_name = f"player_{direction}_{frame}"
                sprite_path = self.assets_path / f"{sprite_name}.png"
                if sprite_path.exists():
                    self.sprites[sprite_name] = pygame.image.load(str(sprite_path)).convert_alpha()
                    animation_frames.append(sprite_name)
            
            if animation_frames:
                anim_name = f"player_{direction}"
                self.animations[anim_name] = animation_frames
                self.animation_speeds[anim_name] = 0.3  # 300ms per frame
                self.current_frames[anim_name] = 0
                self.animation_timers[anim_name] = 0.0
        
        # Load tile sprites
        for tile_type in ['floor', 'grass', 'wall']:
            sprite_name = f"tile_{tile_type}"
            sprite_path = self.assets_path / f"{sprite_name}.png"
            if sprite_path.exists():
                self.sprites[sprite_name] = pygame.image.load(str(sprite_path)).convert_alpha()
        
        # Load gem animation
        gem_frames = []
        for frame in range(4):
            sprite_name = f"gem_{frame}"
            sprite_path = self.assets_path / f"{sprite_name}.png"
            if sprite_path.exists():
                self.sprites[sprite_name] = pygame.image.load(str(sprite_path)).convert_alpha()
                gem_frames.append(sprite_name)
        
        if gem_frames:
            self.animations['gem'] = gem_frames
            self.animation_speeds['gem'] = 0.15  # Faster animation
            self.current_frames['gem'] = 0
            self.animation_timers['gem'] = 0.0
        
        # Load goal animation
        goal_frames = []
        for frame in range(4):
            sprite_name = f"goal_{frame}"
            sprite_path = self.assets_path / f"{sprite_name}.png"
            if sprite_path.exists():
                self.sprites[sprite_name] = pygame.image.load(str(sprite_path)).convert_alpha()
                goal_frames.append(sprite_name)
        
        if goal_frames:
            self.animations['goal'] = goal_frames
            self.animation_speeds['goal'] = 0.2
            self.current_frames['goal'] = 0
            self.animation_timers['goal'] = 0.0
        
        # Load particle sprites
        for color in ['gem_yellow', 'goal_green', 'player_blue']:
            sprite_name = f"particle_{color}"
            sprite_path = self.assets_path / f"{sprite_name}.png"
            if sprite_path.exists():
                self.sprites[sprite_name] = pygame.image.load(str(sprite_path)).convert_alpha()
    
    def update(self, dt: float):
        """Update all animations."""
        for anim_name in self.animations:
            self.animation_timers[anim_name] += dt
            
            # Check if we should advance to next frame
            if self.animation_timers[anim_name] >= self.animation_speeds[anim_name]:
                self.animation_timers[anim_name] = 0.0
                self.current_frames[anim_name] = (
                    self.current_frames[anim_name] + 1
                ) % len(self.animations[anim_name])
    
    def get_sprite(self, sprite_name: str, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """Get a sprite by name, optionally scaled to size."""
        sprite = self.sprites.get(sprite_name)
        if sprite and size:
            return pygame.transform.scale(sprite, size)
        return sprite
    
    def get_animated_sprite(self, animation_name: str, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """Get current frame of an animation."""
        if animation_name not in self.animations:
            return None
        
        frame_index = self.current_frames[animation_name]
        sprite_name = self.animations[animation_name][frame_index]
        return self.get_sprite(sprite_name, size)
    
    def get_player_sprite(self, direction: str, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """Get current player sprite for given direction."""
        anim_name = f"player_{direction}"
        return self.get_animated_sprite(anim_name, size)
    
    def get_tile_sprite(self, tile_type: str, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """Get tile sprite."""
        sprite_name = f"tile_{tile_type}"
        return self.get_sprite(sprite_name, size)
    
    def get_gem_sprite(self, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """Get current gem animation frame."""
        return self.get_animated_sprite('gem', size)
    
    def get_goal_sprite(self, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """Get current goal animation frame."""
        return self.get_animated_sprite('goal', size)
    
    def get_particle_sprite(self, color: str, size: Optional[Tuple[int, int]] = None) -> Optional[pygame.Surface]:
        """Get particle sprite by color."""
        sprite_name = f"particle_{color}"
        return self.get_sprite(sprite_name, size)
    
    def is_loaded(self) -> bool:
        """Check if sprites are loaded."""
        return len(self.sprites) > 0

