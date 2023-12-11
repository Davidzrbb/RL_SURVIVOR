"""
Loading screen
"""
import arcade
from views.draw_bar import draw_bar
from load_game_map import load_map


class LoadingView(arcade.View):
    def __init__(self):
        super().__init__()
        self.started = False
        self.progress = 0
        self.map_list = None
        arcade.set_background_color(arcade.color.ALMOND)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Loading...",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.ALLOY_ORANGE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )
        self.started = True
        draw_bar(
            current_amount=self.progress,
            max_amount=100,
            center_x=self.window.width / 2,
            center_y=20,
            width=self.window.width,
            height=10,
            color_a=arcade.color.BLACK,
            color_b=arcade.color.WHITE,
        )

    def setup(self):

        pass

    def on_update(self, delta_time: float):
        if not self.started:
            return
        if self.progress >= 100:
            self.window.show_view(self.map_list)
        else:
            self.progress += 1
            self.on_draw()
        pass
