import arcade
from constants import *
from game_environment.enemy import Enemy
from game_environment.map import Environment
from rl.agent import Agent


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(GRID_WIDTH * SPRITE_SIZE, GRID_HEIGHT * SPRITE_SIZE, SCREEN_TITLE)
        self.environment = Environment(self)
        self.agent = Agent(self, self.environment)
        self.enemy = Enemy(self.agent)

    def on_draw(self):
        arcade.start_render()
        self.environment.on_draw()
        self.agent.on_draw()
        self.enemy.on_draw()

    def on_update(self, delta_time):
        self.enemy.on_update(delta_time)
        self.agent.update(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        self.agent.agent_sprite.center_x = x
        self.agent.agent_sprite.center_y = y

    # if press R, reset the ennemy
    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.environment.setup()
            self.agent.setup()
            self.enemy.setup()


def main():
    window = MyWindow()
    window.center_window()
    arcade.run()


if __name__ == "__main__":
    main()
