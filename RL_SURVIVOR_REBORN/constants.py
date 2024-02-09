# constants.py

SCREEN_TITLE = "Survivor Game"

SPRITE_SCALING = 0.25
SPRITE_SIZE = 32

GRID_WIDTH = 30
GRID_HEIGHT = 20
SPRITE_SPEED = 3
BULLET_SPEED = 10
RELOAD_BULLET_TIME = 3
NB_ENEMIES = 2
LVL_AGENT = 1

PLAYER_HEALTH = 5
AGENT_POS = (1, 1)

MAP_WALL = 'W'  # Wall
MAP_WALL_T = 'WT'  # Wall
MAP_OBSTACLE = 'O'  # Obstacle
MAP_OBSTACLE2 = 'O2'  # Obstacle
MAP_OBSTACLE3 = 'O3'  # Obstacle
MAP_EMPTY = 'E'  # Empty
MAP_AGENT = 'A'  # Agent
MAP_ENEMY = 'EN'  # Enemy
MAP_XP = 'XP'  # XP
MAP_BULLET = 'B'  # Bullet

ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT = 'U', 'D', 'L', 'R'
ACTIONS = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

MOVES = {ACTION_UP: (1, 0),
         ACTION_DOWN: (-1, 0),
         ACTION_LEFT: (0, -1),
         ACTION_RIGHT: (0, 1)}

REWARD_ENEMY = -1000
REWARD_NEAR_ENEMY = -100
REWARD_DEFAULT = 0
REWARD_GOAL = 2000
REWARD_NEAR_GOAL = 100
REWARD_WALL = -50

AGENT_FILE = 'survivor.qtable'


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
