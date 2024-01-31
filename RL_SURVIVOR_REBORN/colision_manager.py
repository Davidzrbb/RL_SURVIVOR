from constants import *

class ColisionManager():

    def __init__(self):
        pass

    def setup(self):
        pass

    def update(self, bullet, enemy):
        for id in bullet.bullet_id_to_pos:
            state = bullet.bullet_id_to_pos[id]
            if state in enemy.enemy_id_to_pos.values():
                print("Hit")
                index = list(enemy.enemy_id_to_pos.values()).index(state)
                print(index)
                enemy.enemy_sprite_list[index].kill()
                enemy.enemy_id_to_pos.pop(index)
                #tué enemy
                #tué balle

                #               0   1
                #sprite_list = {s1, s2}

                #               0      1
                #id_to_pos = {(x,y), (x,y)}

                