from constants import *
import random
import arcade
import copy
from utils import state_to_xy


class Environment:
    def __init__(self):
        self.map = {}  # y, x
        self.original_map = {}

        self.cols = None
        self.rows = None

        self.wall_list = None
        self.empty_list = None
        self.wall_T_list = None
        self.obstacle_list = None
        self.forgive_list_enemies = None

        self.setup()

    def setup(self):

        self.rows, self.cols = GRID_HEIGHT, GRID_WIDTH

        self.wall_T_list = arcade.SpriteList(use_spatial_hash=True)
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.obstacle_list = arcade.SpriteList(use_spatial_hash=True)
        self.forgive_list_enemies = arcade.SpriteList(use_spatial_hash=True)
        self.empty_list = arcade.SpriteList(use_spatial_hash=True)

        self.gen_map()
        self.states = self.map.keys()
        self.set_sprite()

    def on_draw(self):
        """Render the screen."""
        # Clear the screen to the background color
        arcade.start_render()
        # Draw our sprites
        self.obstacle_list.draw()
        self.forgive_list_enemies.draw()
        self.wall_list.draw()
        self.wall_T_list.draw()
        self.empty_list.draw()

    def gen_map(self):
        # génére WALL
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if (col == 0 or row == GRID_HEIGHT - 1 or col == GRID_WIDTH - 1) and not row == 0:
                    self.map[row, col] = MAP_WALL
                elif row == 0:
                    self.map[row, col] = MAP_WALL_T
                else:
                    self.map[row, col] = MAP_EMPTY

        # génére obstacles
        for row in range(1, GRID_HEIGHT - 2):
            for col in range(1, GRID_WIDTH - 3):
                if self.map[row, col] == MAP_EMPTY:
                    if (
                            self.map[row - 1, col] == self.map[row, col - 1] ==
                            self.map[row + 1, col] == self.map[row, col + 1] ==
                            self.map[row - 1, col - 1] == self.map[row + 1, col + 1] == MAP_EMPTY
                    ):
                        if random.randint(0, 100) < 3:
                            self.map[row, col] = MAP_OBSTACLE
                            if random.randint(0, 100) < 3:
                                self.map[row, col + 1] = MAP_OBSTACLE
                            if random.randint(0, 100) < 3:
                                self.map[row + 1, col] = MAP_OBSTACLE
                        if random.randint(0, 100) < 3:
                            self.map[row, col] = MAP_OBSTACLE2
                        if random.randint(0, 100) < 3:
                            self.map[row, col] = MAP_OBSTACLE3

        self.original_map = copy.deepcopy(self.map)

    def set_sprite(self):
        for state in self.states:
            if self.map[state] == MAP_WALL:
                wall_sprite = arcade.Sprite(":resources:images/topdown_tanks/tileGrass_transitionN.png",
                                            SPRITE_SCALING * 2, angle=90, hit_box_algorithm="Detailed")
                if state[0] == GRID_HEIGHT - 1:
                    wall_sprite = arcade.Sprite(":resources:images/topdown_tanks/tileGrass_transitionN.png",
                                                SPRITE_SCALING * 2, angle=180, hit_box_algorithm="Detailed")
                    wall_sprite.center_x, wall_sprite.center_y = state_to_xy(state)
                    self.wall_list.append(wall_sprite)
                    if state[1] == 0 or state[1] == GRID_WIDTH - 1:
                        wall_sprite = arcade.Sprite(":resources:images/topdown_tanks/tileGrass_transitionW.png",
                                                    SPRITE_SCALING * 2, angle=90, hit_box_algorithm="Detailed")
                        buisson1 = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                                 SPRITE_SCALING)
                        wall_sprite.center_x, wall_sprite.center_y = state_to_xy(state)
                        buisson1.center_x, buisson1.center_y = state_to_xy(state)
                        self.wall_list.append(wall_sprite)
                        self.wall_list.append(buisson1)
                elif state[1] == GRID_WIDTH - 1:
                    wall_sprite = arcade.Sprite(":resources:images/topdown_tanks/tileGrass_transitionW.png",
                                                SPRITE_SCALING * 2, angle=-180, hit_box_algorithm="Detailed")
                    wall_sprite.center_x, wall_sprite.center_y = state_to_xy(state)
                    self.wall_list.append(wall_sprite)
                if not state[0] == GRID_HEIGHT - 1 and not state[1] == GRID_WIDTH - 1:
                    wall_sprite.center_x, wall_sprite.center_y = state_to_xy(state)
                    self.wall_list.append(wall_sprite)

            elif self.map[state] == MAP_WALL_T:
                wall_sprite_T = arcade.Sprite(":resources:images/topdown_tanks/tileGrass_transitionN.png",
                                              SPRITE_SCALING * 2, hit_box_algorithm="Detailed")
                buisson = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                        SPRITE_SCALING, hit_box_algorithm="Detailed")
                if state[1] == 0 or state[1] == GRID_WIDTH - 1:
                    buisson.center_x, buisson.center_y = state_to_xy(state)
                    wall_sprite_T.center_x, wall_sprite_T.center_y = state_to_xy(state)
                    self.wall_T_list.append(wall_sprite_T)
                    self.wall_T_list.append(buisson)
                else:
                    wall_sprite_T.center_x, wall_sprite_T.center_y = state_to_xy(state)
                    self.wall_T_list.append(wall_sprite_T)

            elif self.map[state] == MAP_EMPTY:
                obstacle_sprite = arcade.Sprite(":resources:images/topdown_tanks/tileGrass1.png", SPRITE_SCALING * 2,
                                                hit_box_algorithm="Detailed")
                obstacle_sprite.center_x, obstacle_sprite.center_y = state_to_xy(state)
                self.empty_list.append(obstacle_sprite)

            elif self.map[state] == MAP_OBSTACLE or self.map[state] == MAP_OBSTACLE2 or self.map[
                state] == MAP_OBSTACLE3:
                if self.map[state] == MAP_OBSTACLE:
                    obstacle_sprite = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING,
                                                    hit_box_algorithm="Detailed")
                elif self.map[state] == MAP_OBSTACLE2:
                    obstacle_sprite = arcade.Sprite(":resources:images/tiles/rock.png",
                                                    SPRITE_SCALING, hit_box_algorithm="Detailed")
                else:
                    obstacle_sprite = arcade.Sprite(":resources:images/tiles/cactus.png",
                                                    SPRITE_SCALING, hit_box_algorithm="Detailed")

                background_sprite = arcade.Sprite(":resources:images/topdown_tanks/tileGrass1.png",
                                                  SPRITE_SCALING * 2, hit_box_algorithm="Detailed")
                background_sprite.center_x, background_sprite.center_y = state_to_xy(state)
                obstacle_sprite.center_x, obstacle_sprite.center_y = state_to_xy(state)
                self.obstacle_list.append(background_sprite)
                self.obstacle_list.append(obstacle_sprite)

                for sprite in self.wall_list:
                    self.forgive_list_enemies.append(copy.copy(sprite))

                for sprite in self.wall_T_list:
                    self.forgive_list_enemies.append(copy.copy(sprite))

    def update_map(self, state, value):
        self.map[state] = value

    def reset_map(self):
        self.map = copy.deepcopy(self.original_map)
