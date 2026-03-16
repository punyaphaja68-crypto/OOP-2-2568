# 🔧 Quick Reference Guide - Refactored Code Structure

## File Structure

```
main.py
├── Imports & Configuration
│
├── SECTION 1: Abstract Base Classes & Interfaces
│   ├── GameObjectType (Enum)
│   ├── Drawable (Interface)
│   ├── Collidable (Interface)
│   └── GameObject (Abstract Base)
│
├── SECTION 2: Bullet System
│   ├── BulletBehavior (Strategy)
│   ├── LinearBulletBehavior
│   ├── HomingBulletBehavior
│   ├── Bullet
│   └── Debris
│
├── SECTION 3: Power-ups
│   ├── PowerUpType (Constants)
│   └── Pill
│
├── SECTION 4: Player System
│   ├── StarSystem
│   ├── ShieldSystem
│   └── Player
│
├── SECTION 5: Enemy System
│   ├── EnemyBehavior (Strategy)
│   ├── StandardEnemyBehavior
│   ├── Enemy (Abstract)
│   ├── EnemyShip
│   ├── UFOBehavior
│   ├── UFOEnemy
│   └── BigUFOBoss
│
├── SECTION 6: Meteor System
│   └── Meteor
│
├── SECTION 7: Factories
│   ├── EnemyFactory
│   └── PowerUpFactory
│
├── SECTION 8: Collision Detection
│   └── CollisionDetector
│
├── SECTION 9: Spawning System
│   └── SpawningManager
│
├── SECTION 10: Rendering
│   └── Renderer
│
├── SECTION 11: Game Engine
│   ├── AudioManager
│   ├── BackgroundManager
│   ├── GameState
│   └── GameEngine (Main)
│
└── Entry Point: if __name__ == "__main__"
```

---

## Key Classes at a Glance

### 🎯 Abstract Base Classes

| Class | Purpose | Key Methods |
|-------|---------|------------|
| `Drawable` | Objects that can be drawn | `draw(surface)` |
| `Collidable` | Objects with collision | `collision_rect`, `collision_mask` |
| `GameObject` | All game objects inherit | `update()`, `image`, `rect` |
| `Enemy` | Base for all enemies | `update(bullets, sprites)` |
| `BulletBehavior` | Movement strategies | `update_position()`, `is_out_of_bounds()` |
| `EnemyBehavior` | Enemy behavior strategies | `update_position()`, `shoot()` |

### 👤 Player System

```python
class Player(GameObject):
    # Manages: Position, Health, Weapons, Stars, Shields
    
    # Composed objects (Composition > Inheritance)
    _star_system: StarSystem        # Stars & leveling
    _shield_system: ShieldSystem    # Shield states
    
    # Key public properties
    health: int
    color: str
    is_hyper_active: bool
    
    # Key methods
    update(score)           # Called every frame
    take_damage(amount)     # Returns if dead
    add_star(type)          # Add star, check for hyper
    collect_powerup(pill)   # Handle powerup effects
    draw_ui(surface)        # Draw UI elements
```

### 🎯 Enemy System

```python
class Enemy(GameObject, ABC):
    # Abstract base for all enemies
    _target: Player
    _speed: float
    _is_alive: bool
    
    @abstractmethod
    def update(bullet_group, all_sprites): pass

# Concrete implementations
class EnemyShip(Enemy):
    # Red/Blue/Green enemy ships with strategies
    _behavior: StandardEnemyBehavior

class UFOEnemy(Enemy):
    # UFO enemies with homing tracking
    _behavior: UFOBehavior

class BigUFOBoss(Enemy):
    # Boss with 500 HP, homing bullets, stationary
    health: int
    draw_hp(surface)
```

### 💥 Bullet System

```python
class Bullet(GameObject):
    # Uses Strategy pattern for movement
    _behavior: BulletBehavior  # Linear or Homing
    
    # Two built-in strategies
    LinearBulletBehavior()      # Straight down
    HomingBulletBehavior()      # Tracks target
```

### 📦 Power-ups

```python
class Pill(GameObject):
    color: str              # gold, blue, bronze, etc.
    item_type: str          # SHIELD_GOLD, SPEED_BOOST, etc.
    
# Handled by Player.collect_powerup()
SHIELD_GOLD        → Activate gold shield 7s
SPEED_BOOST        → Boost speed 5s
STAR_BRONZE/SILVER → Add star
HEALTH (green)     → Restore 20 HP
```

