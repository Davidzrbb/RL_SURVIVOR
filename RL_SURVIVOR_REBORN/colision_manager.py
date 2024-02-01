import copy

from constants import *


class CollisionManager:

    def __init__(self):
        pass

    def setup(self):
        pass

    def update(self, bullet, enemy):
        for bullet_id in copy.copy(bullet.bullet_id_to_pos):
            state = bullet.bullet_id_to_pos[bullet_id]

            # Find the key in enemy_id_to_pos with the matching value (state)
            enemy_key = next((key for key, value in enemy.enemy_id_to_pos.items() if value == state), None)

            if enemy_key is not None and enemy_key not in enemy.enemy_id_removed:
                # Get the index of the enemy sprite based on the key
                index = list(enemy.enemy_id_to_pos).index(enemy_key)
                # Add id enemy removed
                enemy.enemy_id_removed.append(enemy_key)
                # Perform actions on the enemy sprite based on the index
                enemy.enemy_sprite_list[index].kill()

                # Remove the bullet
                bullet.bullet_id_to_sprite[bullet_id].kill()
                bullet.bullet_last_pop.append(bullet_id)
                bullet.bullet_id_to_pos.pop(bullet_id)
