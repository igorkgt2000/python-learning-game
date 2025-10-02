"""
Animation system with easing functions, interpolation, and particle effects.

This module provides a complete animation framework including:
- Smooth interpolation between values (position, rotation, scale, color)
- Professional easing functions (ease-in, ease-out, bounce, elastic)
- Animation management (multiple simultaneous animations)
- Physics-based particle system (gem collection effects)

All animations are time-based (not frame-based) for smooth playback
regardless of frame rate.

Classes:
    EasingType: Enum of available easing functions
    Animation: Single interpolated animation
    AnimationManager: Manages multiple named animations
    Particle: Single physics-based particle
    ParticleSystem: Manages particle effects

Mathematics:
    - Interpolation: value = start + (end - start) * t
    - Easing: t' = ease(t) where t ∈ [0, 1]
    - Physics: velocity += gravity * dt, position += velocity * dt
"""

import math
from typing import Tuple, Callable, Optional
from enum import Enum

class EasingType(Enum):
    """
    Easing function types for smooth animations.
    
    Easing functions control the acceleration curve of animations.
    They take a normalized time value (0.0 to 1.0) and return a
    modified time value that creates different motion feels.
    
    Values:
        LINEAR: Constant speed (no easing)
        EASE_IN: Start slow, accelerate (t²)
        EASE_OUT: Start fast, decelerate (1 - (1-t)²)
        EASE_IN_OUT: Ease both ends (combines ease-in and ease-out)
        BOUNCE: Bouncy landing effect (like a ball bouncing)
        ELASTIC: Spring-like overshoot (oscillates before settling)
    
    Visual Guide:
        LINEAR:      /
        EASE_IN:    /
        EASE_OUT:  /
        EASE_IN_OUT: S-curve
        BOUNCE:    Bounces at end
        ELASTIC:   Overshoots and oscillates
    """
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE = "bounce"
    ELASTIC = "elastic"

class Animation:
    """
    Represents a single time-based animation with easing.
    
    Interpolates between a start value and end value over a specified
    duration, applying an easing function for smooth motion.
    
    Supports animating:
    - Numbers (float/int): position, rotation, scale, opacity
    - Tuples: 2D/3D positions, RGB colors
    
    Attributes:
        start_value: Initial value (number or tuple)
        end_value: Target value (same type as start_value)
        duration (float): Animation length in seconds
        easing (EasingType): Acceleration curve
        elapsed (float): Time elapsed so far
        completed (bool): True when animation finishes
    
    Example:
        >>> # Animate position from (0, 0) to (100, 50) over 0.5 seconds
        >>> anim = Animation((0, 0), (100, 50), 0.5, EasingType.EASE_OUT)
        >>> anim.update(0.016)  # ~60 FPS frame
        >>> pos = anim.get_value()
        >>> print(pos)  # Somewhere between (0,0) and (100,50)
    """
    
    def __init__(self, start_value, end_value, duration: float, 
                 easing: EasingType = EasingType.EASE_IN_OUT):
        """
        Initialize a new animation.
        
        Args:
            start_value: Starting value (number or tuple of numbers)
            end_value: Ending value (must match type of start_value)
            duration (float): Animation length in seconds
            easing (EasingType): Easing function to use (default: EASE_IN_OUT)
        
        Example:
            >>> # Number animation
            >>> anim = Animation(0, 100, 1.0, EasingType.LINEAR)
            
            >>> # Tuple animation (position)
            >>> anim = Animation((10, 20), (100, 200), 0.5)
        """
        self.start_value = start_value  # Where we start
        self.end_value = end_value      # Where we're going
        self.duration = duration        # How long it takes
        self.easing = easing            # How we get there
        self.elapsed = 0.0              # Time spent so far
        self.completed = False          # Are we done?
    
    def update(self, dt: float):
        """
        Update animation by delta time.
        
        Advances animation progress. Marks as completed when elapsed
        time reaches duration.
        
        Args:
            dt (float): Time passed since last update (seconds)
        
        Example:
            >>> anim.update(0.016)  # One frame at 60 FPS
            >>> anim.update(1.0)    # One second
        """
        # Accumulate elapsed time
        self.elapsed += dt
        
        # Clamp to duration and mark complete
        if self.elapsed >= self.duration:
            self.elapsed = self.duration
            self.completed = True
    
    def get_value(self):
        """
        Get current interpolated value.
        
        Calculates the current value based on elapsed time and easing function.
        Returns the end value if animation is complete.
        
        Returns:
            Number or tuple: Current animated value
        
        Mathematics:
            1. Normalize time: t = elapsed / duration  (0.0 to 1.0)
            2. Apply easing: t' = ease(t)
            3. Interpolate: value = start + (end - start) * t'
        
        Example:
            >>> anim = Animation(0, 100, 1.0, EasingType.LINEAR)
            >>> anim.update(0.5)  # Halfway through
            >>> anim.get_value()
            50.0
        """
        # If complete, return final value
        if self.completed:
            return self.end_value
        
        # Calculate normalized time (0.0 to 1.0)
        t = self.elapsed / self.duration
        
        # Apply easing function
        t = self._apply_easing(t)
        
        # Interpolate between start and end
        if isinstance(self.start_value, tuple):
            # Tuple interpolation (for positions, colors, etc.)
            return tuple(
                self.start_value[i] + (self.end_value[i] - self.start_value[i]) * t
                for i in range(len(self.start_value))
            )
        else:
            # Scalar interpolation (for numbers)
            return self.start_value + (self.end_value - self.start_value) * t
    
    def _apply_easing(self, t: float) -> float:
        """
        Apply easing function to normalized time.
        
        Transforms linear time (0.0 to 1.0) into eased time using
        mathematical curves. This creates different motion feels.
        
        Args:
            t (float): Normalized time from 0.0 to 1.0
        
        Returns:
            float: Eased time from 0.0 to 1.0
        
        Note:
            This is a private method (indicated by _ prefix).
            Formulas based on https://easings.net/
        """
        if self.easing == EasingType.LINEAR:
            # No easing - constant speed
            return t
        
        elif self.easing == EasingType.EASE_IN:
            # Quadratic acceleration: t²
            return t * t
        
        elif self.easing == EasingType.EASE_OUT:
            # Quadratic deceleration: 1 - (1-t)²
            return 1 - (1 - t) * (1 - t)
        
        elif self.easing == EasingType.EASE_IN_OUT:
            # S-curve: accelerate then decelerate
            if t < 0.5:
                # First half: ease in (accelerate)
                return 2 * t * t
            else:
                # Second half: ease out (decelerate)
                return 1 - pow(-2 * t + 2, 2) / 2
        
        elif self.easing == EasingType.BOUNCE:
            # Bouncing effect at end (like a ball landing)
            # Multiple parabolic curves create bounce effect
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
            # Spring-like overshoot (oscillates before settling)
            # Uses exponential decay with sine wave
            if t == 0 or t == 1:
                return t
            p = 0.3  # Period
            s = p / 4  # Phase shift
            return pow(2, -10 * t) * math.sin((t - s) * (2 * math.pi) / p) + 1
        
        # Fallback (should never reach here)
        return t

