# constants.py

SCREEN_TITLE = "Survivor Game"

SPRITE_SCALING = 0.25
SPRITE_SIZE = 32

GRID_WIDTH = 30
GRID_HEIGHT = 20
SPRITE_SPEED = 1
BULLET_SPEED = 5
RELOAD_BULLET_TIME = 3
NB_ENEMIES = 5
LVL_AGENT = 1

PLAYER_HEALTH = 5

MAP_WALL = 'W'  # Wall
MAP_WALL_T = 'WT'  # Wall
MAP_OBSTACLE = 'O'  # Obstacle
MAP_OBSTACLE2 = 'O2'  # Obstacle
MAP_OBSTACLE3 = 'O3'  # Obstacle
MAP_EMPTY = 'E'  # Empty
MAP_AGENT = 'A'  # Agent
MAP_ENEMY = 'EN1'  # Enemy
MAP_ENEMY2 = 'EN2'  # Enemy


def set_nb_enemies(value):
    global NB_ENEMIES
    NB_ENEMIES = value


def set_bullet_time(value):
    global RELOAD_BULLET_TIME
    RELOAD_BULLET_TIME = value


def get_nb_enemies():
    return NB_ENEMIES


def get_bullet_time():
    return RELOAD_BULLET_TIME
