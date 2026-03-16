"""
Rocket Evolution Game - Main Entry Point
A space shooter game with upgradeable systems and boss encounters.

Structure:
- config.py: Game configuration constants
- core/: Game engine and asset management
  - engine.py: GameEngine class (main game loop)
  - asset_manager.py: AssetManager class (resource loading)
- entities/: Game object classes
  - base.py: GameObject base class
  - player.py: Player class
  - enemies.py: Enemy classes
  - obstacles.py: Meteor and Debris classes
  - projectiles.py: Bullet and HomingBullet classes
  - items.py: Pill (power-ups) class

OOP Principles Demonstrated:
- Inheritance: Entity hierarchy from GameObject
- Polymorphism: Different entity types with overridden update()
- Encapsulation: Private attributes with properties
- Composition: Entities contain references to other objects
- Single Responsibility: Each class has one main purpose
- Dependency Injection: AssetManager passed to GameEngine
- Factory Pattern: Pill.create_random() for item spawning
"""

from core.engine import GameEngine
from core.asset_manager import AssetManager


def main():
    """Start the game"""
    asset_manager = AssetManager()
    game = GameEngine(asset_manager)
    game.run()


if __name__ == "__main__":
    main()