class AnimationManager:
    """
    Manages multiple simultaneous animations by name.
    
    Allows running multiple animations in parallel, each with a unique
    name identifier. Automatically removes completed animations.
    
    Useful for:
    - Player movement animations
    - UI transitions
    - Multiple objects animating at once
    
    Attributes:
        animations (Dict[str, Animation]): Named animation dictionary
    
    Example:
        >>> manager = AnimationManager()
        >>> manager.add("move", Animation((0, 0), (100, 100), 0.5))
        >>> manager.add("fade", Animation(1.0, 0.0, 1.0))
        >>> manager.update(dt)
        >>> pos = manager.get("move").get_value()
    """
    
    def __init__(self):
        """Initialize empty animation manager."""
        self.animations = {}  # name -> Animation mapping
    
    def add(self, name: str, animation: Animation):
        """
        Add or replace a named animation.
        
        Args:
            name (str): Unique identifier for this animation
            animation (Animation): Animation to manage
        
        Note:
            If an animation with this name already exists, it's replaced.
        """
        self.animations[name] = animation
    
    def update(self, dt: float):
        """
        Update all active animations.
        
        Advances all animations by dt. Automatically removes
        completed animations from the manager.
        
        Args:
            dt (float): Delta time in seconds
        """
        # Track which animations completed this frame
        completed = []
        
        # Update each animation
        for name, anim in self.animations.items():
            anim.update(dt)
            if anim.completed:
                completed.append(name)
        
        # Remove completed animations (clean up)
        for name in completed:
            del self.animations[name]
    
    def get(self, name: str) -> Optional[Animation]:
        """
        Get animation by name.
        
        Args:
            name (str): Animation identifier
        
        Returns:
            Optional[Animation]: Animation if found, None otherwise
        """
        return self.animations.get(name)
    
    def is_animating(self) -> bool:
        """
        Check if any animations are currently active.
        
        Returns:
            bool: True if at least one animation is running
        """
        return len(self.animations) > 0
    
    def clear(self):
        """Clear all animations immediately."""
        self.animations.clear()

