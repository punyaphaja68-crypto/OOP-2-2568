# Rocket Evolution - Refactored Architecture & SOLID Principles

## 📋 Overview

This document explains the refactored code structure, demonstrating clear application of **OOP principles** (Inheritance, Polymorphism, Encapsulation, Composition) and **SOLID principles** (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion).

---

## 🎯 OOP Principles Implementation

### 1. **Inheritance (สืบทอด)**

**Examples in codebase:**

#### a) GameObject Hierarchy
```
GameObject (Abstract Base Class)
├── Bullet
├── Debris  
├── Pill
├── Player
├── Meteor
└── Enemy (Abstract)
    ├── EnemyShip
    ├── UFOEnemy
    └── BigUFOBoss
```

**Benefits:**
- Common sprite functionality centralized in `GameObject`
- Reusable image loading, positioning, and collision detection
- Consistent interface across all game objects

#### b) Enemy Hierarchy
```python
class Enemy(GameObject, ABC):
    """Abstract base for all enemies"""
    def __init__(self, x, y, image_path, scale, target):
        super().__init__(...)  # Call parent initializer
        
# Concrete implementations
class EnemyShip(Enemy):
    def update(self, ...): ...

class UFOEnemy(Enemy):
    def update(self, ...): ...

class BigUFOBoss(Enemy):
    def update(self, ...): ...
```

---

### 2. **Polymorphism (รูปแบบหลากหลาย)**

#### a) Strategy Pattern for Bullet Behavior
```python
class BulletBehavior(ABC):
    @abstractmethod
    def update_position(self, bullet): pass
    
class LinearBulletBehavior(BulletBehavior):
    def update_position(self, bullet):
        bullet.rect.y += bullet._speed  # Straight movement

class HomingBulletBehavior(BulletBehavior):
    def update_position(self, bullet):
        # Track target and move towards it
        distance = math.hypot(dx, dy)
        bullet.rect.x += (dx / distance) * self._speed

# Polymorphic usage
class Bullet(GameObject):
    def __init__(self, ..., behavior=None):
        self._behavior = behavior or LinearBulletBehavior()
    
    def update(self):
        self._behavior.update_position(self)  # Runtime polymorphism!
```

**Benefits:**
- Different bullet types without modifying Bullet class
- Easy to add new movement patterns
- Runtime behavior selection

#### b) Enemy Behavior Polymorphism
```python
class StandardEnemyBehavior(EnemyBehavior):
    def update_position(self, enemy): ...
    def shoot(self, enemy, bullet_group, all_sprites): ...

class UFOBehavior(EnemyBehavior):
    def update_position(self, enemy): ...
    def shoot(self, enemy, bullet_group, all_sprites): ...

# Enemies use behaviors polymorphically
class EnemyShip(Enemy):
    def __init__(self, ...):
        self._behavior = StandardEnemyBehavior(self._color_name)
    
    def update(self, bullet_group, all_sprites):
        self._behavior.update_position(self)
        self._behavior.shoot(self, bullet_group, all_sprites)
```

---

### 3. **Encapsulation (การห่อหุ้ม)**

#### a) Private Attributes with Properties
```python
class Player(GameObject):
    def __init__(self):
        self._health = 100           # PRIVATE (with underscore)
        self._max_health = 100
        self._speed = 6
        self._shield_system = StarSystem()
        self._star_system = ShieldSystem()
    
    # PROPERTIES for safe access
    @property
    def health(self) -> int:
        return self._health
    
    @health.setter
    def health(self, value: int) -> None:
        self._health = max(0, min(value, self._max_health))
    
    @property
    def is_hyper_active(self) -> bool:
        return self._hyper_mode_active
```

**Benefits:**
- Health can't go below 0 or above max
- Validation on setters
- Change implementation without breaking public API

#### b) Composition Over Inheritance
```python
class Player(GameObject):
    def __init__(self, ...):
        # Instead of inheriting from StarSystem and ShieldSystem,
        # we COMPOSE them (have them as members)
        self._star_system: StarSystem = StarSystem()
        self._shield_system: ShieldSystem = ShieldSystem()
    
    def add_star(self, star_type: str):
        # Delegate to composed object
        self._star_system.add_star(star_type)
    
    # Other methods also delegate to composed objects
```

**Why Composition Over Inheritance:**
- More flexible: can swap implementations easily
- Avoids "fragile base class" problem
- Single responsibility becomes clearer
- Reusable in different contexts

