import arcade
from constants import *
import random
from utils import state_to_xy, xy_to_state
import copy


class Enemy:

    def __init__(self, env):
        self.physics_engine_list = None
        self.barrier_list = None
        self.env = env
        self.enemy_sprite_list = None
        self.enemy_id_to_pos = {}
        self.playing_field_left_boundary = 0
        self.playing_field_right_boundary = GRID_WIDTH * SPRITE_SIZE  # ou une valeur appropriée
        self.playing_field_top_boundary = GRID_HEIGHT * SPRITE_SIZE  # ou une valeur appropriée
        self.playing_field_bottom_boundary = 0
        self.enemy_id_pos_removed = {}
        self.setup()

    def setup(self):
        self.enemy_id_to_pos = {}
        self.enemy_id_pos_removed = {}
    
        self.enemy_sprite_list = arcade.SpriteList()
        self.spawn_zombie()

        self.barrier_list = []
        self.physics_engine_list = []

        for sprite in self.enemy_sprite_list:
            barrier = arcade.AStarBarrierList(sprite, self.env.obstacle_list,
                                              SPRITE_SIZE,
                                              self.playing_field_left_boundary,
                                              self.playing_field_right_boundary,
                                              self.playing_field_bottom_boundary,
                                              self.playing_field_top_boundary)
            self.barrier_list.append(barrier)
            physics_engine = arcade.PhysicsEngineSimple(sprite,
                                                        self.enemy_sprite_list)
            self.physics_engine_list.append(physics_engine)

    def on_draw(self):
        self.enemy_sprite_list.draw()

    def spawn_zombie(self):
        cpt = 0
        while cpt < get_nb_enemies():

            direction = random.randint(0, 3)
            rand_sprite = random.randint(0, 1)
            sprite = None

            if (rand_sprite):
                sprite = arcade.Sprite(":resources:images/animated_characters/zombie/zombie_walk0.png", SPRITE_SCALING)
            else:
                sprite = arcade.Sprite(":resources:images/animated_characters/robot/robot_walk0.png", SPRITE_SCALING)

            x = 0
            y = 0

            match (direction):
                case 0:
                    # HAUT
                    y = 1
                    x = random.randint(1, GRID_WIDTH - 2)
                case 1:
                    # DROITE
                    y = random.randint(1, GRID_HEIGHT - 2)
                    x = GRID_WIDTH - 2
                case 2:
                    # BAS
                    y = GRID_HEIGHT - 2
                    x = random.randint(1, GRID_WIDTH - 2)
                case 3:
                    # GAUCHE
                    y = random.randint(1, GRID_HEIGHT - 2)
                    x = 1

            self.enemy_id_to_pos[cpt] = (x, y)
            sprite.center_x, sprite.center_y = state_to_xy((y, x))
            self.enemy_sprite_list.append(sprite)

            cpt += 1

    def update(self, agent):
        # check if enemy dead is removed
        for id in self.enemy_id_pos_removed.keys():
            if id in self.enemy_id_to_pos:
                self.enemy_id_to_pos.pop(id)

        # moving enemy
        for cpt in range(0, len(self.enemy_id_to_pos)):
            self.follow_agent(cpt, agent)

    def follow_agent(self, id, agent):
        # Utilisez une liste contenant votre sprite ennemi comme premier argument
        self.physics_engine_list[id].update()
        start = (self.enemy_sprite_list[id].center_x, self.enemy_sprite_list[id].center_y)
        end = (agent.agent_sprite.center_x, agent.agent_sprite.center_y)
        path = arcade.astar_calculate_path(start, end, self.barrier_list[id],
                                           diagonal_movement=True)

        if path and len(path) > 1:
            if self.enemy_sprite_list[id].center_y < path[1][1]:
                self.enemy_sprite_list[id].center_y += min(SPRITE_SPEED,
                                                           path[1][1] - self.enemy_sprite_list[id].center_y)
            elif self.enemy_sprite_list[id].center_y > path[1][1]:
                self.enemy_sprite_list[id].center_y -= min(SPRITE_SPEED,
                                                           self.enemy_sprite_list[id].center_y - path[1][1])

            if self.enemy_sprite_list[id].center_x < path[1][0]:
                self.enemy_sprite_list[id].center_x += min(SPRITE_SPEED,
                                                           path[1][0] - self.enemy_sprite_list[id].center_x)
            elif self.enemy_sprite_list[id].center_x > path[1][0]:
                self.enemy_sprite_list[id].center_x -= min(SPRITE_SPEED,
                                                           self.enemy_sprite_list[id].center_x - path[1][0])

            self.enemy_id_to_pos[id] = xy_to_state(self.enemy_sprite_list[id].center_x,
                                                   self.enemy_sprite_list[id].center_y)