### 🎮 Game Engine

```python
class GameEngine:
    # Main orchestrator (Facade Pattern)
    
    # Subdelegates
    _audio_manager: AudioManager
    _bg_manager: BackgroundManager
    _renderer: Renderer
    _spawning_manager: SpawningManager
    
    # Sprite groups
    _all_sprites, _enemies, _meteors, _pills
    _p_bullets, _e_bullets
    
    # Main public method
    run()               # Infinite game loop
```

### 🏭 Factories (Dependency Inversion)

```python
class EnemyFactory:
    @staticmethod
    create_random_enemy(player, score) → Enemy
    create_ufo_enemy(player) → UFOEnemy
    create_boss(player) → BigUFOBoss

class PowerUpFactory:
    @staticmethod
    create_random_powerup() → Pill  # Based on probability
```

### 💥 Collision Detection

```python
class CollisionDetector:
    @staticmethod
    detect_enemy_bullet_collisions(enemies, p_bullets) 
        → (hit_enemies, score_gained)
    
    detect_player_damage(player, e_bullets, enemies, meteors)
        → damage_amount
    
    detect_boss_bullet_collisions(boss, p_bullets)
        → damage_amount
```

### 🎮 Spawning Manager

```python
class SpawningManager:
    spawn_enemies(...)          # Random enemy spawning
    spawn_meteors(...)          # Random meteor spawning
    spawn_powerup(...)          # Random powerup spawning
    spawn_boss_if_ready(...)    # Spawn boss at score 100
    spawn_boss_guards(...)      # 8 UFO guards around boss
```

### 🎨 Renderer

```python
class Renderer:
    draw_game(sprites, player, boss, score)
    draw_game_over(score, time, gold_stars)
    set_background(image)
```

### 🔊 Audio Manager

```python
class AudioManager:
    get_sound(key) → Sound or None
    play(key)      # Play sound by key
```

### 🌅 Background Manager

```python
class BackgroundManager:
    get_current_background() → Surface
    get_random_background() → Surface
```

---

## 🔄 Game Loop Flow

```python
GameEngine.run():
    while True:  # Infinite game loop
        1. _reset_game()
           ├─ Clear all sprites
           ├─ Create new player
           ├─ Initialize GameState
           └─ Play shield sound
        
        2. Set background
        
        3. while running:  # Inner loop per round
           │
           ├─ Handle events (quit)
           │
           ├─ _update_game()
           │  ├─ Update all sprites
           │  │  ├─ Player.update(score)
           │  │  ├─ Enemy.update(...)
           │  │  └─ Meteor.update(...)
           │  │
           │  ├─ Spawn enemies (random)
           │  ├─ Spawn meteors (random)
           │  ├─ Spawn powerups (random)
           │  └─ Spawn boss if score >= 100
           │
           ├─ _handle_collisions()
           │  ├─ Detect enemy bullet hits
           │  ├─ Detect player damage
           │  ├─ Detect boss damage
           │  ├─ Detect powerup collection
           │  └─ Check background changes
           │  └─ Return True if player dead
           │
           ├─ _renderer.draw_game(...)
           │
           └─ Clock.tick(60 FPS)
        
        4. Show Game Over screen
        
        5. Wait for Restart (R) or Quit (Q)
```

---

## 📋 Creating New Content

### Adding a New Enemy Type

```python
# 1. Create behavior (if needed)
class SnakeEnemyBehavior(EnemyBehavior):
    def update_position(self, enemy):
        # Wavy movement
        enemy.rect.y += enemy._speed
        enemy.rect.x += math.sin(time.time() * 2) * 3

# 2. Extend Enemy
class SnakeEnemy(Enemy):
    def __init__(self, target):
        super().__init__(x, y, "path/to/image", (50, 40), target)
        self._behavior = SnakeEnemyBehavior()
    
    def update(self, bullet_group, all_sprites):
        self._behavior.update_position(self)
        self._behavior.shoot(self, bullet_group, all_sprites)

# 3. Register in factory (optional)
class EnemyFactory:
    ENEMY_TYPES = [EnemyShip, UFOEnemy, SnakeEnemy]
```

