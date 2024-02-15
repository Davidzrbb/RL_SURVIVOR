import arcade
from constants import *
from utils import state_to_xy


class HealthBar:
    def __init__(self):
        self.empty_box = None
        self.hp_box = None
        self.health_bar_list = arcade.SpriteList()
        self.health_value = 100
        self.setup()

    def setup(self):
        self.health_value = 100

        self.empty_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            102,
            6,
            arcade.color.BLACK,
        )
        self.hp_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self.health_value,
            4,
            arcade.color.GREEN,
        )

        self.health_bar_list: arcade.SpriteList = arcade.SpriteList()
        self.health_bar_list.append(self.empty_box)
        self.health_bar_list.append(self.hp_box)

    def on_draw(self):
        self.health_bar_list.draw()

    def update(self, agent):
        self.empty_box.center_x, self.empty_box.center_y = agent.agent_sprite.center_x, agent.agent_sprite.center_y + 30
        if self.health_value <= 0:
            self.hp_box.width = 0.1
        else:
            self.hp_box.width = self.health_value
        self.hp_box.center_x, self.hp_box.center_y = (
            (agent.agent_sprite.center_x - 50) + (self.health_value / 2), agent.agent_sprite.center_y + 30)

    def loose_hp(self):
        self.health_value -= 10

    def game_over(self):
        return self.health_value <= 0
