"""
Player class - Main player-controlled spacecraft
Demonstrates Encapsulation, Composition, and state management
"""

import pygame
import os
import random
from entities.base import GameObject
from entities.projectiles import Bullet
import config


class Player(GameObject):
    """
    Player-controlled spaceship with upgrade system and special abilities.
    
    Encapsulation: Private health, shield, and ability states
    Composition: Contains bullet group and sprite group references
    State Management: Tracks multiple power-up states and timers
    """
    
    # Available ship skins
    SHIP_SKINS = [f"playerShip{i}_{c}.png" for i in range(1, 4) for c in ["blue", "green", "orange", "red"]]
    
    def __init__(self, bullet_group: pygame.sprite.Group, 
                 all_sprites: pygame.sprite.Group, sfx_dict: dict):
        """
        Initialize player ship.
        
        Args:
            bullet_group: Group for player bullets
            all_sprites: All sprites group for rendering
            sfx_dict: Dictionary of sound effects
        """
        # Initial color and image
        self._color = "blue"
        path = os.path.join("PNG", f"playerShip1_{self._color}.png")
        super().__init__(config.WIDTH // 2, config.HEIGHT - 60, path, (50, 45))
        
        # Composition: References to game systems
        self._bullet_group = bullet_group
        self._all_sprites = all_sprites
        self._sfx = sfx_dict
        
        # --- Core Stats ---
        self._health = config.PLAYER_MAX_HEALTH
        self._max_health = config.PLAYER_MAX_HEALTH
        self._base_speed = 6
        self._speed = self._base_speed
        
        # --- Timing ---
        self._last_shot = pygame.time.get_ticks()
        self._spawn_time = pygame.time.get_ticks()
        
        # --- Power-up States (Timer-based) ---
        self._shield_gold_active = False
        self._shield_end = 0
        self._speed_end = 0
        self._hyper_mode_end = 0
        self._beam_laser_end = 0
        
        # --- Special Abilities ---
        self._perm_laser = False  # Permanent beam laser mode
        self._laser_style = "01"
        self._is_hyper_active = False
        self._last_regen_tick = 0
        self._regen_end = 0
        
        # --- Progression Stats ---
        self._stars = {"bronze": 0, "silver": 0, "gold": 0}
        self._total_gold_stars_collected = 0
        self._last_evolve_score = 0
        
        # --- Shield Icons ---
        self._load_shield_images()
    
    def _load_shield_images(self):
        """Load shield visual assets"""
        shield2_path = os.path.join("PNG", "Effects", "shield2.png")
        if os.path.exists(shield2_path):
            self._shield_img = pygame.transform.scale(
                pygame.image.load(shield2_path).convert_alpha(), (90, 90))
        else:
            self._shield_img = pygame.Surface((90, 90), pygame.SRCALPHA)
        
        shield1_path = os.path.join("PNG", "Effects", "shield1.png")
        if os.path.exists(shield1_path):
            self._shield_gold_img = pygame.transform.scale(
                pygame.image.load(shield1_path).convert_alpha(), (95, 95))
        else:
            self._shield_gold_img = None
    
    # --- PROPERTIES FOR ENCAPSULATION ---
    
    @property
    def health(self) -> int:
        """Get current health"""
        return self._health
    
    @health.setter
    def health(self, value: int):
        """Set health (clamped 0-max)"""
        self._health = max(0, min(value, self._max_health))
    
    @property
    def max_health(self) -> int:
        """Get max health"""
        return self._max_health
    
    @property
    def color(self) -> str:
        """Get ship color"""
        return self._color
    
    @property
    def stars(self) -> dict:
        """Get star collection"""
        return self._stars.copy()
    
    @property
    def total_gold_stars_collected(self) -> int:
        """Get total gold stars ever collected"""
        return self._total_gold_stars_collected
    
    @property
    def is_hyper_active(self) -> bool:
        """Check if hyper mode is active"""
        return self._is_hyper_active
    
    @property
    def shield_gold_active(self) -> bool:
        """Check if golden shield is active"""
        return self._shield_gold_active
    
    # --- GAMEPLAY METHODS ---
    
    def update(self, score: int):
        """
        Update player state, movement, and shooting.
        
        Args:
            score: Current game score (for evolution)
        """
        now = pygame.time.get_ticks()
        
        # --- Ship Evolution (color change at score milestones) ---
        if score > 0 and score % 100 == 0 and score != self._last_evolve_score:
            self._evolve_ship()
            self._last_evolve_score = score
        
        # --- Check hyper mode timeout ---
        if self._is_hyper_active and now > self._hyper_mode_end:
            self._is_hyper_active = False
        
        # --- Handle input and movement ---
        self._handle_movement()
        
        # --- Handle regeneration ---
        if now < self._regen_end and now - self._last_regen_tick >= 1000:
            self._health = min(self._max_health, self._health + 1)
            self._last_regen_tick = now
        
        # --- Handle shooting ---
        self._handle_shooting()
    
    def _evolve_ship(self):
        """Evolve ship color at score milestones"""
        new_ship = random.choice(self.SHIP_SKINS)
        self._color = new_ship.split('_')[1].replace('.png', '')
        ship_path = os.path.join("PNG", new_ship)
        
        if os.path.exists(ship_path):
            self.image = pygame.image.load(ship_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 45))
            self.original_image = self.image
    
    def _handle_movement(self):
        """Process keyboard input and move player"""
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        
        # Apply speed boost if active
        self._speed = self._base_speed * 1.5 if now < self._speed_end else self._base_speed
        
        # Get movement input
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        
        self.rect.x += dx * self._speed
        self.rect.y += dy * self._speed
        
        # Clamp to screen
        self.rect.clamp_ip(pygame.Rect(0, 0, config.WIDTH, config.HEIGHT))
    
    def _handle_shooting(self):
        """Process shooting input"""
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        
        if self._perm_laser:
            # Permanent laser mode (automatic)
            if now - self._last_shot > 80:
                self.shoot(is_beam=True, is_hyper=True)
                self._last_shot = now
        elif keys[pygame.K_SPACE]:
            # Manual shooting
            is_beam = now < self._beam_laser_end
            cooldown = 100 if (is_beam or self._is_hyper_active) else 300
            
            if now - self._last_shot > cooldown:
                self.shoot(is_beam)
                self._last_shot = now
    
    def shoot(self, is_beam: bool = False, is_hyper: bool = False):
        """
        Fire a bullet.
        
        Args:
            is_beam: Whether to fire a beam laser
            is_hyper: Whether this is hyper mode damage
        """
        damage = config.HYPER_MODE_DAMAGE if self._is_hyper_active else config.NORMAL_MODE_DAMAGE
        
        if is_hyper or self._is_hyper_active:
            if self._sfx.get('laser2'):
                self._sfx['laser2'].play()
            style = self._laser_style if is_hyper else "02"
            path = os.path.join("PNG", "Lasers", f"laser{self._color.capitalize()}{style}.png")
            bullet = Bullet(self.rect.centerx, self.rect.top, 
                          -config.PLAYER_HYPER_BULLET_SPEED, 
                          self._color, custom_path=path, damage=damage)
        else:
            if self._sfx.get('laser1'):
                self._sfx['laser1'].play()
            bullet = Bullet(self.rect.centerx, self.rect.top, 
                          -config.PLAYER_NORMAL_BULLET_SPEED,
                          self._color, is_beam, damage=damage)
        
        self._all_sprites.add(bullet)
        self._bullet_group.add(bullet)
    
    def take_damage(self, amount: int):
        """
        Apply damage to player.
        
        Args:
            amount: Damage amount
        """
        self._health = max(0, self._health - amount)
    
    def add_star(self, star_type: str):
        """
        Add a star and handle upgrades.
        
        Args:
            star_type: Type of star ("bronze", "silver", "gold")
        """
        if star_type not in self._stars:
            return
        
        self._stars[star_type] += 1
        
        if star_type == "gold":
            self._total_gold_stars_collected += 1
        
        # Auto-upgrade logic
        if self._stars["bronze"] >= config.STAR_UPGRADE_THRESHOLD["bronze"]:
            self._stars["bronze"] -= config.STAR_UPGRADE_THRESHOLD["bronze"]
            self._stars["silver"] += 1
        
        if self._stars["silver"] >= config.STAR_UPGRADE_THRESHOLD["silver"]:
            self._stars["silver"] -= config.STAR_UPGRADE_THRESHOLD["silver"]
            self._stars["gold"] += 1
        
        # 3 gold stars = hyper mode activation
        if self._stars["gold"] >= config.STAR_UPGRADE_THRESHOLD["gold"]:
            self._stars["gold"] -= config.STAR_UPGRADE_THRESHOLD["gold"]
            self._is_hyper_active = True
            self._hyper_mode_end = pygame.time.get_ticks() + config.HYPER_MODE_DURATION
    
    def activate_shield_gold(self):
        """Activate golden shield protection"""
        now = pygame.time.get_ticks()
        self._shield_gold_active = True
        self._shield_end = now + config.SHIELD_GOLD_DURATION
    
    def activate_speed_boost(self):
        """Activate speed boost"""
        now = pygame.time.get_ticks()
        self._speed_end = now + config.SPEED_BOOST_DURATION
    
    def activate_beam_laser(self):
        """Activate beam laser weapon"""
        now = pygame.time.get_ticks()
        self._beam_laser_end = now + config.HYPER_MODE_DURATION
    
    def draw_ui(self, surface: pygame.Surface):
        """
        Draw player UI elements (shields, health bar).
        
        Args:
            surface: Surface to draw on
        """
        now = pygame.time.get_ticks()
        
        # Draw shields
        if self._shield_gold_active and now < self._shield_end:
            if self._shield_gold_img:
                surface.blit(self._shield_gold_img, 
                           self._shield_gold_img.get_rect(center=self.rect.center))
        elif now - self._spawn_time < config.PLAYER_SPAWN_SHIELD_DURATION:
            surface.blit(self._shield_img, 
                       self._shield_img.get_rect(center=self.rect.center))
        
        # Draw health bar
        bar_width = 50
        fill_amount = (max(0, self._health) / self._max_health) * bar_width
        pygame.draw.rect(surface, (0, 255, 0), 
                        (self.rect.x, self.rect.y - 15, fill_amount, 6))
        pygame.draw.rect(surface, (255, 255, 255), 
                        (self.rect.x, self.rect.y - 15, bar_width, 6), 1)
