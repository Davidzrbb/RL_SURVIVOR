import arcade
from constants import *
from environment import Environment
from agent import Agent
from bullet import Bullet
from health_bar import HealthBar
from xp_bar import XpBar
from enemy import Enemy

class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(GRID_WIDTH * SPRITE_SIZE, GRID_HEIGHT * SPRITE_SIZE, SCREEN_TITLE)
        self.environment = Environment() #init et draw l'environment
        self.agent = Agent() #init et draw Agent
        self.bullet = Bullet() #init et draw bullet
        self.health_bar = HealthBar() #init et draw barre de vie
        self.xp_bar = XpBar() #init et draw barre d'xp
        self.enemy = Enemy(self.environment) #init et draw les ennemies

    def on_update(self, delta_time):
        self.environment.reset_map()

        self.agent.update()
        self.environment.update_map(self.agent.state, MAP_AGENT)
        
        self.bullet.update(delta_time, self, self.agent)
        for id in self.bullet.bullet_id_to_pos:
            self.environment.update_map(self.bullet.bullet_id_to_pos[id], MAP_BULLET)

        self.health_bar.update(self.agent)
        self.xp_bar.update(self.agent)

        self.enemy.update(self.agent)
        for id in self.enemy.enemy_id_to_pos:
            self.environment.update_map(self.enemy.enemy_id_to_pos[id], MAP_ENEMY)

    def on_draw(self):
        arcade.start_render()
        self.environment.on_draw()
        self.agent.on_draw()
        self.bullet.on_draw()
        self.health_bar.on_draw()
        self.xp_bar.on_draw()
        self.enemy.on_draw()    

    # def reload(self):


def main():
    window = MyWindow()
    window.center_window()
    arcade.run()


if __name__ == "__main__":
    main()

#TODO loose hp, gain xp
