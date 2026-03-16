"""
Game Engine - Main game loop and state management
Demonstrates Composition, Dependency Injection, and Single Responsibility Principle
"""

import pygame
import random
import math
import os

import config
from core.asset_manager import AssetManager
from entities.player import Player
from entities.enemies import EnemyShip, UFOEnemy, BigUFOBoss
from entities.obstacles import Meteor, Debris
from entities.items import Pill
from entities.projectiles import Bullet


class GameEngine:
    """
    Main game engine handling game loop, collision detection, and state management.
    
    Composition: Uses AssetManager, Contains sprite groups, Manages all game entities
    Dependency Injection: AssetManager passed in (allows for testing/substitution)
    Single Responsibility: Game loop coordination (not handling individual entity logic)
    """
    
    def __init__(self, asset_manager: AssetManager = None):
        """
        Initialize game engine.
        
        Args:
            asset_manager: AssetManager instance (creates new if None)
        """
        pygame.init()
        pygame.mixer.init()
        
        # Display setup
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Rocket Evolution - Miguel Edition")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 48, bold=True)
        
        # Asset management (Dependency Injection)
        self.asset_manager = asset_manager or AssetManager()
        
        # Background
        self._bg_list = ["black.png", "blue.png", "darkPurple.png", "purple.png"]
        self.bg_image = self._load_background("purple.png")
        self._last_bg_score = 0
        
        # Sound effects
        self._sfx = self._load_sounds()
        
        # Game state
        self.player = None
        self.boss = None
        self.score = 0
    
    def _load_background(self, filename: str) -> pygame.Surface:
        """Load and scale background image"""
        return self.asset_manager.load_background(filename, (config.WIDTH, config.HEIGHT))
    
    def _load_sounds(self) -> dict:
        """Load all game sounds"""
        sfx = {}
        for key, (folder, filename) in config.SOUND_FILES.items():
            sfx[key] = self.asset_manager.load_sound(folder, filename)
        return sfx
    
    def reset_game(self):
        """Reset all game state for a new round"""
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()
        self.pills = pygame.sprite.Group()
        self.p_bullets = pygame.sprite.Group()  # Player bullets
        self.e_bullets = pygame.sprite.Group()  # Enemy bullets
        
        # Create player
        self.player = Player(self.p_bullets, self.all_sprites, self._sfx)
        self.all_sprites.add(self.player)
        
        # Reset game state
        self.boss = None
        self.score = 0
        self._last_bg_score = 0
        self.start_ticks = pygame.time.get_ticks()
        
        # Play shield sound
        if self._sfx.get('shield'):
            self._sfx['shield'].play()
    
    def spawn_boss_guards(self):
        """Spawn 8 UFO guards around the boss"""
        for i in range(config.BOSS_GUARDS_COUNT):
            angle = i * (360 / config.BOSS_GUARDS_COUNT)
            rad = math.radians(angle)
            dist = 160
            
            gx = config.WIDTH // 2 + math.cos(rad) * dist
            gy = 120 + math.sin(rad) * dist
            
            ufo = UFOEnemy(self.player)
            ufo.rect.center = (gx, gy)
            ufo._speed = 0  # Stationary guards
            
            self.enemies.add(ufo)
            self.all_sprites.add(ufo)
    
    def spawn_debris(self, pos: tuple):
        """
        Spawn debris particles at position.
        
        Args:
            pos: (x, y) position to spawn debris
        """
        debris_types = random.sample([1, 2, 3], 2)
        for debris_type in debris_types:
            path = os.path.join("PNG", "Damage", f"playerShip1_damage{debris_type}.png")
            debris = Debris(pos[0], pos[1], path)
            self.all_sprites.add(debris)
    
    def try_spawn_item(self):
        """
        Attempt to spawn a random power-up item.
        Implements Factory pattern via Pill.create_random()
        """
        if random.random() < config.ITEM_SPAWN_PROBABILITY:
            item = Pill.create_random()
            
            # Avoid spawning inside meteors (collision detection)
            collision = True
            attempts = 0
            while collision and attempts < 10:
                item.rect.x = random.randint(50, config.WIDTH - 50)
                collision = pygame.sprite.spritecollideany(item, self.meteors)
                attempts += 1
            
            self.pills.add(item)
            self.all_sprites.add(item)
    
    def try_spawn_enemy(self):
        """Attempt to spawn a new enemy ship"""
        if (len(self.enemies) < config.MAX_ENEMIES and 
            random.random() < config.ENEMY_SPAWN_PROBABILITY and 
            not self.boss):
            enemy = EnemyShip(self.score, self.player)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
    
    def try_spawn_meteor(self):
        """Attempt to spawn a new meteor"""
        if (len(self.meteors) < config.MAX_METEORS and 
            random.random() < config.METEOR_SPAWN_PROBABILITY):
            meteor = Meteor()
            self.meteors.add(meteor)
            self.all_sprites.add(meteor)
    
    def try_spawn_boss(self):
        """Spawn boss when score reaches threshold"""
        if self.score >= config.BOSS_SPAWN_SCORE and not self.boss:
            self.boss = BigUFOBoss(self.player)
            self.all_sprites.add(self.boss)
            self.spawn_boss_guards()
    
    def update_background(self):
        """Change background when score milestone reached"""
        if self.score > 0 and self.score // config.BACKGROUND_CHANGE_INTERVAL > self._last_bg_score // config.BACKGROUND_CHANGE_INTERVAL:
            self.bg_image = self._load_background(random.choice(self._bg_list))
            self._last_bg_score = self.score
    
    def handle_collisions(self):
        """
        Handle all collision detection and damage.
        Single Responsibility: Only collision logic
        """
        now = pygame.time.get_ticks()
        
        # --- Enemy kills ---
        hits = pygame.sprite.groupcollide(self.enemies, self.p_bullets, True, True)
        for _ in hits:
            self.score += config.SCORE_PER_ENEMY_KILL
        
        # Bullets collide with meteors (no destruction)
        pygame.sprite.groupcollide(self.p_bullets, self.meteors, False, False)
        
        # --- Boss logic ---
        if self.boss:
            self.boss.update(self.e_bullets, self.all_sprites)
            boss_hits = pygame.sprite.spritecollide(self.boss, self.p_bullets, True)
            for bullet in boss_hits:
                self.boss.health -= bullet.damage
                if self.boss.health <= 0:
                    if self._sfx.get('boss_death'):
                        self._sfx['boss_death'].play()
                    self.spawn_debris(self.boss.rect.center)
                    self.boss.kill()
                    self.boss = None
                    self.score += config.SCORE_PER_BOSS_KILL
        
        # --- Item pickup ---
        for item in pygame.sprite.spritecollide(self.player, self.pills, True):
            self._apply_item_effect(item)
        
        # --- Player damage (only when not in spawn shield or gold shield) ---
        if (now - self.player._spawn_time > config.PLAYER_SPAWN_SHIELD_DURATION and 
            not self.player.shield_gold_active):
            self._handle_player_damage()
    
    def _apply_item_effect(self, item: Pill):
        """
        Apply power-up effects to player.
        
        Args:
            item: Pill object collected
        """
        if item.item_type == "shield_gold":
            self.player.activate_shield_gold()
        elif item.item_type == "speed":
            self.player.activate_speed_boost()
        elif "star_" in item.item_type:
            star_type = item.item_type.split("_")[1]
            self.player.add_star(star_type)
        elif item.color == "green":
            self.player.health = min(config.PLAYER_MAX_HEALTH, 
                                   self.player.health + config.PLAYER_HEALTH_RESTORE)
    
    def _handle_player_damage(self):
        """Apply damage from various sources to player"""
        # Enemy bullet hits
        enemy_bullet_hits = pygame.sprite.spritecollide(
            self.player, self.e_bullets, True, pygame.sprite.collide_mask)
        for bullet in enemy_bullet_hits:
            self.player.take_damage(bullet.damage)
        
        # Direct enemy collision
        enemy_hits = pygame.sprite.spritecollide(
            self.player, self.enemies, True, pygame.sprite.collide_mask)
        for _ in enemy_hits:
            self.player.take_damage(config.PLAYER_COLLISION_DAMAGE)
        
        # Meteor collision (size-based damage)
        meteor_hits = pygame.sprite.spritecollide(
            self.player, self.meteors, False, pygame.sprite.collide_mask)
        for meteor in meteor_hits:
            if not Meteor.should_damage_from_collision(meteor.size_tag):
                # Small/tiny meteors: minimal damage
                if "small" in meteor.size_tag:
                    self.player.take_damage(1)
                # Tiny meteors: no damage
            else:
                # Medium/big meteors: lethal
                if self._sfx.get('lose'):
                    self._sfx['lose'].play()
                return False  # Game over
        
        return True  # Still alive
    
    def render(self):
        """Render all game elements"""
        # Background
        self.screen.blit(self.bg_image, (0, 0))
        
        # All sprites
        self.all_sprites.draw(self.screen)
        
        # Boss HP bar
        if self.boss:
            self.boss.draw_hp(self.screen)
        
        # Player UI
        self.player.draw_ui(self.screen)
        
        # Score and health text
        txt = self.font.render(
            f"Score: {self.score} HP: {self.player.health}", 
            True, (255, 255, 255))
        self.screen.blit(txt, (10, 10))
        
        pygame.display.flip()
    
    def show_game_over(self, survival_time: int) -> bool:
        """
        Show game over screen and wait for restart.
        
        Args:
            survival_time: Time survived in seconds
            
        Returns:
            True if player wants to restart, False if quit
        """
        self.screen.fill((0, 0, 0))
        
        # Game over text
        game_over_txt = self.big_font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(game_over_txt, (config.WIDTH // 2 - 130, config.HEIGHT // 2 - 100))
        
        # Stats text
        stats_txt = self.font.render(
            f"Score: {self.score} | Time: {survival_time}s | Gold Stars: {self.player.total_gold_stars_collected}",
            True, (255, 255, 255))
        self.screen.blit(stats_txt, (config.WIDTH // 2 - 180, config.HEIGHT // 2 - 20))
        
        # Instructions
        restart_txt = self.font.render("Press R to restart or Q to quit", True, (200, 200, 200))
        self.screen.blit(restart_txt, (config.WIDTH // 2 - 150, config.HEIGHT // 2 + 40))
        
        pygame.display.flip()
        
        # Wait for player action
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    elif event.key == pygame.K_q:
                        return False
    
    def run(self):
        """
        Main game loop.
        Orchestrates all game systems.
        """
        while True:
            self.reset_game()
            running = True
            boss_spawned = False
            
            while running:
                now = pygame.time.get_ticks()
                survival_time = (now - self.start_ticks) // 1000
                
                # --- Handle Input ---
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                
                # --- Spawning ---
                self.try_spawn_enemy()
                self.try_spawn_meteor()
                self.try_spawn_item()
                
                # Boss spawning (one-time per round)
                if not boss_spawned:
                    self.try_spawn_boss()
                    if self.boss:
                        boss_spawned = True
                
                # --- Update ---
                self.update_background()
                self.player.update(self.score)
                self.enemies.update(self.e_bullets, self.all_sprites)
                self.meteors.update()
                self.pills.update()
                self.p_bullets.update()
                self.e_bullets.update()
                
                # --- Collision Detection ---
                self.handle_collisions()
                
                # --- Check Player Death ---
                if self.player.health <= 0:
                    if self._sfx.get('lose'):
                        self._sfx['lose'].play()
                    running = False
                
                # --- Render ---
                self.render()
                self.clock.tick(config.FPS)
            
            # Game Over screen
            if not self.show_game_over(survival_time):
                pygame.quit()
                return
