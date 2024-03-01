import arcade
from constants import *


class GameOver:
    def __init__(self):
        self.total_time = 0.0
        self.timer = arcade.Text(
            text="3",
            start_x=GRID_WIDTH * SPRITE_SIZE // 2 + 10,
            start_y=GRID_HEIGHT * SPRITE_SIZE // 2 - 60,
            color=arcade.color.RED,
            font_size=40,
            anchor_x="center",
        )

    def setup(self):
        self.total_time = 0.0
        self.timer = arcade.Text(
            text="3",
            start_x=GRID_WIDTH * SPRITE_SIZE // 2 + 10,
            start_y=GRID_HEIGHT * SPRITE_SIZE // 2 - 60,
            color=arcade.color.RED,
            font_size=40,
            anchor_x="center",
        )

    def is_game_over(self, health_bar):
        return health_bar.health_value <= 0

    def on_draw(self):
        arcade.draw_lrtb_rectangle_filled(0, GRID_WIDTH * SPRITE_SIZE, GRID_HEIGHT * SPRITE_SIZE, 0, (0, 0, 0, 200))
        arcade.draw_text("Game Over", GRID_WIDTH * SPRITE_SIZE / 2 - 125, GRID_HEIGHT * SPRITE_SIZE / 2 + 20,
                         arcade.color.RED,
                         40)
        self.timer.draw()

    def wait_3_sec(self, delta_time):
        self.total_time += delta_time
        # Calculate seconds by using a modulus (remainder)
        seconds = 3 - int(self.total_time) % 60
        # Use string formatting to create a new text string for our timer
        self.timer.text = f"{seconds:2d}"
        return True
        if self.total_time > 3:
            return True
