import pickle
from os.path import exists
from time import sleep

from utils import state_to_xy, xy_to_state
from constants import *
from random import *


def sign(x):
    # Si x est strictement supérieur à 0, la fonction renvoie 1.
    # Si x est strictement inférieur à 0, la fonction renvoie -1.
    # Si x est égal à 0, la fonction renvoie 0.
    return 1 if x > 0 else -1 if x < 0 else 0


def arg_max(table):
    return max(table, key=table.get)


class ReinforcementLearning:
    def __init__(self, learning_rate=0.5, discount_factor=0.5):
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
        self.noise = 1

    def get_radar(self, position_agent):
        row, col = position_agent[0], position_agent[1]
        neighbors_average = []
        neighbors_close = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for n in self.neighbors_average:
            neighbors_average.append((row + n[0], col + n[1]))
        neighbor_categories = [neighbors_close, neighbors_average]
        radar = []
        for n in neighbors_close:
            if n in self.map:
                if self.map[n] == MAP_XP or self.map[n] == MAP_EMPTY or self.map[n] == MAP_ENEMY:
                    radar.append(self.map[n])

                else:
                    radar.append(MAP_EMPTY)
            else:
                radar.append(MAP_EMPTY)
        for n in range(0, len(neighbors_average)):
            list_case_value = []
            if neighbors_average[n] in self.map:
                list_case_value.append(self.map[neighbors_average[n]])
                if n % 9 == 0 and n != 0:
                    if MAP_ENEMY in list_case_value:
                        radar.append(MAP_ENEMY)
                    elif MAP_XP in list_case_value:
                        radar.append(MAP_XP)
                    else:
                        radar.append(MAP_EMPTY)
                    list_case_value.clear()
            else:
                continue
        return tuple(radar)

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
        self.score += reward
        self.iteration += 1
        # Q-learning
        self.add_state(new_state)
        maxQ = max(self.qtable[new_state].values())
        delta = self.learning_rate * (reward + self.discount_factor * maxQ
                                      - self.qtable[self.state][action])
        self.qtable[self.state][action] += delta
        self.state = new_state

        return action, reward

    def save_history(self):
        self.history.append(self.score)
        self.noise *= 1 - 0.05
        print("noise: ", self.noise)

    def best_action(self):
        if random() < self.noise:
            return choice(ACTIONS)
        else:
            return arg_max(self.qtable[self.state])

    def move(self, position, action):
        move = MOVES[action]
        new_position = (position[0] + move[0], position[1] + move[1])
        reward = self.is_not_allowed(new_position)
        print("reward: ", reward)
        if reward in [REWARD_ENEMY, REWARD_NEAR_ENEMY, False]:
            new_position = position

        return [new_position, reward]

    def is_not_allowed(self, position):
        # si pas dans la map ou si pas vide ou si pas xp
        # si True, on ne peut pas aller dans cette direction
        # si False, on peut aller dans cette direction
        if position not in self.map:
            return REWARD_ENEMY
        if self.map[position] == MAP_XP:
            return REWARD_GOAL
        if self.map[position] == MAP_ENEMY:
            return REWARD_ENEMY
        if self.map[position] == MAP_EMPTY:
            return REWARD_DEFAULT
        # check if adjacent cells are enemy or xp
        if position[0] + 1 == 20 or position[1] + 1 == 30 or position[0] - 1 == -1 or position[1] - 1 == -1:
            return REWARD_DEFAULT
        if self.map[(position[0] - 1, position[1])] == MAP_XP:
            return REWARD_NEAR_GOAL
        if self.map[(position[0] + 1, position[1])] == MAP_XP:
            return REWARD_NEAR_GOAL
        if self.map[(position[0], position[1] - 1)] == MAP_XP:
            return REWARD_NEAR_GOAL
        if self.map[(position[0], position[1] + 1)] == MAP_XP:
            return REWARD_NEAR_GOAL
        if self.map[(position[0] + 1, position[1] + 1)] == MAP_XP:
            return REWARD_NEAR_GOAL
        if self.map[(position[0] - 1, position[1] - 1)] == MAP_XP:
            return REWARD_NEAR_GOAL
        if self.map[(position[0] - 1, position[1] + 1)] == MAP_XP:
            return REWARD_NEAR_GOAL
        if self.map[(position[0] + 1, position[1] - 1)] == MAP_XP:
            return REWARD_NEAR_GOAL
        if self.map[(position[0] - 1, position[1])] == MAP_ENEMY:
            return REWARD_NEAR_ENEMY
        if self.map[(position[0] + 1, position[1])] == MAP_ENEMY:
            return REWARD_NEAR_ENEMY
        if self.map[(position[0], position[1] - 1)] == MAP_ENEMY:
            return REWARD_NEAR_ENEMY
        if self.map[(position[0], position[1] + 1)] == MAP_ENEMY:
            return REWARD_NEAR_ENEMY
        if self.map[(position[0] + 1, position[1] + 1)] == MAP_ENEMY:
            return REWARD_NEAR_ENEMY
        if self.map[(position[0] - 1, position[1] - 1)] == MAP_ENEMY:
            return REWARD_NEAR_ENEMY
        if self.map[(position[0] - 1, position[1] + 1)] == MAP_ENEMY:
            return REWARD_NEAR_ENEMY
        if self.map[(position[0] + 1, position[1] - 1)] == MAP_ENEMY:
            return REWARD_NEAR_ENEMY

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
