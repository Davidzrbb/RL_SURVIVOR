import random

import arcade
from constants import *
from arcade.sprite import Sprite


class CoinSprite(Sprite):
    def __init__(self, filename, scale, agent, coin_sprite):
        super().__init__(filename, scale, hit_box_algorithm="Simple")
        self.agent = agent
        self.coin_sprite = coin_sprite
        self.check_hitbox_coin = None

    def collect_coin(self, coin_sprite, agent_sprite):
        self.check_hitbox_coin = arcade.check_for_collision_with_list(agent_sprite, coin_sprite)
        if self.check_hitbox_coin:
            # Iterate through the bullets and find the one that collided
            for coin in coin_sprite:
                if arcade.check_for_collision(agent_sprite, coin):
                    coin.kill()


class EnemySprite(Sprite):
    def __init__(self, filename, scale, agent, ennemies, enemy):
        super().__init__(filename, scale, hit_box_algorithm="Simple")
        self.check_hitbox = None
        self.check_hitbox_bullet = None
        self.path = None
        self.barrier_list = None
        self.env = agent.env
        grid_size = SPRITE_SIZE
        self.ennemies = ennemies
        self.agent = agent
        self.enemy = enemy

        playing_field_left_boundary = 0
        playing_field_right_boundary = GRID_WIDTH * SPRITE_SIZE  # ou une valeur appropriée
        playing_field_top_boundary = GRID_HEIGHT * SPRITE_SIZE  # ou une valeur appropriée
        playing_field_bottom_boundary = 0

        # Utilisez une liste contenant votre sprite ennemi comme premier argument
        self.barrier_list = arcade.AStarBarrierList(self, self.env.obstacle_list,
                                                    grid_size,
                                                    playing_field_left_boundary,
                                                    playing_field_right_boundary,
                                                    playing_field_bottom_boundary,
                                                    playing_field_top_boundary)
        self.physics_engine = arcade.PhysicsEngineSimple(self,
                                                         self.ennemies)

    def follow_agent(self, agent_sprite):
        self.check_hitbox = arcade.check_for_collision(self, agent_sprite)
        self.check_hitbox_bullet = arcade.check_for_collision_with_list(self, self.agent.bullet)

        if self.check_hitbox_bullet:
            # Iterate through the bullets and find the one that collided
            for bullet in self.agent.bullet:
                if arcade.check_for_collision(self, bullet):
                    enemy_sprite = self
                    enemy_sprite.enemy.add_coin(enemy_sprite)  # Use the 'enemy' attribute to access the Enemy instance
                    self.kill()  # Kill the enemy
                    bullet.kill()  # Kill the specific bullet that collided
                    break

        if self.check_hitbox:
            # SI ENNEMI TOUCHE AGENT
            if random.randint(0, 100) < 10:
                self.agent.indicator_bar.fullness -= 0.1
        self.physics_engine.update()
        start = (self.center_x, self.center_y)
        end = (agent_sprite.center_x, agent_sprite.center_y)
        self.path = arcade.astar_calculate_path(start, end, self.barrier_list,
                                                diagonal_movement=True)
        if self.path and len(self.path) > 1:
            if self.center_y < self.path[1][1]:
                self.center_y += min(SPRITE_SPEED, self.path[1][1] - self.center_y)
            elif self.center_y > self.path[1][1]:
                self.center_y -= min(SPRITE_SPEED, self.center_y - self.path[1][1])

            if self.center_x < self.path[1][0]:
                self.center_x += min(SPRITE_SPEED, self.path[1][0] - self.center_x)
            elif self.center_x > self.path[1][0]:
                self.center_x -= min(SPRITE_SPEED, self.center_x - self.path[1][0])


class Enemy:
    def __init__(self, window, agent):
        self.coin_sprite_list = arcade.SpriteList()
        self.enemy_sprite_list = arcade.SpriteList()
        self.agent = agent
        self.env = agent.env
        self.window = window
        self.total_time = 0.0
        self.killed_enemy_positions = []
        self.timer_text = arcade.Text(
            text="3",
            start_x=window.width // 2 + 10,
            start_y=window.height // 2 - 60,
            color=arcade.color.RED,
            font_size=40,
            anchor_x="center",
        )
        self.setup()

    def setup(self):
        # reset the enemy
        self.enemy_sprite_list = arcade.SpriteList()
        self.coin_sprite_list = arcade.SpriteList()
        self.total_time = 0.0
        count = 0
        while count < NB_ENEMIES:
            width_random, height_random = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
            if self.map(width_random, height_random) == MAP_ENEMY or self.map(width_random,
                                                                              height_random) == MAP_ENEMY2:
                if self.map(width_random, height_random) == MAP_ENEMY:
                    enemy_sprite = EnemySprite(":resources:images/animated_characters/zombie/zombie_walk0.png",
                                               SPRITE_SCALING * 1.3, self.agent, self.enemy_sprite_list, self
                                               )
                else:
                    enemy_sprite = EnemySprite(":resources:images/animated_characters/robot/robot_walk0.png",
                                               SPRITE_SCALING * 1.3, self.agent, self.enemy_sprite_list, self
                                               )
                enemy_sprite.center_x, enemy_sprite.center_y = self.state_to_xy((height_random, width_random))
                self.enemy_sprite_list.append(enemy_sprite)
                count += 1

    def game_over(self):
        if self.agent.indicator_bar.fullness <= 0:
            arcade.draw_lrtb_rectangle_filled(0, self.window.width, self.window.height, 0, (0, 0, 0, 200))
            arcade.draw_text("Game Over", self.window.width / 2 - 125, self.window.height / 2 + 20, arcade.color.RED,
                             40)
            self.timer_text.draw()

    def add_coin(self, enemy_sprite):
        coin_sprite = CoinSprite(":resources:images/items/coinGold.png", SPRITE_SCALING, self.agent,
                                 self.coin_sprite_list)
        coin_sprite.center_x, coin_sprite.center_y = enemy_sprite.center_x, enemy_sprite.center_y
        self.coin_sprite_list.append(coin_sprite)

        # Store the position of the killed enemy
        position = (enemy_sprite.center_y // SPRITE_SIZE, enemy_sprite.center_x // SPRITE_SIZE)
        self.killed_enemy_positions.append(position)

        # Remove the enemy sprite from the list
        self.enemy_sprite_list.remove(enemy_sprite)

    def on_draw(self):
        self.enemy_sprite_list.draw()
        self.coin_sprite_list.draw()
        self.game_over()

    def on_update(self, delta_time):
        if self.agent.indicator_bar.fullness <= 0:
            self.total_time += delta_time
            # Calculate seconds by using a modulus (remainder)
            seconds = 3 - int(self.total_time) % 60
            # Use string formatting to create a new text string for our timer
            self.timer_text.text = f"{seconds:2d}"
            if self.total_time > 3:
                self.window.reload()
        for enemy in self.enemy_sprite_list:
            enemy.follow_agent(self.agent.agent_sprite)
        for coin in self.coin_sprite_list:
            coin.collect_coin(self.coin_sprite_list, self.agent.agent_sprite)

    def state_to_xy(self, state):
        return (state[1] + 0.5) * SPRITE_SIZE, \
               (self.env.rows - state[0] - 0.5) * SPRITE_SIZE

    def map(self, width_random, height_random):
        state = (height_random, width_random)
        if self.env.map_object[state] == MAP_EMPTY:
            if random.randint(0, 100) < 50:
                self.env.map_object[state] = MAP_ENEMY
            else:
                self.env.map_object[state] = MAP_ENEMY2
        return self.env.map_object[state]