### Adding a New Power-up

```python
# 1. Add type constant
class PowerUpType:
    # ... existing ...
    INVINCIBILITY = "invincibility"

# 2. Create Pill in factory
class PowerUpFactory:
    POWERUP_CONFIGS = [
        # ... existing ...
        (0.05, lambda: Pill("purple", PowerUpType.INVINCIBILITY, ...)),
    ]

# 3. Handle in Player
class Player:
    def collect_powerup(self, powerup):
        # ... existing ...
        elif powerup.item_type == PowerUpType.INVINCIBILITY:
            self._invincibility_end = now + 10000
```

### Adding a New Bullet Style

```python
# 1. Create behavior
class BouncingBulletBehavior(BulletBehavior):
    def __init__(self, target):
        self._target = target
        self._bounces = 0
    
    def update_position(self, bullet):
        # Bouncing logic
        pass
    
    def is_out_of_bounds(self, bullet):
        return self._bounces > 5

# 2. Use it
behavior = BouncingBulletBehavior(target)
bullet = Bullet(..., behavior=behavior)
```

---

## 🔍 How to Find Things

| Want to... | Look in |
|-----------|---------|
| Change player speed | `Player._base_speed` |
| Change enemy spawn rate | `SpawningManager._enemy_spawn_probability` |
| Change bullet damage | `Bullet.__init__` damage parameter |
| Change player max HP | `Player.__init__` `_max_health` |
| Add new star type | `StarSystem.add_star()` |
| Change shield duration | `ShieldSystem.activate_gold_shield()` |
| Add new sound effect | `AudioManager._load_all_sounds()` |
| Change game resolution | `WIDTH, HEIGHT` constants |
| Change FPS | `FPS` constant |
| Modify rendering | `Renderer.draw_game()` |
| Add collision detection | `CollisionDetector` static methods |

---

## 🎯 Key Principles in Code

### Single Responsibility
- `AudioManager` - only plays sounds
- `Renderer` - only draws
- `CollisionDetector` - only detects collisions
- `SpawningManager` - only spawns
- Each has ONE reason to change

### Encapsulation
- Player health: `self._health` (private) + `@property` (public)
- Can't set invalid values
- Internal implementation can change

### Polymorphism
- `BulletBehavior` strategies for different bullet movements
- `EnemyBehavior` strategies for different enemy behaviors
- All `Enemy` subclasses work the same way

### Composition
- `Player` has-a `StarSystem` (not is-a)
- `Player` has-a `ShieldSystem` (not is-a)
- More flexible than inheritance

### Factory Pattern
- `EnemyFactory.create_random_enemy()`
- `PowerUpFactory.create_random_powerup()`
- Hide creation complexity

### Facade Pattern
- `GameEngine` coordinates everything
- Simple public interface: `run()`
- Hides complexity of subsystems

---

## ✅ Common Tasks

### Change enemy damage
```python
class StandardEnemyBehavior:
    def shoot(self, enemy, bullet_group, all_sprites):
        bullet = Bullet(..., damage=10)  # Change here
```

### Change spawn probabilities
```python
class SpawningManager:
    def __init__(self):
        self._enemy_spawn_probability = 0.02  # Change this
        self._meteor_spawn_probability = 0.08  # Or this
        self._powerup_spawn_probability = 0.01  # Or this
```

### Change player movement speed
```python
class Player:
    def __init__(self):
        self._base_speed = 8  # Base speed
        
    def _update_movement(self, now):
        # Speed boost is 1.5x base
        self._current_speed = self._base_speed * 1.5
```

### Modify boss HP
```python
class BigUFOBoss:
    def __init__(self, target):
        self._health = 750  # Change this
        self._max_health = 750
```

---

## 🚀 Tips for Development

1. **Type hints are your friend** - Use them for clarity
2. **Properties for encapsulation** - Protect internal state
3. **Strategy pattern for variations** - Don't use if/else
4. **Composition over inheritance** - More flexible
5. **Factory for creation** - Hide complexity
6. **One reason to change** - Each class has one job
7. **Interfaces for contracts** - Consistent behavior

---

## 📚 Further Reading

- See `ARCHITECTURE.md` for detailed principle explanations
- Each class has docstrings explaining its purpose
- Comments explain WHY, not WHAT

Happy coding! 🎮
