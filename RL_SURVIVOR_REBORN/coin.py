import arcade

from constants import *
from utils import state_to_xy


class Coin:
    def __init__(self):
        self.coin_sprite = None
        self.coin_sprite_list = arcade.SpriteList()
        self.coin_id_to_pos = {}
        self.coin_id_to_sprite = {}

    def setup(self):
        self.coin_sprite_list = arcade.SpriteList()
        self.coin_id_to_pos = {}
        self.coin_id_to_sprite = {}

    def on_draw(self):
        self.coin_sprite_list.draw()

    def add_coin(self, id, state):
        self.coin_sprite = arcade.Sprite(
            ":resources:images/items/coinGold.png", SPRITE_SCALING)
        self.coin_sprite.center_x, self.coin_sprite.center_y = state_to_xy(state)
        self.coin_sprite_list.append(self.coin_sprite)
        self.coin_id_to_pos[id] = state
        self.coin_id_to_sprite[id] = self.coin_sprite
