import pygame
import random
import os
import math

# --- Configuration ---
WIDTH, HEIGHT = 800, 600
FPS = 60

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, scale=(40, 40)):
        super().__init__()
        if not os.path.exists(image_path):
            self.image = pygame.Surface(scale); self.image.fill((255, 0, 255)) 
        else:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, scale)
        self.original_image = self.image 
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

class Bullet(GameObject):
    def __init__(self, x, y, speed, color_type="blue", is_beam=False, damage=5, custom_path=None):
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
        self.speed = speed
        self.damage = damage
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > HEIGHT: self.kill()

class Debris(GameObject):
    """เศษซากยานที่ลอยผ่านไปโดยทำดาเมจ"""
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path, (40, 40))
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(2, 5)
        self.rot_speed = random.uniform(-5, 5)
        self.rotation = 0

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.rotation = (self.rotation + self.rot_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        if self.rect.top > HEIGHT: self.kill()

class HomingBullet(GameObject):
    """กระสุนล็อคเป้าจากบอส ดาเมจ 15"""
    def __init__(self, x, y, target):
        path = os.path.join("PNG", "Lasers", "laserRed08.png")
        super().__init__(x, y, path, (15, 15))
        self.target = target
        self.speed = 3.5
        self.damage = 15 # ปรับจาก 20 เป็น 15 ตามที่ Miguel ต้องการ

    def update(self):
        # ระบบล็อกเป้า (Homing logic)
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.rect.x += (dx / dist) * self.speed
            self.rect.y += (dy / dist) * self.speed
        
        # ลบกระสุนเมื่อออกนอกจอ
        if self.rect.top > HEIGHT or self.rect.bottom < 0 or self.rect.left > WIDTH or self.rect.right < 0: 
            self.kill()

class Pill(GameObject):
    def __init__(self, color, item_type="pill", custom_path=None):
        self.color = color
        self.item_type = item_type
        path = custom_path if custom_path else os.path.join("PNG", "Power-ups", f"pill_{color}.png")
        super().__init__(random.randint(50, WIDTH-50), -50, path, (25, 25))
        self.speed = 2
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT: self.kill()

class Player(GameObject):
    def __init__(self, bullet_group, all_sprites, sfx_dict):
        self.all_ships = [f"playerShip{i}_{c}.png" for i in range(1,4) for c in ["blue", "green", "orange", "red"]]
        self.color = "blue"
        path = os.path.join("PNG", f"playerShip1_{self.color}.png")
        super().__init__(WIDTH//2, HEIGHT-60, path, (50, 45))
        self.base_speed = 6
        self.speed = self.base_speed
        self.bullet_group = bullet_group
        self.all_sprites = all_sprites
        self.sfx = sfx_dict
        self.health = 100 
        self.max_health = 100
        self.last_shot = pygame.time.get_ticks()
        self.last_evolve_score = 0
        self.spawn_time = pygame.time.get_ticks()
        self.shield_gold_active = False
        self.shield_end = 0
        self.perm_laser = False
        self.laser_style = "01"
        self.stars = {"bronze": 0, "silver": 0, "gold": 0}
        self.total_gold_stars_collected = 0 
        self.is_hyper_active = False
        self.hyper_damage_end = 0
        self.speed_end = 0
        self.regen_end = 0; self.beam_end = 0; self.last_regen_tick = 0
        
        shield2_path = os.path.join("PNG", "Effects", "shield2.png")
        self.shield_img = pygame.transform.scale(pygame.image.load(shield2_path), (90, 90)) if os.path.exists(shield2_path) else pygame.Surface((90, 90), pygame.SRCALPHA)
        shield1_path = os.path.join("PNG", "Effects", "shield1.png")
        self.shield_gold_img = pygame.transform.scale(pygame.image.load(shield1_path), (95, 95)) if os.path.exists(shield1_path) else None

    def update(self, score):
        now = pygame.time.get_ticks()
        if score > 0 and score % 100 == 0 and score != self.last_evolve_score:
            new_ship = random.choice(self.all_ships)
            self.color = new_ship.split('_')[1].replace('.png', '')
            ship_path = os.path.join("PNG", new_ship)
            if os.path.exists(ship_path):
                self.image = pygame.image.load(ship_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 45))
                self.original_image = self.image
            self.last_evolve_score = score

        if self.is_hyper_active and now > self.hyper_damage_end:
            self.is_hyper_active = False

        keys = pygame.key.get_pressed()
        self.speed = self.base_speed * 1.5 if now < self.speed_end else self.base_speed
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        if now < self.regen_end and now - self.last_regen_tick >= 1000:
            self.health = min(self.max_health, self.health + 1)
            self.last_regen_tick = now

        if self.perm_laser:
            if now - self.last_shot > 80:
                self.shoot(is_beam=True, is_hyper=True); self.last_shot = now
        elif keys[pygame.K_SPACE]:
            is_beam = now < self.beam_end
            if now - self.last_shot > (100 if is_beam or self.is_hyper_active else 300):
                self.shoot(is_beam); self.last_shot = now

    def shoot(self, is_beam, is_hyper=False):
        dmg = 50 if self.is_hyper_active else 5
        if is_hyper or self.is_hyper_active:
            if self.sfx['laser2']: self.sfx['laser2'].play()
            style = self.laser_style if is_hyper else "02"
            path = os.path.join("PNG", "Lasers", f"laser{self.color.capitalize()}{style}.png")
            b = Bullet(self.rect.centerx, self.rect.top, -15, self.color, custom_path=path, damage=dmg)
        else:
            if self.sfx['laser1']: self.sfx['laser1'].play()
            b = Bullet(self.rect.centerx, self.rect.top, -12, self.color, is_beam, damage=dmg)
        self.all_sprites.add(b); self.bullet_group.add(b)

    def add_star(self, s_type):
        self.stars[s_type] += 1
        if s_type == "gold": self.total_gold_stars_collected += 1
        if self.stars["bronze"] >= 3: self.stars["bronze"] -= 3; self.stars["silver"] += 1
        if self.stars["silver"] >= 5: self.stars["silver"] -= 5; self.stars["gold"] += 1
        if self.stars["gold"] >= 3:
            self.stars["gold"] -= 3
            self.is_hyper_active = True
            self.hyper_damage_end = pygame.time.get_ticks() + 30000 

    def draw_ui(self, surface):
        now = pygame.time.get_ticks()
        if self.shield_gold_active and now < self.shield_end:
            if self.shield_gold_img: surface.blit(self.shield_gold_img, self.shield_gold_img.get_rect(center=self.rect.center))
        elif now - self.spawn_time < 3000:
            surface.blit(self.shield_img, self.shield_img.get_rect(center=self.rect.center))
        fill = (max(0, self.health) / self.max_health) * 50
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 15, fill, 6))
        pygame.draw.rect(surface, (255, 255, 255), (self.rect.x, self.rect.y - 15, 50, 6), 1)

