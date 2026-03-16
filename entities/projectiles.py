"""
Projectile classes - Bullets and homing projectiles
Demonstrates Inheritance and Polymorphism
"""

import pygame
import os
import math
from entities.base import GameObject
import config


class Bullet(GameObject):
    """
    Standard projectile fired by player and enemies.
    
    Inheritance: Extends GameObject
    Polymorphism: Different bullet types with different behaviors
    """
    
    def __init__(self, x: float, y: float, speed: float, color_type: str = "blue", 
                 is_beam: bool = False, damage: int = 5, custom_path: str = None):
        """
        Initialize bullet with customizable properties.
        
        Args:
            x: Starting X position
            y: Starting Y position
            speed: Vertical speed (negative = up, positive = down)
            color_type: Color of the laser (blue, red, etc)
            is_beam: Whether this is a beam laser
            damage: Damage dealt on hit
            custom_path: Custom image path override
        """
        # Determine image path and scale
        if custom_path:
            path = custom_path
            size = (15, 120)
        elif is_beam:
            path = os.path.join("PNG", "Lasers", f"laser{color_type.capitalize()}04.png")
            size = (15, 100)
        else:
            path = os.path.join("PNG", "Lasers", f"laser{color_type.capitalize()}01.png")
            size = (10, 30)
        
        super().__init__(x, y, path, size)
        
        # Encapsulation: Private attributes
        self._speed = speed
        self._damage = damage
    
    @property
    def speed(self) -> float:
        """Get bullet speed"""
        return self._speed
    
    @property
    def damage(self) -> int:
        """Get damage value"""
        return self._damage
    
    def update(self):
        """Move bullet and remove if off-screen"""
        self.rect.y += self._speed
        
        # Remove bullet if off-screen
        if self.rect.bottom < 0 or self.rect.top > config.HEIGHT:
            self.kill()


class HomingBullet(GameObject):
    """
    Special bullet that tracks and follows a target.
    Fired by boss enemies.
    
    Inheritance: Extends GameObject
    Composition: Contains reference to target GameObject
    """
    
    def __init__(self, x: float, y: float, target: GameObject):
        """
        Initialize homing bullet.
        
        Args:
            x: Starting X position
            y: Starting Y position
            target: Target GameObject to track
        """
        path = os.path.join("PNG", "Lasers", "laserRed08.png")
        super().__init__(x, y, path, (15, 15))
        
        # Composition: Target reference
        self._target = target
        self._speed = config.HOMING_BULLET_SPEED
        self._damage = config.HOMING_BULLET_DAMAGE
    
    @property
    def target(self) -> GameObject:
        """Get current target"""
        return self._target
    
    @property
    def damage(self) -> int:
        """Get damage value"""
        return self._damage
    
    def update(self):
        """
        Homing logic: Track target and move towards it.
        Remove if target dies or goes off-screen.
        """
        if not self._target or not self._target.alive():
            self.kill()
            return
        
        # Calculate direction to target
        dx = self._target.rect.centerx - self.rect.centerx
        dy = self._target.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        
        # Move towards target (normalized direction)
        if dist != 0:
            self.rect.x += (dx / dist) * self._speed
            self.rect.y += (dy / dist) * self._speed
        
        # Remove if off-screen
        if (self.rect.top > config.HEIGHT or self.rect.bottom < 0 or 
            self.rect.left > config.WIDTH or self.rect.right < 0):
            self.kill()
