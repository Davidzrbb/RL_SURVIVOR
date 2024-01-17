import arcade

from constants import *
import random

from game_environment.indicator_bar import IndicatorBar


class Agent:
    def __init__(self, window, env):
        self.agent_sprite = None
        self.bullet_sprite = None
        self.agent = None
        self.bullet = None
        self.total_time = 0.0
        self.env = env
        self.bar_list = None
        self.indicator_bar = None
        self.health: int = PLAYER_HEALTH
        self.window = window
        self.setup()

    def setup(self):
        self.agent = arcade.SpriteList()
        self.total_time = 0.0
        self.bullet = arcade.SpriteList()
        self.bar_list = arcade.SpriteList()
        self.indicator_bar = IndicatorBar(
            owner=self,
            sprite_list=self.bar_list,
            position=(0, 0),
            full_color=arcade.color.GREEN,
            background_color=arcade.color.BLACK,
            width=100,
            height=4,
            border_size=4,
        )
        self.agent_sprite = arcade.Sprite(
            ":resources:images/animated_characters/male_adventurer/maleAdventurer_walk0.png", SPRITE_SCALING * 1.5)

        empty_cells = [state for state in self.env.states if self.is_empty_and_adjacent(state)]
        if empty_cells:
            random_empty_cell = random.choice(empty_cells)
            self.agent_sprite.center_x, self.agent_sprite.center_y = self.state_to_xy(random_empty_cell)
            self.map(random_empty_cell, MAP_AGENT)
        else:
            print("Error: No suitable cells in the environment")

        self.agent.append(self.agent_sprite)
        self.add_bullet()

    def add_bullet(self):
        self.bullet_sprite = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING * 5)
        self.bullet_sprite.center_x, self.bullet_sprite.center_y = self.agent_sprite.center_x, self.agent_sprite.center_y
        self.bullet.append(self.bullet_sprite)

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
        self.bullet.draw()
        self.indicator_bar.bar_list.draw()

    def update(self, delta_time):
        self.indicator_bar.position = self.agent_sprite.center_x, self.agent_sprite.center_y + 25
        # the bullet move to the end of the map and then disappear
        if self.bullet_sprite.center_x > self.window.width or self.bullet_sprite.center_y > self.window.height or \
                self.bullet_sprite.center_x < 0 or self.bullet_sprite.center_y < 0:
            self.bullet_sprite.remove_from_sprite_lists()
        self.total_time += delta_time
        if self.total_time > RELOAD_BULLET_TIME:
            self.add_bullet()
            self.total_time = 0.0

        for bullet in self.bullet:
            bullet.center_x += BULLET_SPEED

    def state_to_xy(self, state):
        return (state[1] + 0.5) * SPRITE_SIZE, \
               (self.env.rows - state[0] - 0.5) * SPRITE_SIZE

    def map(self, state, value=None):
        if value is not None:
            self.env.map_object[state] = value
        return self.env.map_object[state]
