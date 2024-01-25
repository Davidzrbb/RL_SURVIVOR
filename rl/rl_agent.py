import pickle
from os.path import exists

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
    def __init__(self, env, agent, rl, learning_rate=1, discount_factor=0.9):
        self.neighbors_close = None
        self.state = None
        self.iteration = None
        self.score = None
        row, col = 0, 0
        self.env = env
        self.agent = agent
        self.position = (1, 1)
        self.rl = rl
        self.map = rl.get_map()
        self.goal = rl.stack_map_tab
        self.neighbors_far = []
        self.qtable = {}

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.history = []
        self.noise = 0

        for i in range(-3, 4):
            for j in range(-7, 8):
                if j <= -4 or j >= 4:
                    self.neighbors_far.append((i, j))
        for i in range(-7, 8):
            for j in range(-3, 4):
                if i <= -5 or i >= 5:
                    self.neighbors_far.append((i, j))
        self.neighbors_average = []
        for i in range(-3, 4):
            for j in range(-3, 4):
                if i != 0 and j != 0:
                    self.neighbors_average.append((i, j))

        self.reset()
        self.add_state(self.state)

    def is_not_allowed(self, position):
        # si pas dans la map ou si pas vide ou si pas xp
        # si True, on ne peut pas aller dans cette direction
        # si False, on peut aller dans cette direction
        if position not in self.map:
            return True
        if self.map[position] not in [MAP_EMPTY, MAP_XP]:
            return True

        return False

    def get_radar(self, state):
        # position de l'agent
        row, col = state[0], state[1]
        neighbors_close = []
        neighbors_average = []
        neighbors_far = []

        self.neighbors_close = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for n in self.neighbors_average:
            neighbors_average.append((row + n[0], col + n[1]))
        for n in self.neighbors_far:
            neighbors_far.append((row + n[0], col + n[1]))

        radar = []
        neighbor_categories = [neighbors_far, neighbors_average, neighbors_close]
        self.map = self.rl.get_map()
        self.goal = self.rl.stack_map_tab
        for category in neighbor_categories:
            for n in category:
                # si la case est dans la map, on ajoute la valeur de la case dans radar
                if n in self.map:
                    radar.append(self.map[n])
                else:
                    # si la case n'est pas dans la map, on ajoute MAP_WALL dans radar
                    radar.append(MAP_WALL)
        radar_goal = [0] * 9
        if len(self.goal) != 0:
            # (1 - 0) = 1  + 1 = 2
            delta_row = sign(list(self.goal.keys())[0][0] - row) + 1
            # (2 - 0) = 1 + 1 = 2
            delta_col = sign(list(self.goal.keys())[0][1] - col) + 1
            position = delta_row * 3 + delta_col  # 2 * 3 + 2 = 8
            radar_goal[position] = 1  # radar_goal[8] = 1
        return tuple(radar + radar_goal)

    def do(self, position, action):
        move = MOVES[action]
        new_position = (position[0] + move[0], position[1] + move[1])
        if self.is_not_allowed(new_position):
            reward = REWARD_WALL
        else:
            position = new_position
            if position in self.goal:
                reward = REWARD_GOAL
            else:
                reward = REWARD_DEFAULT

        return self.get_radar(position), position, reward

    def reset(self):
        self.position = (1, 1)
        self.score = 0
        self.iteration = 0
        self.state = self.get_radar(self.position)

    def best_action(self):
        # la meilleure action à faire en fonction de la qtable
        # ou de faire une action aléatoire
        if random() < self.noise:
            return choice(ACTIONS)
        else:
            if self.state in self.qtable:
                return arg_max(self.qtable[self.state])
            else:
                # Handle missing key
                return choice(ACTIONS)

    def add_state(self, state):
        if state not in self.qtable:
            self.qtable[state] = {}
            for action in ACTIONS:
                self.qtable[state][action] = 0.0

    def do1(self):
        action = self.best_action()
        new_state, position, reward = self.do(self.position, action)
        self.score += reward
        self.iteration += 1
        self.position = position
        # Q-learning
        self.add_state(new_state)
        maxQ = max(self.qtable[new_state].values())
        delta = self.learning_rate * (reward + self.discount_factor * maxQ \
                                      - self.qtable[self.state][action])
        self.qtable[self.state][action] += delta
        self.state = new_state
        # if self.position == self.goal:
        #     self.history.append(self.score)
        #     self.noise *= 1 - 1E-1

        return action, reward

    def load(self, filename):
        if exists(filename):
            with open(filename, 'rb') as file:
                self.qtable = pickle.load(file)
            self.reset()

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.qtable, file)

    def state_to_xy(self, state):
        return (state[1] + 0.5) * SPRITE_SIZE, \
               (GRID_HEIGHT - state[0] - 0.5) * SPRITE_SIZE

    def update_player(self):
        self.agent.agent_sprite.center_x, self.agent.agent_sprite.center_y = self.state_to_xy(self.position)