#### c) Private Methods (Encapsulation)
```python
class Player(GameObject):
    def update(self, score):
        self._update_evolution(score)      # Private helper
        self._update_movement(None)        # Private helper
        self._update_shooting(None)        # Private helper
        self._update_regeneration(None)    # Private helper
    
    def _update_evolution(self, score):
        """Private implementation detail"""
        ...
    
    def _shoot(self, is_beam=False):
        """Private - only called from update"""
        ...
```

---

## ✅ SOLID Principles Implementation

### 1. **S - Single Responsibility Principle**

Each class has ONE reason to change:

| Class | Responsibility |
|-------|-----------------|
| `Player` | Manage player character state |
| `StarSystem` | Manage star collection & leveling |
| `ShieldSystem` | Manage shield states |
| `Bullet` | Represent a bullet projectile |
| `EnemyShip` | Represent an enemy ship |
| `SpawningManager` | Spawn entities |
| `CollisionDetector` | Detect collisions |
| `Renderer` | Draw game to screen |
| `AudioManager` | Play sound effects |
| `GameEngine` | Orchestrate all systems |

```python
# ❌ BAD: Multiple responsibilities
class GameEngine:
    def update(self):
        # Spawning
        if random.random() < 0.01:
            enemy = EnemyShip(...)
            
        # Collision
        hits = pygame.sprite.groupcollide(...)
        
        # Rendering
        self.screen.blit(...)
        
        # Audio
        self.sfx['laser'].play()

# ✅ GOOD: Separated responsibilities
class SpawningManager:
    def spawn_enemies(self, ...): ...

class CollisionDetector:
    @staticmethod
    def detect_collisions(...): ...

class Renderer:
    def draw_game(self, ...): ...

class AudioManager:
    def play(self, key): ...

class GameEngine:
    def run(self):
        self._spawning_manager.spawn_enemies(...)
        self._handle_collisions()
        self._renderer.draw_game(...)
        self._audio_manager.play(...)
```

---

### 2. **O - Open/Closed Principle**

**Open for extension, Closed for modification:**

#### Adding New Enemy Types
```python
# Original: EnemyShip, UFOEnemy already exist
# Want to add: RobotEnemy?

# ✅ GOOD: Just extend,don't modify
class RobotEnemy(Enemy):
    def __init__(self, target):
        super().__init__(...)
        self._behavior = RobotBehavior()
    
    def update(self, ...):
        self._behavior.update_position(self)
        self._behavior.shoot(self, ...)

# Factory automatically supports it
class EnemyFactory:
    enemies = [EnemyShip, UFOEnemy, RobotEnemy]
    
    @staticmethod
    def create_random_enemy(player, score):
        enemy_class = random.choice(EnemyFactory.enemies)
        return enemy_class(score, player)
```

#### Adding New Bullet Types
```python
# Want custom bullet behavior?

class WaveBulletBehavior(BulletBehavior):
    def update_position(self, bullet):
        bullet.rect.y += bullet._speed
        bullet.rect.x += math.sin(time.time() * 5) * 3

# Use it:
wave_bullet = Bullet(..., behavior=WaveBulletBehavior())
```

---

### 3. **L - Liskov Substitution Principle**

Derived classes must be substitutable for base classes:

```python
# ✅ GOOD: All enemies work the same way
def update_all_enemies(enemies):
    for enemy in enemies:  # Works with any Enemy subclass
        enemy.update(bullet_group, all_sprites)

# This works for:
enemies = [EnemyShip(...), UFOEnemy(...), BigUFOBoss(...)]

for enemy in enemies:
    enemy.update(...)  # Polymorphic call - respects contract
```

**Contract:** All Enemy subclasses:
- Have `update(bullet_group, all_sprites)` method
- Have `rect` property for positioning
- Have `collision_rect` and `collision_mask` properties
- Follow same lifecycle

---

### 4. **I - Interface Segregation Principle**

Clients depend on specific interfaces, not broad ones:

```python
# ✅ GOOD: Segregated interfaces
class Drawable(ABC):
    @abstractmethod
    def draw(self, surface): pass

class Collidable(ABC):
    @property
    @abstractmethod
    def collision_rect(self): pass

class GameObject(pygame.sprite.Sprite, Drawable, Collidable):
    # Implements both interfaces but clients only use what they need
    pass

# Renderer only cares about Drawable
def draw_game(self, all_sprites):
    for sprite in all_sprites:
        if isinstance(sprite, Drawable):
            sprite.draw(self._screen)

# Collision system only cares about Collidable
def detect_collision(player, enemies):
    hits = pygame.sprite.spritecollide(player, enemies, ...)
    # Collidable interface provides collision_rect and collision_mask
```

