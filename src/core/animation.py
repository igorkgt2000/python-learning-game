"""
Animation system with easing functions and sprite management.
"""

import math
from typing import Tuple, Callable, Optional
from enum import Enum

class EasingType(Enum):
    """Easing function types for smooth animations."""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE = "bounce"
    ELASTIC = "elastic"

class Animation:
    """Represents a single animation."""
    
    def __init__(self, start_value, end_value, duration: float, 
                 easing: EasingType = EasingType.EASE_IN_OUT):
        """Initialize animation."""
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.easing = easing
        self.elapsed = 0.0
        self.completed = False
    
    def update(self, dt: float):
        """Update animation progress."""
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self.completed = True
    
    def get_value(self):
        """Get current animated value."""
        if self.completed:
            return self.end_value
        
        t = self.elapsed / self.duration
        t = self._apply_easing(t)
        
        # Interpolate between start and end
        if isinstance(self.start_value, tuple):
            return tuple(
                self.start_value[i] + (self.end_value[i] - self.start_value[i]) * t
                for i in range(len(self.start_value))
            )
        else:
            return self.start_value + (self.end_value - self.start_value) * t
    
    def _apply_easing(self, t: float) -> float:
        """Apply easing function to normalized time."""
        if self.easing == EasingType.LINEAR:
            return t
        elif self.easing == EasingType.EASE_IN:
            return t * t
        elif self.easing == EasingType.EASE_OUT:
            return 1 - (1 - t) * (1 - t)
        elif self.easing == EasingType.EASE_IN_OUT:
            if t < 0.5:
                return 2 * t * t
            else:
                return 1 - pow(-2 * t + 2, 2) / 2
        elif self.easing == EasingType.BOUNCE:
            if t < 1 / 2.75:
                return 7.5625 * t * t
            elif t < 2 / 2.75:
                t -= 1.5 / 2.75
                return 7.5625 * t * t + 0.75
            elif t < 2.5 / 2.75:
                t -= 2.25 / 2.75
                return 7.5625 * t * t + 0.9375
            else:
                t -= 2.625 / 2.75
                return 7.5625 * t * t + 0.984375
        elif self.easing == EasingType.ELASTIC:
            if t == 0 or t == 1:
                return t
            p = 0.3
            s = p / 4
            return pow(2, -10 * t) * math.sin((t - s) * (2 * math.pi) / p) + 1
        
        return t

class AnimationManager:
    """Manages multiple animations."""
    
    def __init__(self):
        """Initialize animation manager."""
        self.animations = {}
    
    def add(self, name: str, animation: Animation):
        """Add an animation."""
        self.animations[name] = animation
    
    def update(self, dt: float):
        """Update all animations."""
        completed = []
        for name, anim in self.animations.items():
            anim.update(dt)
            if anim.completed:
                completed.append(name)
        
        # Remove completed animations
        for name in completed:
            del self.animations[name]
    
    def get(self, name: str) -> Optional[Animation]:
        """Get animation by name."""
        return self.animations.get(name)
    
    def is_animating(self) -> bool:
        """Check if any animations are active."""
        return len(self.animations) > 0
    
    def clear(self):
        """Clear all animations."""
        self.animations.clear()

class Particle:
    """Single particle for effects."""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 color: Tuple[int, int, int], lifetime: float, size: float):
        """Initialize particle."""
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
        self.initial_size = size
    
    def update(self, dt: float):
        """Update particle."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 200 * dt  # Gravity
        self.lifetime -= dt
        
        # Fade out
        alpha = self.lifetime / self.max_lifetime
        self.size = self.initial_size * alpha
    
    def is_dead(self) -> bool:
        """Check if particle is dead."""
        return self.lifetime <= 0

class ParticleSystem:
    """Manages particle effects."""
    
    def __init__(self):
        """Initialize particle system."""
        self.particles = []
    
    def emit(self, x: float, y: float, count: int, 
             color: Tuple[int, int, int], speed: float = 100):
        """Emit particles."""
        import random
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed_var = random.uniform(0.5, 1.5) * speed
            vx = math.cos(angle) * speed_var
            vy = math.sin(angle) * speed_var - 100  # Initial upward velocity
            lifetime = random.uniform(0.3, 0.8)
            size = random.uniform(2, 6)
            
            self.particles.append(Particle(x, y, vx, vy, color, lifetime, size))
    
    def update(self, dt: float):
        """Update all particles."""
        self.particles = [p for p in self.particles if not p.is_dead()]
        for particle in self.particles:
            particle.update(dt)
    
    def get_particles(self):
        """Get all active particles."""
        return self.particles
    
    def clear(self):
        """Clear all particles."""
        self.particles.clear()
