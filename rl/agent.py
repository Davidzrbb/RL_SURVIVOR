from typing import Tuple

import arcade
from constants import *
import random


class Agent:
    def __init__(self, window, env):
        print("Agent init")
        self.agent_sprite = None
        self.agent = None
        self.env = env
        self.setup()
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
        self.health: int = PLAYER_HEALTH

    def setup(self):
        self.agent = arcade.SpriteList()
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
        self.indicator_bar.bar_list.draw()

    def update(self, delta_time):
        self.indicator_bar.position = self.agent_sprite.center_x, self.agent_sprite.center_y + 25

    def state_to_xy(self, state):
        return (state[1] + 0.5) * SPRITE_SIZE, \
               (self.env.rows - state[0] - 0.5) * SPRITE_SIZE

    def map(self, state, value=None):
        if value is not None:
            self.env.map_object[state] = value
        return self.env.map_object[state]


class IndicatorBar:
    def __init__(
            self,
            owner: Agent,
            sprite_list: arcade.SpriteList,
            position: Tuple[float, float] = (0, 0),
            full_color: arcade.Color = arcade.color.GREEN,
            background_color: arcade.Color = arcade.color.BLACK,
            width: int = 100,
            height: int = 4,
            border_size: int = 4,
    ) -> None:
        self.owner: Agent = owner
        self.sprite_list: arcade.SpriteList = sprite_list

        self._box_width: int = width
        self._box_height: int = height
        self._half_box_width: int = self._box_width // 2
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._fullness: float = 0.0

        self._background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width + border_size,
            self._box_height + border_size,
            background_color,
        )
        self._full_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width,
            self._box_height,
            full_color,
        )

        self.bar_list: arcade.SpriteList = arcade.SpriteList()
        self.bar_list.append(self._background_box)
        self.bar_list.append(self._full_box)

        self.fullness: float = 1.0
        self.position: Tuple[float, float] = position

    @property
    def background_box(self) -> arcade.SpriteSolidColor:
        return self._background_box

    @property
    def full_box(self) -> arcade.SpriteSolidColor:
        return self._full_box

    @property
    def fullness(self) -> float:
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        if not (0.0 <= new_fullness <= 1.0):
            raise ValueError(
                f"Got {new_fullness}, but fullness must be between 0.0 and 1.0."
            )

        self._fullness = new_fullness
        if new_fullness == 0.0:
            self.full_box.visible = False
        else:
            self.full_box.visible = True
            self.full_box.width = self._box_width * new_fullness
            self.full_box.left = self._center_x - (self._box_width // 2)

    @property
    def position(self) -> Tuple[float, float]:
        return self._center_x, self._center_y

    @position.setter
    def position(self, new_position: Tuple[float, float]) -> None:
        if new_position != self.position:
            self._center_x, self._center_y = new_position
            self.background_box.position = new_position
            self.full_box.position = new_position
            self.full_box.left = self._center_x - (self._box_width // 2)
