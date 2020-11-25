from random import randint


def step_gen(zombie):
    while True:
        goal_position = [randint(0, zombie.field_size[0]), randint(0, zombie.field_size[1])]
        while True:
            pos = zombie.position
            delta = get_delta(pos, goal_position)

            if at_position(delta):
                break

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


def at_position(delta):
    for d in delta:
        if d != 0:
            return False
    return True

def get_delta(pos, goal_pos):
    return [goal_pos[0] - pos[0], goal_pos[1] - pos[1]]