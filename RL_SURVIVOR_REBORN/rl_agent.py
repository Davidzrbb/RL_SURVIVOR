import pickle
from os.path import exists

from rl.rl_agent import arg_max
from utils import state_to_xy, xy_to_state
from constants import *
from random import *


def sign(x):
    # Si x est strictement supérieur à 0, la fonction renvoie 1.
    # Si x est strictement inférieur à 0, la fonction renvoie -1.
    # Si x est égal à 0, la fonction renvoie 0.
    return 1 if x > 0 else -1 if x < 0 else 0


class ReinforcementLearning:
    def __init__(self, learning_rate=1, discount_factor=0.9):
        self.goal = {}
        self.position_agent = AGENT_POS
        self.map = {}
        self.state = ()
        self.neighbors_average = []
        for i in range(-3, 4):
            for j in range(-3, 4):
                if i != 0 and j != 0:
                    self.neighbors_average.append((i, j))
        self.reset()
        self.qtable = {}
        self.add_state(self.state)
        self.iteration = 0
        self.score = 0
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.history = []
        self.noise = 0

    def get_radar(self, position_agent):
        row, col = position_agent[0], position_agent[1]
        neighbors_average = []
        neighbors_close = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for n in self.neighbors_average:
            neighbors_average.append((row + n[0], col + n[1]))
        neighbor_categories = [neighbors_average, neighbors_close]
        radar = []
        for category in neighbor_categories:
            for n in category:
                # si la case est dans la map, on ajoute la valeur de la case dans radar
                if n in self.map:
                    radar.append(self.map[n])
                else:
                    # si la case n'est pas dans la map, on ajoute MAP_WALL dans radar
                    radar.append(MAP_WALL)

        radar_goal = [0] * 9
        for id in self.goal:
            delta_row = sign(self.goal[id][0] - row) + 1
            delta_col = sign(self.goal[id][0] - col) + 1
            position = delta_row * 3 + delta_col
            radar_goal[position] = 1
        return tuple(radar + radar_goal)

    def reset(self):
        self.position_agent = AGENT_POS
        self.score = 0
        self.iteration = 0
        self.map = {}
        self.goal = {}
        self.state = self.get_radar(self.position_agent)

    def add_state(self, state):
        if state not in self.qtable:
            self.qtable[state] = {}
            for action in ACTIONS:
                self.qtable[state][action] = 0.0

    def do(self, map_actual, coin_id_to_pos):
        self.goal = coin_id_to_pos
        self.map = map_actual
        action = self.best_action()
        self.position_agent, reward = self.move(self.position_agent, action)
        new_state = self.get_radar(self.position_agent)
        print("new_state", new_state)
        self.score += reward
        self.iteration += 1
        # Q-learning
        self.add_state(new_state)
        maxQ = max(self.qtable[new_state].values())
        delta = self.learning_rate * (reward + self.discount_factor * maxQ \
                                      - self.qtable[self.state][action])
        self.qtable[self.state][action] += delta
        self.state = new_state

        if self.position_agent in self.goal.values():
            self.history.append(self.score)
            self.noise *= 1 - 1E-1

        return action, reward

    def best_action(self):
        if random() < self.noise:
            return choice(ACTIONS)
        else:
            return arg_max(self.qtable[self.state])

    def move(self, position, action):
        move = MOVES[action]
        new_position = (position[0] + move[0], position[1] + move[1])
        if self.is_not_allowed(new_position):
            reward = REWARD_WALL
            new_position = position
        else:
            if new_position in self.goal:
                reward = REWARD_GOAL
            else:
                reward = REWARD_DEFAULT

        return [new_position, reward]

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

    def load(self, filename):
        if exists(filename):
            with open(filename, 'rb') as file:
                self.qtable = pickle.load(file)
            self.reset()

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.qtable, file)

    def update_player(self, agent):
        agent.agent_sprite.center_x, agent.agent_sprite.center_y = state_to_xy(self.position_agent)
        agent.state = self.position_agent
