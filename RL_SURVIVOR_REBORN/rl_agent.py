import pickle
from os.path import exists

from utils import state_to_xy, xy_to_state
from constants import *
from random import *


class ReinforcementLearning:
    def __init__(self):
        self.position = AGENT_POS
        self.map = {}
        # self.reset()
        # self.add_state(self.state)

    def setup(self):
        self.position = AGENT_POS
        self.map = {}

    def do(self, map_actual):
        self.map = map_actual
        action = self.best_action()
        self.position = self.move(self.position, action)

    def best_action(self):
        #  faire une action aléatoire
        return choice(ACTIONS)

    def move(self, position, action):
        move = MOVES[action]
        new_position = (position[0] + move[0], position[1] + move[1])
        if self.is_not_allowed(new_position):
            return position
        else:
            return new_position

    def is_not_allowed(self, position):
        # si pas dans la map ou si pas vide ou si pas xp
        # si True, on ne peut pas aller dans cette direction
        # si False, on peut aller dans cette direction

        if position not in self.map:
            return True
        if self.map[position] not in [MAP_EMPTY, MAP_XP]:
            return True
        # check if adjacent cells are empty or xp
        if self.map[(position[0] - 1, position[1])] is MAP_ENEMY:
            return True
        if self.map[(position[0] + 1, position[1])] is MAP_ENEMY:
            return True
        if self.map[(position[0], position[1] - 1)] is MAP_ENEMY:
            return True
        if self.map[(position[0], position[1] + 1)] is MAP_ENEMY:
            return True
        if self.map[(position[0] + 1, position[1] + 1)] is MAP_ENEMY:
            return True
        if self.map[(position[0] - 1, position[1] - 1)] is MAP_ENEMY:
            return True
        return False

    def update_player(self, agent):
        agent.agent_sprite.center_x, agent.agent_sprite.center_y = state_to_xy(self.position)
        agent.state = self.position
