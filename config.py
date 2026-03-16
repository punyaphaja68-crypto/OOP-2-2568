"""
Configuration file for Rocket Evolution Game
Contains all global constants and configuration values
"""

# --- Screen Configuration ---
WIDTH = 800
HEIGHT = 600
FPS = 60

# --- Game Configuration ---
PLAYER_MAX_HEALTH = 100
PLAYER_SPAWN_SHIELD_DURATION = 3000  # ms

# --- Enemy Configuration ---
MAX_ENEMIES = 3
ENEMY_SPAWN_PROBABILITY = 0.01
ENEMY_SHIP_COLORS = ["Red", "Blue", "Green", "Orange", "Black"]
ENEMY_SHIP_DAMAGE = 5
ENEMY_UFO_DAMAGE = 10
HOMING_BULLET_DAMAGE = 15

# --- Meteor Configuration ---
MAX_METEORS = 12
METEOR_SPAWN_PROBABILITY = 0.05
METEOR_TYPES = ["Brown", "Grey"]
METEOR_SIZES = [("big1", 70), ("med1", 45), ("small1", 25), ("tiny1", 15)]

# --- Projectile Configuration ---
PLAYER_NORMAL_BULLET_SPEED = 12
PLAYER_HYPER_BULLET_SPEED = 15
HYPER_MODE_DAMAGE = 50
NORMAL_MODE_DAMAGE = 5
BOSS_BULLET_SPEED = 6
UFO_BULLET_SPEED = 5
HOMING_BULLET_SPEED = 3.5

# --- Item Configuration ---
ITEM_SPAWN_PROBABILITY = 0.008
PLAYER_COLLISION_DAMAGE = 20
PLAYER_HEALTH_RESTORE = 20

# --- Boss Configuration ---
BOSS_SPAWN_SCORE = 100
BOSS_MAX_HEALTH = 500
BOSS_SPAWN_BULLET_COOLDOWN = 2500  # ms
BOSS_GUARDS_COUNT = 8

# --- UI Configuration ---
BACKGROUND_CHANGE_INTERVAL = 200  # score points
STAR_UPGRADE_THRESHOLD = {"bronze": 3, "silver": 5, "gold": 3}

# --- Power-up Durations ---
SPEED_BOOST_DURATION = 5000  # ms
SHIELD_GOLD_DURATION = 7000  # ms
HYPER_MODE_DURATION = 30000  # ms
BEAM_LASER_DURATION = None  # Variable

# --- Sound Files ---
SOUND_FILES = {
    'laser1': ("Bonus", "sfx_laser1.ogg"),
    'laser2': ("Bonus", "sfx_laser2.ogg"),
    'lose': ("Bonus", "sfx_lose.ogg"),
    'shield': ("Bonus", "sfx_shieldUp.ogg"),
    'boss_death': ("Bonus", "sfx_twoTone.ogg")
}

# --- Gameplay Statistics ---
SCORE_PER_ENEMY_KILL = 10
SCORE_PER_BOSS_KILL = 500
