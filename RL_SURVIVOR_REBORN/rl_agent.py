import pickle
from os.path import exists

from utils import state_to_xy
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
    def __init__(self, learning_rate=0.9, discount_factor=0.8):
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
        self.noise = 0.5
        self.health_value = 100

    def get_radar(self, position_agent):
        row, col = position_agent[0], position_agent[1]
        neighbors_average = []
        neighbors_close = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for n in self.neighbors_average:
            neighbors_average.append((row + n[0], col + n[1]))
        radar = []
        for n in neighbors_close:
            if n in self.map:
                if MAP_WALL == self.map[n] \
                        or MAP_WALL_T == self.map[n] \
                        or MAP_OBSTACLE == self.map[n] \
                        or MAP_OBSTACLE2 == self.map[n] \
                        or MAP_OBSTACLE3 == self.map[n]:
                    radar.append(MAP_EMPTY)
                else:
                    radar.append(self.map[n])
            else:
                # si la case n'est pas dans la map, on ajoute MAP_WALL dans radar
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
                    elif MAP_WALL in list_case_value \
                            or MAP_WALL_T in list_case_value \
                            or MAP_OBSTACLE in list_case_value \
                            or MAP_OBSTACLE2 in list_case_value \
                            or MAP_OBSTACLE3 in list_case_value:
                        radar.append(MAP_EMPTY)
                    else:
                        radar.append(MAP_EMPTY)
                    list_case_value.clear()
            else:
                radar.append(MAP_EMPTY)

        return tuple(radar)

    def reset(self):
        self.position_agent = AGENT_POS
        self.score = 0
        self.iteration = 0
        self.map = {}
        self.state = self.get_radar(self.position_agent)

    def add_state(self, state):
        if state not in self.qtable:
            self.qtable[state] = {}
            for action in ACTIONS:
                self.qtable[state][action] = 0.0

    def do(self, map_actual, health_bar):
        health_value_actual = health_bar.health_value
        self.map = map_actual
        action = self.best_action()
        self.position_agent, reward = self.move(self.position_agent, action)
        if health_value_actual < self.health_value:
            reward += REWARD_ENEMY
        self.health_value = health_value_actual
        new_state = self.get_radar(self.position_agent)
        self.score += reward
        self.iteration += 1
        # Q-learning
        self.add_state(new_state)
        maxQ = max(self.qtable[new_state].values())
        delta = self.learning_rate * (reward + self.discount_factor * maxQ - self.qtable[self.state][action])
        self.qtable[self.state][action] += delta
        self.state = new_state

        return action, reward

    def save_history(self):
        self.history.append(self.score)
        self.noise -= 0.05
        print('noise :', self.noise)
        print('score :', self.score)

    def best_action(self):
        if random() < self.noise:
            return choice(ACTIONS)
        else:
            return arg_max(self.qtable[self.state])

    def move(self, position, action):
        move = MOVES[action]
        new_position = (position[0] + move[0], position[1] + move[1])
        reward = self.is_not_allowed(new_position)
        if reward == REWARD_WALL or reward == REWARD_ENEMY:
            # bouge pas
            new_position = position
        if reward == REWARD_WALL:
            reward = REWARD_DEFAULT

        return [new_position, reward]

    def is_not_allowed(self, position):
        if position not in self.map:
            return REWARD_ENEMY

        if position[0] < 2 or position[1] < 2 or position[0] > GRID_HEIGHT - 3 or position[1] > GRID_WIDTH - 3:
            return REWARD_WALL

        if self.map[position] == MAP_WALL or \
                self.map[position] == MAP_WALL_T or \
                self.map[position] == MAP_OBSTACLE or \
                self.map[position] == MAP_OBSTACLE2 or \
                self.map[position] == MAP_OBSTACLE3:
            return REWARD_WALL

        if self.map[position] == MAP_ENEMY:
            return REWARD_ENEMY

        if self.map[position] == MAP_XP:
            return REWARD_GOAL

        return REWARD_DEFAULT

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
