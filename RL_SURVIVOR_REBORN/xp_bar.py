import arcade
from constants import *
from utils import state_to_xy

class XpBar:
    def __init__(self):
        self.empty_box = None
        self.xp_box = None
        self.xp_bar_list = arcade.SpriteList()
        self.xp_value = 0
        self.setup()

    def setup(self):

        self.empty_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            102,
            6,
            arcade.color.BLACK,
        )

        self.xp_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self.xp_value,
            4,
            arcade.color.AZURE,
        )

        self.xp_bar_list: arcade.SpriteList = arcade.SpriteList()
        self.xp_bar_list.append(self.empty_box)
        self.xp_bar_list.append(self.xp_box)

    def on_draw(self):
       self.xp_bar_list.draw()

    def update(self, agent):
       self.empty_box.center_x, self.empty_box.center_y = agent.agent_sprite.center_x, agent.agent_sprite.center_y + 20
       self.xp_box.center_x, self.xp_box.center_y = ((agent.agent_sprite.center_x - 50) + (self.xp_value/2), agent.agent_sprite.center_y + 20)
        

        
    

        