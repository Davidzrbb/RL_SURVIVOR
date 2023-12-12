import arcade
from constants import *


class Agent:
    def __init__(self, window, env):
        self.agent_sprite = None
        self.agent = None
        self.env = env
        self.setup()

    def setup(self):
        # Create the Sprite lists
        self.agent = arcade.SpriteList()
        # Set up the player
        self.agent_sprite = arcade.Sprite(
            ":resources:images/animated_characters/male_adventurer/maleAdventurer_walk0.png", SPRITE_SCALING * 1.5)
        for state in self.env.states:
            if self.map(state) == MAP_AGENT:
                self.agent_sprite.center_x, self.agent_sprite.center_y = self.state_to_xy(state)
                break
        self.agent.append(self.agent_sprite)

    def on_draw(self):
        self.agent.draw()

    def state_to_xy(self, state):
        return (state[1] + 0.5) * SPRITE_SIZE, \
               (self.env.rows - state[0] - 0.5) * SPRITE_SIZE

    def map(self, state):
        if self.env.map_object[state] == MAP_EMPTY:
            self.env.map_object[state] = MAP_AGENT
        return self.env.map_object[state]
