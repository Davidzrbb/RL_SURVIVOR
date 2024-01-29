import arcade
from constants import *
from utils import state_to_xy
import random


class Agent:

    def __init__(self):
        self.agent_sprite = None
        self.agent_list = arcade.SpriteList()
        self.state = (1,1)

        self.setup()
        
    def setup(self):
        self.agent_list = arcade.SpriteList(use_spatial_hash=True)
        self.agent_sprite = arcade.Sprite(
            ":resources:images/animated_characters/male_adventurer/maleAdventurer_walk0.png", SPRITE_SCALING)
        self.agent_sprite.center_x, self.agent_sprite.center_y = state_to_xy(self.state)
        self.agent_list.append(self.agent_sprite)

    def on_draw(self):
        self.agent_list.draw()

    def update(self):
        direction = random.randint(0,4)          
        self.state = direction, direction
        self.agent_sprite.center_x, self.agent_sprite.center_y = state_to_xy((self.state))