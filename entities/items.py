"""
Item/Power-up classes
Demonstrates Composition and Encapsulation
"""

import pygame
import os
import random
from entities.base import GameObject
import config


class Pill(GameObject):
    """
    Power-up item that falls from the sky.
    Types: Shield, Health, Speed Boost, Star upgrades
    
    Encapsulation: Private item properties
    Composition: Contains color and type data
    """
    
    # Item type definitions (Class constants)
    ITEM_TYPES = {
        "shield_gold": ("gold", (25, 25)),
        "speed": ("blue", (25, 25)),
        "star_bronze": ("bronze", (25, 25)),
        "star_silver": ("silver", (25, 25)),
        "star_gold": ("gold", (25, 25)),
        "health": ("green", (25, 25))
    }
    
    def __init__(self, color: str, item_type: str = "pill", custom_path: str = None):
        """
        Initialize power-up item.
        
        Args:
            color: Color identifier (gold, blue, bronze, etc)
            item_type: Type of item (affects behavior on pickup)
            custom_path: Custom image path override
        """
        # Determine image path
        path = custom_path if custom_path else os.path.join("PNG", "Power-ups", f"pill_{color}.png")
        
        # Start at random top position
        super().__init__(random.randint(50, config.WIDTH - 50), -50, path, (25, 25))
        
        # Encapsulation: Private attributes
        self._color = color
        self._item_type = item_type
        self._speed = 2
    
    @property
    def color(self) -> str:
        """Get item color"""
        return self._color
    
    @property
    def item_type(self) -> str:
        """Get item type"""
        return self._item_type
    
    @property
    def speed(self) -> float:
        """Get falling speed"""
        return self._speed
    
    def update(self):
        """Move item downward and remove if off-screen"""
        self.rect.y += self._speed
        
        # Remove if fallen off bottom
        if self.rect.top > config.HEIGHT:
            self.kill()
    
    @staticmethod
    def create_random() -> 'Pill':
        """
        Factory method: Create random power-up based on probability rates.
        
        Returns:
            Randomly generated Pill instance
        """
        r = random.random()
        
        if r < 0.1:  # 10%
            return Pill("gold", "shield_gold", 
                       os.path.join("PNG", "Power-ups", "shield_gold.png"))
        elif r < 0.2:  # 10%
            return Pill("blue", "speed", 
                       os.path.join("PNG", "Power-ups", "bolt_gold.png"))
        elif r < 0.4:  # 20%
            return Pill("bronze", "star_bronze", 
                       os.path.join("PNG", "Power-ups", "star_bronze.png"))
        elif r < 0.5:  # 10%
            return Pill("silver", "star_silver", 
                       os.path.join("PNG", "Power-ups", "star_silver.png"))
        elif r < 0.6:  # 10%
            return Pill("gold", "star_gold", 
                       os.path.join("PNG", "Power-ups", "star_gold.png"))
        else:  # 40%
            return Pill(random.choice(["green", "blue"]))
