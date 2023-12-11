import arcade
from constants import SCREEN_HEIGHT


class Enemy:
    def __init__(self, window):
        self.window = window
        self.hello_text = "Hey, I'm an enemy!"

    def on_draw(self):
        arcade.draw_text(self.hello_text, 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 16)

# ... (le reste de votre code)