class EnemyShip(GameObject):
    def __init__(self, score, target_player):
        self.color = random.choice(["Red", "Blue", "Green", "Orange", "Black"])
        path = os.path.join("PNG", "Enemies", f"enemy{self.color}1.png")
        super().__init__(random.randint(50, WIDTH-50), -50, path, (50, 40))
        self.target = target_player
        self.speed = 4 if self.color == "Black" else 2
        self.last_shot = pygame.time.get_ticks()
        self.vx = 0

    def update(self, bullet_group, all_sprites):
        now = pygame.time.get_ticks()
        if self.color == "Red":
            if self.rect.centerx < self.target.rect.centerx: self.rect.x += 1
            else: self.rect.x -= 1
        elif self.color == "Blue" and self.vx == 0:
            self.vx = random.choice([-1, 0, 1])
        self.rect.x += self.vx
        self.rect.y += self.speed
        if now - self.last_shot > 2000:
            b = Bullet(self.rect.centerx, self.rect.bottom, 6, "red", damage=5)
            all_sprites.add(b); bullet_group.add(b); self.last_shot = now
        if self.rect.top > HEIGHT: self.kill()

class UFOEnemy(GameObject):
    def __init__(self, target):
        color = random.choice(["Blue", "Green", "Red", "Yellow"])
        path = os.path.join("PNG", f"ufo{color}.png")
        super().__init__(random.randint(50, WIDTH-50), -50, path, (45, 45))
        self.target = target
        self.speed = 2
        self.last_shot = pygame.time.get_ticks()
    def update(self, bullet_group, all_sprites):
        now = pygame.time.get_ticks()
        if self.rect.centerx < self.target.rect.centerx: self.rect.x += 1
        elif self.rect.centerx > self.target.rect.centerx: self.rect.x -= 1
        self.rect.y += self.speed
        if now - self.last_shot > 2000:
            b = Bullet(self.rect.centerx, self.rect.bottom, 5, "red", damage=10)
            all_sprites.add(b); bullet_group.add(b); self.last_shot = now
        if self.rect.top > HEIGHT: self.kill()

