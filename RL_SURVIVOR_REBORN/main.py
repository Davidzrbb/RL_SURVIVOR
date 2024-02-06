import arcade
from matplotlib import pyplot as plt

from rl_agent import ReinforcementLearning
from coin import Coin
from constants import *
from environment import Environment
from agent import Agent
from bullet import Bullet
from health_bar import HealthBar
from xp_bar import XpBar
from enemy import Enemy
from game_over import GameOver
from colision_manager import CollisionManager


class MyWindow(arcade.Window):

    def __init__(self):
        super().__init__(GRID_WIDTH * SPRITE_SIZE, GRID_HEIGHT * SPRITE_SIZE, SCREEN_TITLE)
        self.environment = Environment()  # init et draw l'environment
        self.agent = Agent()  # init et draw Agent
        self.bullet = Bullet()  # init et draw bullet
        self.health_bar = HealthBar()  # init et draw barre de vie
        self.xp_bar = XpBar()  # init et draw barre d'xp
        self.enemy = Enemy(self.environment)  # init et draw les ennemies
        self.coin = Coin()  # init et draw les coins
        self.collision_manager = CollisionManager()
        self.reinforcement_learning = ReinforcementLearning()
        self.game_over = GameOver()

    def on_update(self, delta_time):

        

        # remettre a zero la map
        self.environment.reset_map()

        # mettre a jour la position de la bullet
        self.bullet.update(delta_time, self, self.agent)
        for id in self.bullet.bullet_id_to_pos:
            self.environment.update_map(self.bullet.bullet_id_to_pos[id], MAP_BULLET)

        # mettre a jour la position de l'ennemie dans la map
        self.enemy.update(self.agent)
        for id in self.enemy.enemy_id_to_pos:
            self.environment.update_map(self.enemy.enemy_id_to_pos[id], MAP_ENEMY)

        # verifier les colisions
        self.collision_manager.collision_between_bullet_and_enemy(self.bullet, self.enemy, self.coin)

        # Pour chaque ennemi tué, je recupère son id et
        # je lui donne son id à l'id de la piece que je veux creer
        # et s'il y a nouveau ennemie tué donc il n'y a pas de coin a cette id
        # dans enemy_id_pos_removed j'ai id et sa pos quand il est mort
        # for id in self.enemy.enemy_id_pos_removed.keys():
        #     if id not in self.coin.coin_id_to_pos.keys():
        #         self.coin.add_coin(id, self.enemy.enemy_id_pos_removed[id])
        # mettre a jour la position de la coin dans la map
        for id in self.coin.coin_id_to_pos:
            self.environment.update_map(self.coin.coin_id_to_pos[id], MAP_XP)

        # verifier les colisions entre l'agent et les ennemies
        self.collision_manager.collision_between_agent_and_ennemies(self.agent, self.enemy, self.health_bar)

        # verifier si l'agent est mort
        if self.game_over.is_game_over(self.health_bar):
            if self.game_over.wait_3_sec(delta_time):
                self.reload()
        else:
            # calculer la meilleur action pour l'agent
            self.reinforcement_learning.do(self.environment.map,self.coin.coin_id_to_pos)
            
            # mettre a jour la position de l'agent
            self.reinforcement_learning.update_player(self.agent)

            # mettre a jour la map avec la position de l'agent
            self.environment.update_map(self.agent.state, MAP_AGENT)

        # verifier les colisions entre l'agent et les coins
        self.collision_manager.collision_between_agent_and_coin(self.agent, self.coin, self.xp_bar)

        # mettre a jour la position de barre de vie et d'xp
        self.health_bar.update(self.agent)
        self.xp_bar.update(self.agent)

        if(len(self.enemy.enemy_id_pos_removed) == get_nb_enemies() and get_nb_enemies() != 10):
            set_nb_enemies(get_nb_enemies() + 2)
            self.enemy = Enemy(self.environment)
        elif(len(self.enemy.enemy_id_pos_removed) == get_nb_enemies() and get_nb_enemies() == 10):
            self.reload()



        
    # def on_mouse_motion(self, x, y, dx, dy):
    #     self.agent.agent_sprite.center_x = x
    #     self.agent.agent_sprite.center_y = y

    def on_draw(self):
        arcade.start_render()
        self.environment.on_draw()
        self.agent.on_draw()
        self.bullet.on_draw()
        self.health_bar.on_draw()
        self.xp_bar.on_draw()
        self.enemy.on_draw()
        self.coin.on_draw()
        # verifier si l'agent est mort
        if self.game_over.is_game_over(self.health_bar):
            self.game_over.on_draw()
        # def reload(self):

    def reload(self):
        self.reinforcement_learning.save_history()
        self.environment.setup()
        self.agent.setup()
        self.bullet.setup()
        self.health_bar.setup()
        self.xp_bar.setup()
        set_nb_enemies(2)
        self.enemy.setup()
        self.coin.setup()
        self.reinforcement_learning.reset()
        self.game_over.setup()


def main():
    
    window = MyWindow()
    window.reinforcement_learning.load(AGENT_FILE)
    window.center_window()
    arcade.run()
    window.reinforcement_learning.save(AGENT_FILE)
    plt.plot(window.reinforcement_learning.history)
    plt.show()


if __name__ == "__main__":
    main()

