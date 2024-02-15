import arcade
from constants import *
from utils import state_to_xy


class XpBar:
    def __init__(self):
        self.empty_box = None
        self.xp_box = None
        self.xp_bar_list = arcade.SpriteList()
        self.xp_value = 1
        self.xp_level = 1
        self.sprite_level_x = None
        self.sprite_level_y = None
        self.setup()

    def setup(self):
        self.xp_value = 1
        self.xp_level = 1
        self.empty_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            102,
            6,
            arcade.color.BLACK,
        )

        self.xp_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            1,
            4,
            arcade.color.AZURE,
        )

        self.xp_bar_list: arcade.SpriteList = arcade.SpriteList()
        self.xp_bar_list.append(self.empty_box)
        self.xp_bar_list.append(self.xp_box)

    def on_draw(self):
        self.xp_bar_list.draw()
        arcade.draw_text(
            text=self.xp_level,
            start_x=self.sprite_level_x,
            start_y=self.sprite_level_y,
            color=arcade.color.RED,
            font_size=10,
            width=(GRID_WIDTH * SPRITE_SIZE),
            anchor_x="center",
            anchor_y="center",
        )

    def update(self, agent):
        self.empty_box.center_x, self.empty_box.center_y = agent.agent_sprite.center_x, agent.agent_sprite.center_y + 20

        self.xp_box.width = self.xp_value
        self.xp_box.center_x, self.xp_box.center_y = (
            (agent.agent_sprite.center_x - 50) + (self.xp_value / 2), agent.agent_sprite.center_y + 20)

        self.sprite_level_x = agent.agent_sprite.center_x - 60
        self.sprite_level_y = agent.agent_sprite.center_y + 20

    def add_xp(self):
        self.bool = True

        self.xp_value += (100 / (self.xp_level * 2))
        if self.xp_value >= 100:
            self.xp_value -= 100
            self.xp_level += 1

            set_bullet_time(get_bullet_time() - 0.5)


