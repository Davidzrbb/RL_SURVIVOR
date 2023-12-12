import arcade
from constants import *
from game_environment.map import Environment
from rl.agent import Agent


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(GRID_WIDTH * SPRITE_SIZE,
                         GRID_HEIGHT * SPRITE_SIZE, "Survivor Game")
        self.environment = Environment(self)
        self.agent = Agent(self, self.environment)

    def on_draw(self):
        arcade.start_render()
        self.environment.on_draw()
        self.agent.on_draw()


def main():
    window = MyWindow()
    window.center_window()
    arcade.run()


if __name__ == "__main__":
    main()