class BigUFOBoss(GameObject):
    """บอส UFO ลำใหญ่ ไม่ขยับ ยิงกระสุนล็อคเป้า สร้างดาเมจหนัก 20 ต่อโดน และมี HP 500"""
    def __init__(self, target):
        path = os.path.join("PNG", "ufoRed.png")
        super().__init__(WIDTH//2, 120, path, (150, 135)) 
        self.health = 500
        self.target = target
        self.last_shot = pygame.time.get_ticks()

    def update(self, bullet_group, all_sprites):
        now = pygame.time.get_ticks()
        if now - self.last_shot > 2500:
            b = HomingBullet(self.rect.centerx, self.rect.bottom, self.target)
            all_sprites.add(b); bullet_group.add(b)
            self.last_shot = now

    def draw_hp(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (WIDTH//2 - 100, 20, (self.health/500)*200, 15))
        pygame.draw.rect(surface, (255, 255, 255), (WIDTH//2 - 100, 20, 200, 15), 2)

class Meteor(GameObject):
    def __init__(self):
        m_type = random.choice(["Brown", "Grey"])
        # เพิ่มการเก็บ key ของ size ไว้ใน self.size_tag
        size_info = random.choice([("big1", 70), ("med1", 45), ("small1", 25), ("tiny1", 15)])
        self.size_tag = size_info[0] # เก็บค่า 'big1', 'med1', 'small1', หรือ 'tiny1'
        
        path = os.path.join("PNG", "Meteors", f"meteor{m_type}_{self.size_tag}.png")
        super().__init__(random.randint(50, WIDTH-50), -70, path, (size_info[1], size_info[1]))
        self.speed = random.uniform(1.0, 3.0)
        self.rotation, self.rot_speed = 0, random.uniform(-2, 2)
    def update(self):
        self.rect.y += self.speed
        self.rotation = (self.rotation + self.rot_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.rect.top > HEIGHT: self.kill()

class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Rocket Evolution - Miguel Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.bg_list = ["black.png", "blue.png", "darkPurple.png", "purple.png"]
        self.bg_image = self.load_bg("purple.png")
        self.sfx = {
            'laser1': self.load_sound("Bonus", "sfx_laser1.ogg"),
            'laser2': self.load_sound("Bonus", "sfx_laser2.ogg"),
            'lose': self.load_sound("Bonus", "sfx_lose.ogg"),
            'shield': self.load_sound("Bonus", "sfx_shieldUp.ogg"),
            'boss_death': self.load_sound("Bonus", "sfx_twoTone.ogg")
        }

    def load_bg(self, name):
        bg = pygame.image.load(os.path.join("Backgrounds", name)).convert()
        return pygame.transform.scale(bg, (WIDTH, HEIGHT))

    def load_sound(self, folder, file):
        path = os.path.join(folder, file)
        return pygame.mixer.Sound(path) if os.path.exists(path) else None
        
    def reset_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemies, self.meteors, self.pills = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
        self.p_bullets, self.e_bullets = pygame.sprite.Group(), pygame.sprite.Group()
        self.player = Player(self.p_bullets, self.all_sprites, self.sfx) 
        self.all_sprites.add(self.player)
        self.boss, self.score, self.last_bg_score = None, 0, 0
        self.start_ticks = pygame.time.get_ticks()
        if self.sfx['shield']: self.sfx['shield'].play()

    def spawn_boss_guards(self):
        for i in range(8):
            angle = i * (360 / 8)
            rad = math.radians(angle)
            dist = 160
            gx = WIDTH//2 + math.cos(rad) * dist
            gy = 120 + math.sin(rad) * dist
            u = UFOEnemy(self.player)
            u.rect.center = (gx, gy)
            u.speed = 0 
            self.enemies.add(u); self.all_sprites.add(u)

    def spawn_debris(self, pos):
        """สร้างเศษซาก 2 ประเภทแบบไม่ซ้ำและไม่ทำดาเมจและหายไปเอง"""
        types = random.sample([1, 2, 3], 2)
        for t in types:
            path = os.path.join("PNG", "Damage", f"playerShip1_damage{t}.png")
            d = Debris(pos[0], pos[1], path)
            self.all_sprites.add(d)

    def run(self):
        while True:
            self.reset_game(); running = True; boss_spawned = False; final_survival_time = 0
            while running:
                now = pygame.time.get_ticks()
                survival_time = (now - self.start_ticks) // 1000
                final_survival_time = survival_time
                if self.score > 0 and self.score // 200 > self.last_bg_score // 200:
                    self.bg_image = self.load_bg(random.choice(self.bg_list))
                    self.last_bg_score = self.score

                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); return

                if self.score >= 100 and not self.boss and not boss_spawned:
                    self.boss = BigUFOBoss(self.player); self.all_sprites.add(self.boss)
                    self.spawn_boss_guards(); boss_spawned = True

                if len(self.enemies) < 3 and random.random() < 0.01 and not self.boss:
                    u = EnemyShip(self.score, self.player); self.enemies.add(u); self.all_sprites.add(u)
                if len(self.meteors) < 12 and random.random() < 0.05: 
                    m = Meteor(); self.meteors.add(m); self.all_sprites.add(m)
                
                if random.random() < 0.008:
                    r = random.random()
                    if r < 0.1: item = Pill("gold", "shield_gold", os.path.join("PNG", "Power-ups", "shield_gold.png"))
                    elif r < 0.2: item = Pill("blue", "speed", os.path.join(1"PNG", "Power-ups", "bolt_gold.png"))
                    elif r < 0.4: item = Pill("bronze", "star_bronze", os.path.join("PNG", "Power-ups", "star_bronze.png"))
                    elif r < 0.5: item = Pill("silver", "star_silver", os.path.join("PNG", "Power-ups", "star_silver.png"))
                    elif r < 0.6: item = Pill("gold", "star_gold", os.path.join("PNG", "Power-ups", "star_gold.png"))
                    else: item = Pill(random.choice(["green", "blue"]))
                    collision = True; attempts = 0
                    while collision and attempts < 10:
                        item.rect.x = random.randint(50, WIDTH-50)
                        collision = pygame.sprite.spritecollideany(item, self.meteors)
                        attempts += 1
                    self.pills.add(item); self.all_sprites.add(item)

                self.player.update(self.score)
                self.enemies.update(self.e_bullets, self.all_sprites)
                self.meteors.update(); self.pills.update(); self.p_bullets.update(); self.e_bullets.update()

                hits = pygame.sprite.groupcollide(self.enemies, self.p_bullets, True, True)
                for enemy in hits: self.score += 10
                pygame.sprite.groupcollide(self.p_bullets, self.meteors, False, False)
                
                if self.boss:
                    self.boss.update(self.e_bullets, self.all_sprites)
                    boss_hits = pygame.sprite.spritecollide(self.boss, self.p_bullets, True)
                    for b in boss_hits:
                        self.boss.health -= b.damage
                        if self.boss.health <= 0:
                            if self.sfx['boss_death']: self.sfx['boss_death'].play()
                            self.spawn_debris(self.boss.rect.center)
                            self.boss.kill(); self.boss = None; self.score += 500

                for p in pygame.sprite.spritecollide(self.player, self.pills, True):
                    if p.item_type == "shield_gold": self.player.shield_gold_active, self.player.shield_end = True, now + 7000
                    elif p.item_type == "speed": self.player.speed_end = now + 5000
                    elif "star_" in p.item_type: self.player.add_star(p.item_type.split("_")[1])
                    elif p.color == "green": self.player.health = min(100, self.player.health + 20)

                # --- ส่วนควบคุมการรับดาเมจและการชน (Collision Logic) ที่แก้ไขใหม่ ---
                if now - self.player.spawn_time > 3000 and not self.player.shield_gold_active:
                    
                    # 1. โดนกระสุนศัตรูทุกชนิด (Normal + Homing)
                    enemy_bullet_hits = pygame.sprite.spritecollide(self.player, self.e_bullets, True, pygame.sprite.collide_mask)
                    for b in enemy_bullet_hits:
                        self.player.health -= b.damage # ดาเมจตามที่ตั้งไว้ (Homing=15, Normal=5-10)


                    # 3. ชนตัวยานศัตรูโดยตรง
                    enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, True, pygame.sprite.collide_mask)
                    for e in enemy_hits:
                        self.player.health -= 20 # ชนยานลด 20 HP

                    # 4. เช็คความตาย
                    if self.player.health <= 0:
                        if self.sfx['lose']: self.sfx['lose'].play()
                        running = False
                # ---------------------------------------------------

                    # --- ส่วนที่แก้ไขใหม่: เช็ค Meteor รายตัว ---
                    meteor_hits = pygame.sprite.spritecollide(self.player, self.meteors, False, pygame.sprite.collide_mask)
                    for m in meteor_hits:
                        if "tiny2" in m.size_tag or "tiny1" in m.size_tag:
                            pass # tiny โดนแล้วไม่เป็นไรเลย ชิลล์ๆ
                        elif "small2" in m.size_tag or "small1" in m.size_tag:
                            self.player.health -= 1 # small ลด 1 HP
                            pass # ชนแล้วให้ก้อนหินหายไปด้วย จะได้ไม่โดนซ้ำ
                        else:
                            # ขนาด med หรือ big ชนแล้ว Game Over เหมือนเดิม
                            if self.sfx['lose']: self.sfx['lose'].play()
                            running = False
                    
                    if pygame.sprite.spritecollide(self.player, self.enemies, True, pygame.sprite.collide_mask) or self.player.health <= 0: 
                        if self.sfx['lose']: self.sfx['lose'].play()
                        running = False

                self.screen.blit(self.bg_image, (0, 0))
                self.all_sprites.draw(self.screen)
                if self.boss: self.boss.draw_hp(self.screen)
                self.player.draw_ui(self.screen)
                txt = self.font.render(f"Score: {self.score} HP: {self.player.health}", True, (255, 255, 255))
                self.screen.blit(txt, (10, 10))
                pygame.display.flip(); self.clock.tick(FPS)

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.big_font.render("GAME OVER", True, (255, 0, 0)), (WIDTH//2 - 130, HEIGHT//2 - 100))
            self.screen.blit(self.font.render(f"Score: {self.score} | Time: {final_survival_time}s | Gold Stars: {self.player.total_gold_stars_collected}", True, (255, 255, 255)), (WIDTH//2 - 180, HEIGHT//2 - 20))
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r: waiting = False

if __name__ == "__main__":
    GameEngine().run()