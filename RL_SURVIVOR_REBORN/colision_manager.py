import copy

import arcade

from constants import *


class CollisionManager:

    def __init__(self):
        pass

    def setup(self):
        pass

    def update(self, bullet, enemy):
        #on check si le bullet touche un ennemi avec la hitbox
        #si oui on kill le bullet et l'ennemi et on ajoute l'id de l'ennemi dans la liste des ennemis tués
        #on ne verifie plus par rapport à leur position pour kill ou non car pas assez précis
        for bullet_id in copy.copy(bullet.bullet_id_to_pos):
            check_hitbox_bullet = arcade.check_for_collision_with_list(bullet.bullet_id_to_sprite[bullet_id],
                                                                       enemy.enemy_sprite_list)
            if check_hitbox_bullet:
                enemy_sprite_index = enemy.enemy_sprite_list.index(check_hitbox_bullet[0])
                id_enemy = list(enemy.enemy_id_to_pos.keys())[enemy_sprite_index]
                if id_enemy not in enemy.enemy_id_removed:
                    enemy.enemy_id_removed.append(id_enemy)
                    enemy.enemy_sprite_list[enemy_sprite_index].kill()

                bullet.bullet_id_to_sprite[bullet_id].kill()
                bullet.bullet_last_pop.append(bullet_id)
                bullet.bullet_id_to_pos.pop(bullet_id)
