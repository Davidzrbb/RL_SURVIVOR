import arcade
from constants import *
import random


class Agent:
    def __init__(self, window, env):
        self.agent_sprite = None
        self.agent = None
        self.env = env
        self.setup()

    def setup(self):
        self.agent = arcade.SpriteList()
        self.agent_sprite = arcade.Sprite(
            ":resources:images/animated_characters/male_adventurer/maleAdventurer_walk0.png", SPRITE_SCALING * 1.5)

        empty_cells = [state for state in self.env.states if self.is_empty_and_adjacent(state)]
        if empty_cells:
            random_empty_cell = random.choice(empty_cells)
            self.agent_sprite.center_x, self.agent_sprite.center_y = self.state_to_xy(random_empty_cell)
            self.map(random_empty_cell, MAP_AGENT)  # Mark the chosen cell as MAP_AGENT
        else:
            # Handle the case where there are no suitable cells in the environment
            print("Error: No suitable cells in the environment")

        self.agent.append(self.agent_sprite)

    def is_empty_and_adjacent(self, state):
        adjacent_states = [
            (state[0] + 1, state[1]),
            (state[0] - 1, state[1]),
            (state[0], state[1] + 1),
            (state[0], state[1] - 1),
            (state[0] + 1, state[1] + 1),
            (state[0] - 1, state[1] - 1),
            (state[0] + 1, state[1] - 1),
            (state[0] - 1, state[1] + 1)
        ]

        valid_adjacent_states = [
            adj_state for adj_state in adjacent_states
            if 0 <= adj_state[0] < self.env.rows and 0 <= adj_state[1] < self.env.cols
        ]

        return all(self.map(adj_state) == MAP_EMPTY for adj_state in valid_adjacent_states) and self.map(
            state) == MAP_EMPTY

    def on_draw(self):
        self.agent.draw()

    def state_to_xy(self, state):
        return (state[1] + 0.5) * SPRITE_SIZE, \
               (self.env.rows - state[0] - 0.5) * SPRITE_SIZE

    def map(self, state, value=None):
        if value is not None:
            self.env.map_object[state] = value
        return self.env.map_object[state]
