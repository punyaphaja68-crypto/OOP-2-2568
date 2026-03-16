"""
Enemy classes - Various enemy types with different behaviors
Demonstrates Inheritance and Polymorphism
"""

import pygame
import os
import random
from entities.base import GameObject
from entities.projectiles import Bullet, HomingBullet
import config


class EnemyShip(GameObject):
    """
    Standard enemy spacecraft with different color variants and behaviors.
    
    Inheritance: Extends GameObject
    Polymorphism: Different colors = different movement patterns
    Encapsulation: Private attributes for state management
    """
    
    COLORS = ["Red", "Blue", "Green", "Orange", "Black"]
    
    # Color-specific behavior settings
    COLOR_BEHAVIORS = {
        "Red": {"speed": 2, "horizontal_mode": "chase"},
        "Blue": {"speed": 2, "horizontal_mode": "wander"},
        "Green": {"speed": 2, "horizontal_mode": "none"},
        "Orange": {"speed": 2, "horizontal_mode": "none"},
        "Black": {"speed": 4, "horizontal_mode": "chase"}
    }
    
    def __init__(self, score: int, target_player: GameObject):
        """
        Initialize enemy ship.
        
        Args:
            score: Current game score (used for difficulty)
            target_player: Reference to player for targeting
        """
        self._color = random.choice(self.COLORS)
        path = os.path.join("PNG", "Enemies", f"enemy{self._color}1.png")
        super().__init__(random.randint(50, config.WIDTH - 50), -50, path, (50, 40))
        
        # Composition: Target reference
        self._target = target_player
        
        # Encapsulation: Private attributes
        behavior = self.COLOR_BEHAVIORS[self._color]
        self._speed = behavior["speed"]
        self._horizontal_mode = behavior["horizontal_mode"]
        self._vx = 0
        self._last_shot = pygame.time.get_ticks()
        self._shoot_cooldown = 2000  # milliseconds
    
    @property
    def color(self) -> str:
        """Get enemy color"""
        return self._color
    
    @property
    def speed(self) -> float:
        """Get speed"""
        return self._speed
    
    def update(self, bullet_group: pygame.sprite.Group, all_sprites: pygame.sprite.Group):
        """
        Update enemy position and fire bullets.
        
        Args:
            bullet_group: Group to add bullets to
            all_sprites: All sprite group for rendering
        """
        now = pygame.time.get_ticks()
        
        # Horizontal movement based on color
        if self._horizontal_mode == "chase":
            # Red and Black: Chase player
            if self.rect.centerx < self._target.rect.centerx:
                self.rect.x += 1
            else:
                self.rect.x -= 1
        elif self._horizontal_mode == "wander":
            # Blue: Random wander
            if self._vx == 0:
                self._vx = random.choice([-1, 0, 1])
            self.rect.x += self._vx
        
        # Vertical movement
        self.rect.y += self._speed
        
        # Shooting behavior
        if now - self._last_shot > self._shoot_cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.bottom, 
                          config.BOSS_BULLET_SPEED, "red", 
                          damage=config.ENEMY_SHIP_DAMAGE)
            all_sprites.add(bullet)
            bullet_group.add(bullet)
            self._last_shot = now
        
        # Remove if off-screen
        if self.rect.top > config.HEIGHT:
            self.kill()


class UFOEnemy(GameObject):
    """
    UFO-type enemy with different colors and higher damage bullets.
    
    Inheritance: Extends GameObject
    Composition: Contains target reference
    """
    
    COLORS = ["Blue", "Green", "Red", "Yellow"]
    
    def __init__(self, target: GameObject):
        """
        Initialize UFO enemy.
        
        Args:
            target: Reference to player for targeting
        """
        self._color = random.choice(self.COLORS)
        path = os.path.join("PNG", f"ufo{self._color}.png")
        super().__init__(random.randint(50, config.WIDTH - 50), -50, path, (45, 45))
        
        # Composition: Target reference
        self._target = target
        
        # Encapsulation
        self._speed = 2
        self._last_shot = pygame.time.get_ticks()
        self._shoot_cooldown = 2000
    
    @property
    def color(self) -> str:
        """Get UFO color"""
        return self._color
    
    def update(self, bullet_group: pygame.sprite.Group, all_sprites: pygame.sprite.Group):
        """
        Update UFO position and fire bullets.
        
        Args:
            bullet_group: Group to add bullets to
            all_sprites: All sprite group for rendering
        """
        now = pygame.time.get_ticks()
        
        # Chase player horizontally
        if self.rect.centerx < self._target.rect.centerx:
            self.rect.x += 1
        elif self.rect.centerx > self._target.rect.centerx:
            self.rect.x -= 1
        
        # Vertical movement
        self.rect.y += self._speed
        
        # Shooting (higher damage than regular enemies)
        if now - self._last_shot > self._shoot_cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.bottom, 
                          config.UFO_BULLET_SPEED, "red", 
                          damage=config.ENEMY_UFO_DAMAGE)
            all_sprites.add(bullet)
            bullet_group.add(bullet)
            self._last_shot = now
        
        # Remove if off-screen
        if self.rect.top > config.HEIGHT:
            self.kill()


class BigUFOBoss(GameObject):
    """
    Boss enemy - Large UFO that doesn't move, fires homing bullets.
    Spawns after reaching score 100.
    
    Inheritance: Extends GameObject
    Composition: Contains target reference
    Health Management: Has HP system
    """
    
    def __init__(self, target: GameObject):
        """
        Initialize boss.
        
        Args:
            target: Reference to player for tracking
        """
        path = os.path.join("PNG", "ufoRed.png")
        super().__init__(config.WIDTH // 2, 120, path, (150, 135))
        
        # Composition: Target reference
        self._target = target
        
        # Encapsulation
        self._health = config.BOSS_MAX_HEALTH
        self._max_health = config.BOSS_MAX_HEALTH
        self._last_shot = pygame.time.get_ticks()
        self._shoot_cooldown = config.BOSS_SPAWN_BULLET_COOLDOWN
    
    @property
    def health(self) -> int:
        """Get current health"""
        return self._health
    
    @health.setter
    def health(self, value: int):
        """Set health (clamped to 0 minimum)"""
        self._health = max(0, value)
    
    @property
    def is_alive(self) -> bool:
        """Check if boss is still alive"""
        return self._health > 0
    
    def update(self, bullet_group: pygame.sprite.Group, all_sprites: pygame.sprite.Group):
        """
        Update boss behavior - fire homing bullets at target.
        
        Args:
            bullet_group: Group to add bullets to
            all_sprites: All sprite group for rendering
        """
        now = pygame.time.get_ticks()
        
        # Fire homing bullets
        if now - self._last_shot > self._shoot_cooldown:
            bullet = HomingBullet(self.rect.centerx, self.rect.bottom, self._target)
            all_sprites.add(bullet)
            bullet_group.add(bullet)
            self._last_shot = now
    
    def draw_hp(self, surface: pygame.Surface):
        """
        Draw health bar above boss.
        
        Args:
            surface: Surface to draw on
        """
        bar_width = 200
        health_percentage = max(0, self._health / self._max_health)
        filled_width = bar_width * health_percentage
        
        # Red health bar
        pygame.draw.rect(surface, (255, 0, 0), 
                        (config.WIDTH // 2 - 100, 20, filled_width, 15))
        # White border
        pygame.draw.rect(surface, (255, 255, 255), 
                        (config.WIDTH // 2 - 100, 20, bar_width, 15), 2)
