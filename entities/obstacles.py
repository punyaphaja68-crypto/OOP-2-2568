"""
Obstacle classes - Meteors and Debris
Demonstrates Inheritance and different collision behaviors
"""

import pygame
import os
import random
from entities.base import GameObject
import config


class Debris(GameObject):
    """
    Remnants from destroyed enemies.
    Floats downward and rotates. Does not deal damage.
    
    Inheritance: Extends GameObject
    """
    
    def __init__(self, x: float, y: float, image_path: str):
        """
        Initialize debris particle.
        
        Args:
            x: Starting X position
            y: Starting Y position
            image_path: Path to debris image
        """
        super().__init__(x, y, image_path, (40, 40))
        
        # Random floating motion
        self._vx = random.uniform(-2, 2)
        self._vy = random.uniform(2, 5)
        
        # Rotation
        self._rotation = 0
        self._rot_speed = random.uniform(-5, 5)
    
    def update(self):
        """Move debris with physics simulation and rotation"""
        self.rect.x += self._vx
        self.rect.y += self._vy
        
        # Rotate
        self._rotation = (self._rotation + self._rot_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self._rotation)
        
        # Update rect to maintain position during rotation
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # Remove if fallen off screen
        if self.rect.top > config.HEIGHT:
            self.kill()


class Meteor(GameObject):
    """
    Falling asteroids with different sizes and damage values.
    
    Inheritance: Extends GameObject
    Encapsulation: Size information encapsulated in object
    Single Responsibility: Handles meteor movement and rotation
    """
    
    # Class constants for meteor sizes
    SIZES = [("big1", 70), ("med1", 45), ("small1", 25), ("tiny1", 15)]
    TYPES = ["Brown", "Grey"]
    
    # Damage mapping based on size
    DAMAGE_MAP = {
        "tiny1": 0,
        "tiny2": 0,
        "small1": 1,
        "small2": 1,
        "med1": 20,
        "med2": 20,
        "big1": 25,
        "big2": 25
    }
    
    def __init__(self):
        """Initialize meteor with random size and type"""
        # Select random type and size
        meteor_type = random.choice(self.TYPES)
        size_info = random.choice(self.SIZES)
        size_tag, size_pixels = size_info
        
        # Load image
        path = os.path.join("PNG", "Meteors", f"meteor{meteor_type}_{size_tag}.png")
        super().__init__(random.randint(50, config.WIDTH - 50), -70, 
                        path, (size_pixels, size_pixels))
        
        # Encapsulation: Private attributes
        self._size_tag = size_tag
        self._speed = random.uniform(1.0, 3.0)
        self._rotation = 0
        self._rot_speed = random.uniform(-2, 2)
    
    @property
    def size_tag(self) -> str:
        """Get size identifier"""
        return self._size_tag
    
    @property
    def damage(self) -> int:
        """Get damage dealt to player"""
        return self.DAMAGE_MAP.get(self._size_tag, 0)
    
    @property
    def speed(self) -> float:
        """Get falling speed"""
        return self._speed
    
    def update(self):
        """Move meteor downward and rotate"""
        self.rect.y += self._speed
        
        # Rotate for visual effect
        self._rotation = (self._rotation + self._rot_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self._rotation)
        
        # Update rect to maintain position after rotation
        self.rect = self.image.get_rect(center=self.rect.center)
        
        # Remove if fallen off screen
        if self.rect.top > config.HEIGHT:
            self.kill()
    
    @staticmethod
    def should_damage_from_collision(size_tag: str) -> bool:
        """
        Determine if collision with this meteor size deals damage.
        
        Args:
            size_tag: Size identifier string
            
        Returns:
            True if collision should damage player
        """
        return size_tag not in ["tiny1", "tiny2", "small1", "small2"]
