"""
Base GameObject class - Abstract base for all game entities
Demonstrates Encapsulation and Inheritance principles
"""

import pygame
import os


class GameObject(pygame.sprite.Sprite):
    """
    Abstract base class for all game entities.
    
    Encapsulation: Protected attributes with underscore prefix
    Inheritance: Base for all moving/drawable objects
    Single Responsibility: Handles sprite initialization and image management
    """
    
    def __init__(self, x: float, y: float, image_path: str, scale: tuple = (40, 40)):
        """
        Initialize a game object with position and image.
        
        Args:
            x: X position on screen
            y: Y position on screen
            image_path: Path to the sprite image
            scale: Tuple (width, height) for sprite scaling
        """
        super().__init__()
        
        # Protected attributes (convention: single underscore)
        self._x = x
        self._y = y
        self._scale = scale
        
        # Load image (with fallback to placeholder)
        self.image = self._load_image(image_path, scale)
        self.original_image = self.image.copy()
        
        # Setup rect and collision mask
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
    
    def _load_image(self, image_path: str, scale: tuple) -> pygame.Surface:
        """
        Load image with error handling.
        
        Args:
            image_path: Path to image file
            scale: Size to scale to
            
        Returns:
            pygame.Surface with loaded/placeholder image
        """
        if not os.path.exists(image_path):
            # Create magenta placeholder
            surface = pygame.Surface(scale)
            surface.fill((255, 0, 255))
            return surface
        
        try:
            image = pygame.image.load(image_path).convert_alpha()
            return pygame.transform.scale(image, scale)
        except Exception as e:
            print(f"Error loading {image_path}: {e}")
            surface = pygame.Surface(scale)
            surface.fill((255, 0, 255))
            return surface
    
    @property
    def x(self) -> float:
        """Get x position"""
        return self.rect.x
    
    @x.setter
    def x(self, value: float):
        """Set x position"""
        self.rect.x = value
        self._x = value
    
    @property
    def y(self) -> float:
        """Get y position"""
        return self.rect.y
    
    @y.setter
    def y(self, value: float):
        """Set y position"""
        self.rect.y = value
        self._y = value
    
    def get_position(self) -> tuple:
        """Get current position as tuple (x, y)"""
        return (self.rect.x, self.rect.y)
    
    def set_position(self, x: float, y: float):
        """Set position from coordinates"""
        self.rect.x = x
        self.rect.y = y
        self._x = x
        self._y = y
    
    def update(self):
        """
        Update game object state.
        Override in subclasses.
        """
        pass
