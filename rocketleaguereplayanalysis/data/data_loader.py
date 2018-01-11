data = None

data_start = 0


def load_data(filename):
    import json

    from rocketleaguereplayanalysis.data.actor_data import parse_actor_data
    from rocketleaguereplayanalysis.data.object_numbers import \
        parse_player_info, parse_game_event_num
    from rocketleaguereplayanalysis.parser.frames import load_frames
    from rocketleaguereplayanalysis.util.extra_info import parse_pressure, \
        parse_possession, fix_pressure_possession_values

    global data

    with open(filename) as data_file:
        data = json.load(data_file)

    parse_actor_data()
    parse_player_info()
    parse_game_event_num()

    load_frames()

    parse_pressure()
    parse_possession()

    fix_pressure_possession_values()


def get_data():
    return data
