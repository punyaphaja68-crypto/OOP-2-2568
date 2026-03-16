"""
Asset Manager for handling image and sound loading
Implements Dependency Injection Principle to decouple asset loading from game logic
"""

import os
import pygame


class AssetManager:
    """
    Centralized asset loading and caching system.
    Handles all image and sound resources for the game.
    
    Encapsulation: Private cache for loaded assets
    Single Responsibility: Only handles asset loading and caching
    """
    
    def __init__(self):
        """Initialize asset caches for images and sounds"""
        self._image_cache = {}
        self._sound_cache = {}
        self._default_surface = None
    
    def load_image(self, file_path: str, scale: tuple = None) -> pygame.Surface:
        """
        Load an image file with optional scaling.
        
        Args:
            file_path: Path to the image file
            scale: Tuple (width, height) for scaling, or None for original size
            
        Returns:
            Scaled pygame Surface or placeholder if file not found
        """
        # Check cache first (Optimization)
        cache_key = (file_path, scale)
        if cache_key in self._image_cache:
            return self._image_cache[cache_key]
        
        # Load image
        if not os.path.exists(file_path):
            # Return placeholder surface if file not found
            if scale:
                placeholder = pygame.Surface(scale)
                placeholder.fill((255, 0, 255))  # Magenta = missing asset
            else:
                placeholder = pygame.Surface((40, 40))
                placeholder.fill((255, 0, 255))
            self._image_cache[cache_key] = placeholder
            return placeholder
        
        try:
            image = pygame.image.load(file_path).convert_alpha()
            if scale:
                image = pygame.transform.scale(image, scale)
            self._image_cache[cache_key] = image
            return image
        except Exception as e:
            print(f"Error loading image {file_path}: {e}")
            if scale:
                placeholder = pygame.Surface(scale)
            else:
                placeholder = pygame.Surface((40, 40))
            placeholder.fill((255, 0, 255))
            self._image_cache[cache_key] = placeholder
            return placeholder
    
    def load_sound(self, folder: str, filename: str) -> pygame.mixer.Sound | None:
        """
        Load a sound file safely.
        
        Args:
            folder: Folder name containing the sound
            filename: Name of the sound file
            
        Returns:
            pygame.mixer.Sound object or None if file not found
        """
        path = os.path.join(folder, filename)
        
        # Check cache first
        if path in self._sound_cache:
            return self._sound_cache[path]
        
        if not os.path.exists(path):
            self._sound_cache[path] = None
            return None
        
        try:
            sound = pygame.mixer.Sound(path)
            self._sound_cache[path] = sound
            return sound
        except Exception as e:
            print(f"Error loading sound {path}: {e}")
            self._sound_cache[path] = None
            return None
    
    def load_background(self, filename: str, screen_size: tuple) -> pygame.Surface:
        """
        Load and scale background image to screen size.
        
        Args:
            filename: Background image filename
            screen_size: Tuple (width, height) of screen
            
        Returns:
            Scaled pygame Surface
        """
        bg_path = os.path.join("Backgrounds", filename)
        image = self.load_image(bg_path)
        if image:
            image = image.convert()  # Optimize for blitting
            return pygame.transform.scale(image, screen_size)
        return pygame.Surface(screen_size)
    
    def clear_cache(self):
        """Clear all cached assets (use when memory is low)"""
        self._image_cache.clear()
        self._sound_cache.clear()
