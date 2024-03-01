import uuid

import arcade
from constants import *
from utils import state_to_xy, xy_to_state
import copy


class Bullet:
    def __init__(self):
        self.bullet_sprite_bottom = None
        self.bullet_sprite_top = None
        self.bullet_sprite_left = None
        self.bullet_sprite_right = None
        self.bullet_sprite_list = arcade.SpriteList()
        self.bullet_id_to_sprite = {}
        self.bullet_id_to_pos = {}
        self.bullet_id_to_direction = {}
        self.total_time = 0.0
        self.bullet_last_pop = []

    def setup(self):
        set_bullet_time(3)
        self.bullet_sprite_list = arcade.SpriteList()
        self.bullet_id_to_sprite = {}
        self.bullet_id_to_pos = {}
        self.total_time = 0.0
        self.bullet_last_pop = []

    def on_draw(self):
        self.bullet_sprite_list.draw()

    def update(self, delta_time, window, agent):
        # the bullet move to the end of the map and then disappear
        self.total_time += delta_time
        if self.total_time > get_bullet_time():
            self.add_bullet(agent)
            self.total_time = 0.0
        for id in copy.deepcopy(self.bullet_id_to_pos):
            if self.bullet_id_to_pos[id][1] > GRID_WIDTH:
                self.bullet_id_to_sprite[id].kill()
                self.bullet_last_pop.append(id)
                self.bullet_id_to_pos.pop(id)
                self.bullet_id_to_sprite.pop(id)
            else:
                if self.bullet_id_to_direction[id] == "right":
                    self.bullet_id_to_sprite[id].center_x += BULLET_SPEED
                if self.bullet_id_to_direction[id] == "left":
                    self.bullet_id_to_sprite[id].center_x -= BULLET_SPEED
                if self.bullet_id_to_direction[id] == "top":
                    self.bullet_id_to_sprite[id].center_y += BULLET_SPEED
                if self.bullet_id_to_direction[id] == "bottom":
                    self.bullet_id_to_sprite[id].center_y -= BULLET_SPEED
                self.bullet_id_to_pos[id] = xy_to_state(self.bullet_id_to_sprite[id].center_x,
                                                        self.bullet_id_to_sprite[id].center_y)

    def add_bullet(self, agent):
        # to right
        self.bullet_sprite_right = arcade.Sprite(
            ":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING * 5)
        self.bullet_sprite_right.center_x, self.bullet_sprite_right.center_y = state_to_xy(
            (agent.state[0], agent.state[1] + 1))
        # to left
        self.bullet_sprite_left = arcade.Sprite(
            ":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING * 5, angle=180)
        self.bullet_sprite_left.center_x, self.bullet_sprite_left.center_y = state_to_xy(
            (agent.state[0], agent.state[1] - 1))
        # to top
        self.bullet_sprite_top = arcade.Sprite(
            ":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING * 5, angle=90)
        self.bullet_sprite_top.center_x, self.bullet_sprite_top.center_y = state_to_xy(
            (agent.state[0] + 1, agent.state[1]))
        # to bottom
        self.bullet_sprite_bottom = arcade.Sprite(
            ":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING * 5, angle=-90)
        self.bullet_sprite_bottom.center_x, self.bullet_sprite_bottom.center_y = state_to_xy(
            (agent.state[0] - 1, agent.state[1]))

        id = uuid.uuid4()
        self.bullet_id_to_sprite[id] = self.bullet_sprite_right
        self.bullet_id_to_pos[id] = xy_to_state(self.bullet_sprite_right.center_x, self.bullet_sprite_right.center_y)
        self.bullet_id_to_direction[id] = "right"
        id = uuid.uuid4()
        self.bullet_id_to_sprite[id] = self.bullet_sprite_left
        self.bullet_id_to_pos[id] = xy_to_state(self.bullet_sprite_left.center_x, self.bullet_sprite_left.center_y)
        self.bullet_id_to_direction[id] = "left"
        id = uuid.uuid4()
        self.bullet_id_to_sprite[id] = self.bullet_sprite_top
        self.bullet_id_to_pos[id] = xy_to_state(self.bullet_sprite_top.center_x, self.bullet_sprite_top.center_y)
        self.bullet_id_to_direction[id] = "top"
        id = uuid.uuid4()
        self.bullet_id_to_sprite[id] = self.bullet_sprite_bottom
        self.bullet_id_to_pos[id] = xy_to_state(self.bullet_sprite_bottom.center_x, self.bullet_sprite_bottom.center_y)
        self.bullet_id_to_direction[id] = "bottom"

        self.bullet_sprite_list.append(self.bullet_sprite_right)
        self.bullet_sprite_list.append(self.bullet_sprite_left)
        self.bullet_sprite_list.append(self.bullet_sprite_top)
        self.bullet_sprite_list.append(self.bullet_sprite_bottom)
