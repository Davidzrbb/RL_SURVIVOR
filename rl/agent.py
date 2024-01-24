import arcade

from constants import *
import random

from game_environment.indicator_bar import IndicatorBar
from game_environment.indicator_xp_bar import IndicatorXPBar


class Agent:
    def __init__(self, window, env):
        self.radar_list = None
        self.neighbors_average = []
        self.neighbors_far = []
        self.neighbors_close = []
        self.indicator_xp_bar = None
        self.agent_sprite = None
        self.radar_sprite = None
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
        self.radar_list = arcade.SpriteList()
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
        self.indicator_xp_bar = IndicatorXPBar(
            owner=self,
            sprite_list=self.bar_list,
            position=(0, 0),
            full_color=arcade.color.AZURE,
            background_color=arcade.color.BLACK,
            width=100,
            height=4,
            border_size=4,
        )

        self.indicator_xp_bar.fullness = 0.01
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
        count = 0
        self.neighbors_close = [(self.agent_sprite.center_x, self.agent_sprite.center_y),
                                (self.agent_sprite.center_x, self.agent_sprite.center_y),
                                (self.agent_sprite.center_x, self.agent_sprite.center_y),
                                (self.agent_sprite.center_x, self.agent_sprite.center_y)]
        while count < len(self.neighbors_close):
            self.radar_sprite = arcade.Sprite(":resources:images/tiles/lava.png", SPRITE_SCALING)
            self.radar_list.append(self.radar_sprite)
            count += 1
        count = 0
        while count < len(self.neighbors_average):
            self.radar_sprite = arcade.Sprite(":resources:images/tiles/lava.png", SPRITE_SCALING)
            self.radar_list.append(self.radar_sprite)
            count += 1

    def add_bullet(self):
        self.bullet_sprite = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING * 5)
        self.bullet_sprite.center_x, self.bullet_sprite.center_y = self.agent_sprite.center_x + 30, self.agent_sprite.center_y
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
        # self.indicator_xp_bar.draw_level_indicator()
        self.indicator_xp_bar.bar_list.draw()
        self.radar_list.draw()

    def update(self, delta_time):
        self.indicator_bar.position = self.agent_sprite.center_x, self.agent_sprite.center_y + 35
        self.indicator_xp_bar.position = self.agent_sprite.center_x, self.agent_sprite.center_y + 25
        # the bullet move to the end of the map and then disappear
        if self.bullet_sprite.center_x > self.window.width or self.bullet_sprite.center_y > self.window.height or \
                self.bullet_sprite.center_x < 0 or self.bullet_sprite.center_y < 0:
            self.bullet_sprite.kill()
        self.total_time += delta_time
        if self.total_time > get_bullet_time():
            self.add_bullet()
            self.total_time = 0.0

        for bullet in self.bullet:
            bullet.center_x += BULLET_SPEED
        for radar in range(len(self.radar_list)):
            if radar == 0:
                self.radar_list[radar].center_x, self.radar_list[
                    radar].center_y = self.agent_sprite.center_x - self.agent_sprite.height, \
                    self.agent_sprite.center_y
            elif radar == 1:
                self.radar_list[radar].center_x, self.radar_list[
                    radar].center_y = self.agent_sprite.center_x + self.agent_sprite.height, \
                    self.agent_sprite.center_y
            elif radar == 2:
                self.radar_list[radar].center_x, self.radar_list[radar].center_y = self.agent_sprite.center_x, \
                    self.agent_sprite.center_y - self.agent_sprite.height
            elif radar == 3:
                self.radar_list[radar].center_x, self.radar_list[radar].center_y = self.agent_sprite.center_x, \
                    self.agent_sprite.center_y + self.agent_sprite.height
            elif radar >= 4:
                self.radar_list[radar].center_x, self.radar_list[radar].center_y = self.agent_sprite.center_x + \
                                                                                   self.neighbors_average[
                                                                                       radar - 5][
                                                                                       0] * self.agent_sprite.height, \
                                                                                   self.agent_sprite.center_y + \
                                                                                   self.neighbors_average[
                                                                                       radar - 5][
                                                                                       1] * self.agent_sprite.height

    def state_to_xy(self, state):
        return (state[1] + 0.5) * SPRITE_SIZE, \
               (self.env.rows - state[0] - 0.5) * SPRITE_SIZE

    def map(self, state, value=None):
        if value is not None:
            self.env.map_object[state] = value
        return self.env.map_object[state]
