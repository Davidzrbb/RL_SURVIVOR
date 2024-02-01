import arcade
from constants import *
from utils import state_to_xy
import copy


class Bullet:
    def __init__(self):
        self.bullet_sprite = None
        self.bullet_sprite_list = arcade.SpriteList()
        self.bullet_id_to_sprite = {}
        self.bullet_id_to_pos = {}
        self.total_time = 0.0
        self.bullet_last_pop = []

        # id -> sprite
        # id ==
        # id -> pos

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
                self.bullet_id_to_pos[id] = self.bullet_id_to_pos[id][0], self.bullet_id_to_pos[id][1] + 1
                self.bullet_id_to_sprite[id].center_x, self.bullet_id_to_sprite[id].center_y = state_to_xy(
                    self.bullet_id_to_pos[id])

    def add_bullet(self, agent):
        self.bullet_sprite = arcade.Sprite(
            ":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING * 5)
        self.bullet_sprite.center_x, self.bullet_sprite.center_y = state_to_xy(agent.state)

        if (len(self.bullet_last_pop) == 0):
            self.bullet_id_to_pos[len(self.bullet_id_to_pos)] = agent.state
            self.bullet_id_to_sprite[len(self.bullet_id_to_sprite)] = self.bullet_sprite
        else:
            self.bullet_id_to_pos[self.bullet_last_pop[0]] = agent.state
            self.bullet_id_to_sprite[self.bullet_last_pop[0]] = self.bullet_sprite
            self.bullet_last_pop.pop(0)

        self.bullet_sprite_list.append(self.bullet_sprite)
