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
    def __init__(self, env, agent, learning_rate=1, discount_factor=0.9):
        self.neighbors_close = None
        self.state = None
        self.iteration = None
        self.score = None
        self.position = None
        row, col = 0, 0
        self.env = env
        self.agent = agent
        self.map = env.map
        self.goal = (row, col)
        self.neighbors_far = []
        self.reset()
        self.qtable = {}
        self.add_state(self.state)

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

    def reset(self):
        self.position = env.start
        self.score = 0
        self.iteration = 0
        self.state = self.env.get_radar(self.position)

    def best_action(self):
        if random() < self.noise:
            return choice(ACTIONS)
        else:
            return arg_max(self.qtable[self.state])

    def add_state(self, state):
        if state not in self.qtable:
            self.qtable[state] = {}
            for action in ACTIONS:
                self.qtable[state][action] = 0.0

    def is_not_allowed(self, position):
        # si pas dans la map ou si pas vide ou si pas xp
        # si True, on ne peut pas aller dans cette direction
        # si False, on peut aller dans cette direction
        return position not in self.map \
            or self.map[position] not in [MAP_EMPTY, MAP_XP]

    def get_radar(self, state):
        # position de l'agent
        row, col = state[0], state[1]
        neighbors_close = []
        neighbors_average = []
        neighbors_far = []
        self.neighbors_close = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for n in self.neighbors_close:
            neighbors_close.append((row + n[0], col + n[1]))
        for n in self.neighbors_average:
            neighbors_average.append((row + n[0], col + n[1]))
        for n in self.neighbors_far:
            neighbors_far.append((row + n[0], col + n[1]))
        radar = []
        for n in neighbors_far:
            # si la case est dans la map, on ajoute la valeur de la case dans radar
            if n in self.map:
                radar.append(self.map[n])
            else:
                # si la case n'est pas dans la map, on ajoute MAP_WALL dans radar
                radar.append(MAP_WALL)
        for n in neighbors_average:
            # si la case est dans la map, on ajoute la valeur de la case dans radar
            if n in self.map:
                radar.append(self.map[n])
            else:
                # si la case n'est pas dans la map, on ajoute MAP_WALL dans radar
                radar.append(MAP_WALL)
        for n in neighbors_close:
            # si la case est dans la map, on ajoute la valeur de la case dans radar
            if n in self.map:
                radar.append(self.map[n])
            else:
                # si la case n'est pas dans la map, on ajoute MAP_WALL dans radar
                radar.append(MAP_WALL)

        return radar

    def do(self, position, action):
        move = MOVES[action]
        new_position = (position[0] + move[0], position[1] + move[1])

        if self.is_not_allowed(new_position):
            reward = REWARD_WALL
        else:
            position = new_position
            if new_position == self.goal:
                reward = REWARD_GOAL
            else:
                reward = REWARD_DEFAULT

        return self.get_radar(position), position, reward
