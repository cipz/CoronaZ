import argparse
import json


def get_cli_arguments():
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument('-f', '--field', type=int, nargs=2, metavar=('X', 'Y'), default=[100, 100],
                        help='field size in form: x y')
    parser.add_argument('-p', '--position', type=int, nargs=2, metavar=('X', 'Y'), default=[-1, -1],
                        help='Starting position of the client. If one or both values are set to -1, the client will be placed randomly on these axis on the field. Default is "-1 -1". Input form: x y')
    parser.add_argument('-i', '--infected', action='store_true',
                        help='if set the client is infected at startup')
    parser.add_argument('-r', '--infection-radius', type=int, metavar='X', default=10,
                        help='radius in which a contact is recognized')
    parser.add_argument('-s', '--server', type=str, nargs=2, metavar=('IP', 'QUEUE'),
                        help='IP address and QUEUE of the main server')
    parser.add_argument('-z', '--zombie-port', type=int, metavar='PORT', default=4711,
                        help='Port on which the broadcast messages are send')
    parser.add_argument('--interactive', action='store_true',
                        help='if set the client will be in interactive mode and waits for inputs to move')
    parser.add_argument('--zombie-lifetime', type=int, metavar='X', default=120,
                        help='Number of steps to be performed in automatic mode. Default = 120')
    parser.add_argument('--infection-cooldown', type=int, metavar='X', default=15,
                        help='Time it takes to heal and become not infected anymore')
    parser.add_argument('--no-kafka', action='store_true')
    parser.add_argument('--config-file', type=str, metavar='JSON_FILE',
                        help='Json file with configuration arguments')

    args = vars(parser.parse_args())

    if args['config_file'] is not None:
        args = parse_config_file(args)

    return args


def parse_config_file(args):
    with open(args['config_file'], 'r') as file:
        data = json.load(file)
        for k, v in data.items():
            if k == 'field_width':
                args['field'][0] = v
            elif k == 'field_height':
                args['field'][1] = v
            else:
                args[k] = v
    return args