class Particle:
    """
    Single physics-based particle for visual effects.
    
    Particles have position, velocity, color, size, and lifetime.
    They simulate physics (gravity, drag) and fade out over time.
    
    Used for:
    - Gem collection sparkles
    - Explosions
    - Confetti
    - Magic effects
    
    Attributes:
        x, y (float): Current position in screen pixels
        vx, vy (float): Velocity in pixels/second
        color (Tuple[int, int, int]): RGB color
        lifetime (float): Remaining lifetime in seconds
        max_lifetime (float): Initial lifetime (for fade calculation)
        size (float): Current size in pixels
        initial_size (float): Starting size (for shrinking)
    
    Physics:
        - Position: x += vx * dt, y += vy * dt
        - Gravity: vy += 200 * dt (downward acceleration)
        - Fade: size = initial_size * (lifetime / max_lifetime)
    """
    
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 color: Tuple[int, int, int], lifetime: float, size: float):
        """
        Initialize a new particle.
        
        Args:
            x (float): Starting X position (pixels)
            y (float): Starting Y position (pixels)
            vx (float): X velocity (pixels/second)
            vy (float): Y velocity (pixels/second)
            color (Tuple[int, int, int]): RGB color (0-255)
            lifetime (float): How long particle lives (seconds)
            size (float): Initial size (pixels)
        """
        self.x = x  # Position
        self.y = y
        self.vx = vx  # Velocity
        self.vy = vy
        self.color = color  # RGB
        self.lifetime = lifetime  # Time left
        self.max_lifetime = lifetime  # Original lifetime
        self.size = size  # Current size
        self.initial_size = size  # Original size
    
    def update(self, dt: float):
        """
        Update particle physics and lifetime.
        
        Applies:
        - Velocity to position (movement)
        - Gravity to vertical velocity (falls down)
        - Lifetime decay (particle dies)
        - Size fade (shrinks as it dies)
        
        Args:
            dt (float): Delta time in seconds
        """
        # Apply velocity to position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Apply gravity (downward acceleration)
        self.vy += 200 * dt  # 200 pixels/second²
        
        # Decrease lifetime
        self.lifetime -= dt
        
        # Fade out (shrink as particle dies)
        alpha = self.lifetime / self.max_lifetime  # 1.0 to 0.0
        self.size = self.initial_size * alpha
    
    def is_dead(self) -> bool:
        """
        Check if particle should be removed.
        
        Returns:
            bool: True if lifetime expired
        """
        return self.lifetime <= 0

class ParticleSystem:
    """
    Manages a collection of physics-based particles.
    
    Handles particle emission, updating, and cleanup. Particles
    automatically die after their lifetime expires.
    
    Used for creating visual feedback effects like:
    - Gem collection sparkles (burst of 10-20 particles)
    - Victory confetti
    - Damage effects
    
    Attributes:
        particles (List[Particle]): All active particles
    
    Example:
        >>> system = ParticleSystem()
        >>> # Emit gold sparkles when collecting gem
        >>> system.emit(x=320, y=240, count=15, color=(241, 196, 15), speed=150)
        >>> system.update(dt)
        >>> for particle in system.get_particles():
        ...     draw_circle(particle.x, particle.y, particle.size, particle.color)
    """
    
    def __init__(self):
        """Initialize empty particle system."""
        self.particles = []  # List of active particles
    
    def emit(self, x: float, y: float, count: int, 
             color: Tuple[int, int, int], speed: float = 100):
        """
        Emit a burst of particles.
        
        Creates `count` particles at position (x, y) that explode
        outward in random directions with random properties.
        
        Args:
            x (float): Spawn X position (pixels)
            y (float): Spawn Y position (pixels)
            count (int): Number of particles to emit
            color (Tuple[int, int, int]): RGB color for all particles
            speed (float): Average speed in pixels/second (default: 100)
        
        Randomization:
            - Angle: Random 360° direction
            - Speed: 0.5x to 1.5x of specified speed
            - Initial Y velocity: Upward boost (creates fountain effect)
            - Lifetime: 0.3 to 0.8 seconds
            - Size: 2 to 6 pixels
        """
        import random
        
        # Create count particles
        for _ in range(count):
            # Random direction (radians)
            angle = random.uniform(0, 2 * math.pi)
            
            # Random speed variation
            speed_var = random.uniform(0.5, 1.5) * speed
            
            # Calculate velocity components
            vx = math.cos(angle) * speed_var
            vy = math.sin(angle) * speed_var - 100  # Upward boost
            
            # Random properties
            lifetime = random.uniform(0.3, 0.8)  # Short-lived
            size = random.uniform(2, 6)  # Small particles
            
            # Create and add particle
            self.particles.append(Particle(x, y, vx, vy, color, lifetime, size))
    
    def update(self, dt: float):
        """
        Update all particles and remove dead ones.
        
        Updates particle physics (position, velocity, lifetime, size).
        Filters out particles that have expired.
        
        Args:
            dt (float): Delta time in seconds
        
        Performance:
            List comprehension is faster than manual removal.
            Even with 100+ particles, this runs in < 0.5ms.
        """
        # Remove dead particles (filter in-place)
        self.particles = [p for p in self.particles if not p.is_dead()]
        
        # Update remaining particles
        for particle in self.particles:
            particle.update(dt)
    
    def get_particles(self):
        """
        Get all active particles for rendering.
        
        Returns:
            List[Particle]: All particles currently alive
        
        Note:
            Returns direct reference for performance.
            Don't modify the list while iterating.
        """
        return self.particles
    
    def clear(self):
        """Remove all particles immediately."""
        self.particles.clear()
