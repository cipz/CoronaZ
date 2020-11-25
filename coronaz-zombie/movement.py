from random import randint


def step_gen(zombie):
    while True:
        goal_position = [randint(0, zombie.field_size[0]), randint(0, zombie.field_size[1])]
        while True:
            if at_position(zombie, goal_position):
                break
            pos = zombie.position
            delta = [goal_position[0] - pos[0], goal_position[1] - pos[1]]
            if abs(delta[0]) > abs(delta[1]):
                if delta[0] < 0:
                    direction = 3  # west
                else:
                    direction = 1  # east
            else:
                if delta[1] < 0:
                    direction = 2  # south
                else:
                    direction = 0  # north
            yield direction


def at_position(zombie, goal_position):
    pos = zombie.position
    for d in [goal_position[0] - pos[0], goal_position[1] - pos[1]]:
        if d != 0:
            return False
    return True
