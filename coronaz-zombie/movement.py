from random import randint
import logging

def step_gen(zombie):
    while True:
        direction = randint(0, 3)
        for i in range(randint(2, 10)):
            if not valid_step(zombie, direction):
                break
            yield direction

def valid_step(zombie, direction):
    field = zombie.field_size
    pos = zombie.position

    if direction == 0:
        pos[0] += 1
    elif direction == 1:
        pos[1] += 1
    elif direction == 2:
        pos[0] -= 1
    elif direction == 3:
        pos[1] -= 1

    if pos[0] < 0 or field[0] < pos[0] or pos[1] < 0 or field[1] < pos[1]:
        logging.debug('Not valid step: %s' % direction)
        return False

    return True