---

### 5. **D - Dependency Inversion Principle**

High-level modules depend on abstractions, not low-level modules:

```python
# ✅ GOOD: Factory pattern (abstraction)
class EnemyFactory:
    @staticmethod
    def create_random_enemy(player, score):
        return EnemyShip(score, player)

class GameEngine:
    def _update_game(self):
        # Depends on factory abstraction, not concrete class
        enemy = EnemyFactory.create_random_enemy(self._player, self._score)
        self._enemies.add(enemy)

# ✅ GOOD: Dependency injection
class Player:
    def __init__(self, bullet_group, all_sprites, sfx_dict):
        # Dependencies injected in constructor
        self._bullet_group = bullet_group
        self._all_sprites = all_sprites
        self._sfx = sfx_dict

class GameEngine:
    def _reset_game(self):
        player = Player(self._p_bullets, self._all_sprites, self._get_sfx_dict())
        # Provides dependencies to player
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              GameEngine (Facade Pattern)                │
│    Coordinates all subsystems and game loop             │
└──────┬──────────────────────────────────────────────────┘
       │
   Delegates to
 (Composition)
       │
   ┌───┴────────────────────────────────────────────────┐
   │                                                     │
   ▼                    ▼              ▼           ▼          ▼
┌──────────┐ ┌──────────────┐ ┌──────────┐ ┌────────┐ ┌──────────┐
│Renderer  │ │SpawningMgr   │ │Collision │ │Audio   │ │Background│
│          │ │              │ │Detector  │ │Manager │ │Manager   │
│ - draw   │ │ - spawn      │ │          │ │        │ │          │
│ - update │ │ - manage     │ │ - detect │ │ - play │ │ - load   │
|background       spawning  │ │ collisions           │ │ - switch │
└──────────┘ └──────────────┘ └──────────┘ └────────┘ └──────────┘
   
   
   Game Objects (Hierarchy):
   ┌──────────────────────────────┐
   │       GameObject (ABC)       │
   │   (Drawable, Collidable)    │
   └──────────────────────────────┘
              ▲  ▲  ▲  ▲  ▲
              │  │  │  │  │
         ┌────┴─┴──┴──┴──┴────┐
         │  │  │  │  │  │     │
         ▼  ▼  ▼  ▼  ▼  ▼     ▼
      Player Bullet Debris Pill Meteor Enemy Others
                                         ▲
                                  ┌──────┴──────┬─────┐
                                  ▼             ▼     ▼
                              EnemyShip    UFOEnemy BigUFOBoss
                              
                              
   Composition Examples:
   ┌─────────────┐
   │   Player    │
   ├─────────────┤
   │ - Health    │
   │ - StarSystem│ ◄──────── Composed (HasA)
   │ - ShieldSys │ ◄────────── Not inherited
   │ - Weapons   │  (more flexible)
   └─────────────┘
```

---

## 📚 Key Design Patterns Used

### 1. **Strategy Pattern**
```python
# Bullet behavior strategies
BulletBehavior
├── LinearBulletBehavior
└── HomingBulletBehavior

# Enemy behavior strategies
EnemyBehavior
├── StandardEnemyBehavior
└── UFOBehavior
```

### 2. **Factory Pattern**
```python
class EnemyFactory:
    @staticmethod
    def create_random_enemy(player, score): ...

class PowerUpFactory:
    @staticmethod
    def create_random_powerup(): ...
```

### 3. **Facade Pattern**
```python
class GameEngine:
    # Hides complexity of all subsystems
    def run(self):
        # Simple public interface
        while True:
            self._reset_game()
            self._update_game()
            self._handle_collisions()
            self._renderer.draw_game(...)
```

### 4. **Composition Over Inheritance**
```python
class Player(GameObject):
    def __init__(self):
        self._star_system = StarSystem()      # Composed
        self._shield_system = ShieldSystem()  # Composed
        # Not: class Player(GameObject, StarSystem, ShieldSystem)
```

