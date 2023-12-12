import random
import arcade
from constants import *
from arcade.sprite import Sprite

nb_enemies = 10


class EnemySprite(Sprite):
    def __init__(self, filename, scale, agent, enemy_sprite_list):
        super().__init__(filename, scale, hit_box_algorithm="Simple")
        self.barrier_list = None
        self.hit_list = None
        self.env = agent.env
        self.enemy_sprite_list = enemy_sprite_list

    def follow_agent(self, agent_sprite):
        grid_size = SPRITE_SIZE

        # Calculate the playing field size. We can't generate paths outside of
        # this.
        playing_field_left_boundary = 0
        playing_field_right_boundary = 800  # ou une valeur appropriée
        playing_field_top_boundary = 600  # ou une valeur appropriée
        playing_field_bottom_boundary = 0

        # Utilisez une liste contenant votre sprite ennemi comme premier argument
        self.barrier_list = arcade.AStarBarrierList(self, self.env.obstacle_list,
                                                    grid_size,
                                                    playing_field_left_boundary,
                                                    playing_field_right_boundary,
                                                    playing_field_bottom_boundary,
                                                    playing_field_top_boundary)

        start = (self.center_x, self.center_y)  # Utilisez le centre du sprite comme point de départ
        end = (agent_sprite.center_x, agent_sprite.center_y)  # Utilisez le centre du sprite comme point final
        print(start, end)
        self.path = arcade.astar_calculate_path(start, end, self.barrier_list, diagonal_movement=False)

        # Déplacez le sprite le long du chemin
        if self.path:
            self.center_x, self.center_y = self.path[len(self.path) - 1]
            self.path.pop(0)


class Enemy:
    def __init__(self, agent):
        self.enemy_sprite_list = arcade.SpriteList()
        self.agent = agent
        self.env = agent.env
        self.setup()

    def setup(self):
        count = 0
        while count < nb_enemies:
            width_random, height_random = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
            if self.map(width_random, height_random) == MAP_ENEMY or self.map(width_random,
                                                                              height_random) == MAP_ENEMY2:
                if self.map(width_random, height_random) == MAP_ENEMY:
                    enemy_sprite = EnemySprite(":resources:images/animated_characters/zombie/zombie_walk0.png",
                                               SPRITE_SCALING * 1.3, self.agent, self.enemy_sprite_list)
                else:
                    enemy_sprite = EnemySprite(":resources:images/animated_characters/robot/robot_walk0.png",
                                               SPRITE_SCALING * 1.3, self.agent, self.enemy_sprite_list)
                enemy_sprite.center_x, enemy_sprite.center_y = self.state_to_xy((height_random, width_random))
                self.enemy_sprite_list.append(enemy_sprite)
                count += 1

    def on_draw(self):
        self.enemy_sprite_list.draw()

    def on_update(self, delta_time):
        for enemy in self.enemy_sprite_list:
            enemy.follow_agent(self.agent.agent_sprite)

    def state_to_xy(self, state):
        return (state[1] + 0.5) * SPRITE_SIZE, (self.env.rows - state[0] - 0.5) * SPRITE_SIZE

    def map(self, width_random, height_random):
        state = (height_random, width_random)
        if self.env.map_object[state] == MAP_EMPTY:
            if random.randint(0, 100) < 50:
                self.env.map_object[state] = MAP_ENEMY
            else:
                self.env.map_object[state] = MAP_ENEMY2
        return self.env.map_object[state]
