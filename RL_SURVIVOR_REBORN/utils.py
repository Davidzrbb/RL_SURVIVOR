from constants import * 
def state_to_xy(state):
        return (state[1] + 0.5) * SPRITE_SIZE, \
               (GRID_HEIGHT - state[0] - 0.5) * SPRITE_SIZE