### 5. **Template Method Pattern (Abstract Methods)**
```python
class GameObject(ABC):
    @abstractmethod
    def update(self, *args, **kwargs): pass

# Each subclass implements its own update logic
class Bullet(GameObject):
    def update(self): ...

class Meteor(GameObject):
    def update(self): ...
```

---

## 🎮 Game Flow Diagram

```
┌─────────────────┐
│  GameEngine.run │
└────────┬────────┘
         │
    ┌────▼─────┐
    │ New Game  │
    └────┬─────┘
         │
    ┌────▼──────────────────────────┐
    │ Game Loop (while running)      │
    ├────────────────────────────────┤
    │                                │
    │ 1. Handle input events         │
    │ 2. Spawn enemies & items       │ ◄─── SpawningManager
    │ 3. Update all objects          │
    │    - Player.update()           │
    │    - Enemy.update()            │
    │    - Meteor.update()           │
    │ 4. Detect collisions           │ ◄─── CollisionDetector
    │ 5. Handle collisions           │
    │ 6. Render frame                │ ◄─── Renderer
    │                                │
    └────┬──────────────────────────┘
         │
    ┌────▼────────────────┐
    │ Player Dead? YES     │
    └────┬────────────────┘
         │
         NO                YES
         │ ┌──────────────┐
         └─┤ Game Over    │
           │ Screen       │
           └──────┬───────┘
                  │
           ┌──────▼──────┐
           │ Wait for    │
           │ Restart (R) │
           │ or Quit (Q) │
           └──────┬──────┘
                  │
             Restart game
                  │
                  └──────Back to "New Game"
```

---

## 📊 Class Relationships Summary

| Class | Inherits From | Composed Objects | Implements |
|-------|---------------|------------------|------------|
| GameObject | pygame.Sprite | None | Drawable, Collidable |
| Bullet | GameObject | BulletBehavior | - |
| Player | GameObject | StarSystem, ShieldSystem | - |
| Enemy | GameObject | EnemyBehavior | - |
| EnemyShip | Enemy | StandardEnemyBehavior | - |
| UFOEnemy | Enemy | UFOBehavior | - |
| GameEngine | Object | AudioManager, BackgroundManager, GameState,  SpawningManager, Renderer | - |

---

## 🚀 How to Extend the Code

### Adding a New Enemy Type
```python
class LaserEnemy(Enemy):
    def __init__(self, target):
        super().__init__(...)
        self._behavior = LaserEnemyBehavior()
    
    def update(self, bullet_group, all_sprites):
        self._behavior.update_position(self)
        self._behavior.shoot(self, bullet_group, all_sprites)

# Register in factory if needed
```

### Adding a New Bullet Style
```python
class TracingBulletBehavior(BulletBehavior):
    def update_position(self, bullet):
        # Custom movement logic
        pass

# Use it
bullet = Bullet(..., behavior=TracingBulletBehavior())
```

### Adding a New Power-up
```python
# Add to PowerUpType
class PowerUpType:
    # ... existing ...
    INVINCIBILITY = "invincibility"

# Add to PowerUpFactory.POWERUP_CONFIGS
# Add handling to Player.collect_powerup()
```

---

## ✨ Benefits of This Refactoring

1. **Maintainability**: Clear separation of concerns makes code easier to understand
2. **Extensibility**: Add new features without modifying existing code
3. **Testability**: Each component can be tested independently
4. **Reusability**: Components like StarSystem, ShieldSystem are encapsulated
5. **Flexibility**: Strategy pattern allows behavior changes without inheritance
6. **Scalability**: New enemies, bullets, items can be added easily
7. **Type Safety**: Type hints throughout for better IDE support
8. **Documentation**: Clear comments explaining design patterns and principles

---

## 📝 Summary

This refactoring demonstrates:
- ✅ **Inheritance**: Proper class hierarchies (GameObject, Enemy)
- ✅ **Polymorphism**: Runtime behavior via strategy pattern
- ✅ **Encapsulation**: Private attributes with property accessors
- ✅ **Composition**: Preferred over inheritance (Player → StarSystem)
- ✅ **S**ingle Responsibility: Each class has one job
- ✅ **O**pen/Closed: Easy to extend, hard to break
- ✅ **L**iskov Substitution: Interchangeable derived classes  
- ✅ **I**nterface Segregation: Focused interfaces
- ✅ **D**ependency Inversion: Factory patterns and composition

The game maintains the same look and feel while being cleaner, more maintainable, and professional-grade code!
