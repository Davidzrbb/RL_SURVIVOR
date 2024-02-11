import copy

import arcade

from utils import xy_to_state
from constants import *


class CollisionManager:

    def __init__(self):
        pass

    def setup(self):
        pass

    def collision_between_bullet_and_enemy(self, bullet, enemy, coin, env):
        # on check si le bullet touche un ennemi avec la hitbox
        # si oui on kill le bullet et l'ennemi et on ajoute l'id et la pos de l'ennemi dans la liste des ennemis tués
        # on ne verifie plus par rapport à leur position dans la map pour kill ou non car pas assez précis
        for bullet_id in copy.copy(bullet.bullet_id_to_pos):
            check_hitbox_bullet = arcade.check_for_collision_with_list(bullet.bullet_id_to_sprite[bullet_id],
                                                                       enemy.enemy_sprite_list)
            if check_hitbox_bullet:
                enemy_sprite_index = enemy.enemy_sprite_list.index(check_hitbox_bullet[0])
                id_enemy = list(enemy.enemy_id_to_pos.keys())[enemy_sprite_index]
                if id_enemy not in enemy.enemy_id_pos_removed.keys():
                    enemy.enemy_id_pos_removed[id_enemy] = xy_to_state(
                        enemy.enemy_sprite_list[enemy_sprite_index].center_x,
                        enemy.enemy_sprite_list[enemy_sprite_index].center_y)
                    enemy.enemy_sprite_list[enemy_sprite_index].kill()
                    pos_new_coin = enemy.enemy_id_pos_removed[id_enemy]
                    while env.map[pos_new_coin] != MAP_EMPTY and (
                            pos_new_coin[0] < 2 or pos_new_coin[1] < 2 or pos_new_coin[0] > GRID_HEIGHT - 3 or
                            pos_new_coin[1] > GRID_WIDTH - 3):
                        print("test")
                        # modifie la position de la coin avec une position voisine
                        if pos_new_coin[0] < 2:
                            pos_new_coin = (pos_new_coin[0] + 1, pos_new_coin[1])
                        if pos_new_coin[1] < 2:
                            pos_new_coin = (pos_new_coin[0], pos_new_coin[1] + 1)
                        if pos_new_coin[0] > GRID_HEIGHT - 3:
                            pos_new_coin = (pos_new_coin[0] - 1, pos_new_coin[1])
                        if pos_new_coin[1] > GRID_WIDTH - 3:
                            pos_new_coin = (pos_new_coin[0], pos_new_coin[1] - 1)
                    coin.add_coin(pos_new_coin)
                bullet.bullet_id_to_sprite[bullet_id].kill()
                bullet.bullet_last_pop.append(bullet_id)
                bullet.bullet_id_to_pos.pop(bullet_id)

    def collision_between_agent_and_coin(self, agent, coin, xp_bar):
        # on check si l'agent touche une coin avec la hitbox
        check_hitbox_coin = arcade.check_for_collision_with_list(agent.agent_sprite, coin.coin_sprite_list)
        if check_hitbox_coin:
            if check_hitbox_coin[0] in coin.coin_id_to_sprite.values():
                coin_index = list(coin.coin_id_to_sprite.values()).index(check_hitbox_coin[0])
                coin_id = list(coin.coin_id_to_sprite.keys())[coin_index]
                coin.coin_id_to_pos.pop(coin_id)
            xp_bar.add_xp()
            check_hitbox_coin[0].kill()

    def collision_between_agent_and_ennemies(self, agent, enemy, health_bar):
        # on check si l'agent touche une coin avec la hitbox
        check_hitbox_enemy = arcade.check_for_collision_with_list(agent.agent_sprite, enemy.enemy_sprite_list)
        if check_hitbox_enemy:
            health_bar.loose_hp()
