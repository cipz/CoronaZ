import logging
import time
from random import randint

from movement import step_gen


def interactive(zombie):
    logging.info('Interactive mode')
    directions = {'n': 0, 'e': 1, 's': 2, 'w': 3}
    while True:
        command = input('What to do: [c]ontact, [m]ove, [s]imulate, [q]uit\n')
        try:
            if command[0].startswith('m'):
                direction = input('direction: [n]orth, [e]ast, [s]outh, [w]est? ')
                zombie.move(directions[direction])
            elif command[0].startswith('c'):
                position = input('position [x,y]: ')
                zombie.process_message('{"uuid": "test", "position": %s, "infected": false}' % position)
            elif command[0].startswith('s'):
                for i in range(25):
                    zombie.move(randint(0, 3))
                    time.sleep(1)
            else:
                break
        except KeyboardInterrupt:
            logging.info('KeyboardInterrupt.. shutting down')
            return
        except Exception as e:
            print(e)


def automatic(zombie, args):
    logging.info('Automatic mode')
    step = step_gen(zombie)
    try:
        for i in range(args['zombie_lifetime']):
            if args['move_when_infected'] or not zombie.infected or zombie.protected:
                logging.debug('moving..')
                zombie.move(next(step))

            zombie.handle_infection()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt.. shutting down')
        return
