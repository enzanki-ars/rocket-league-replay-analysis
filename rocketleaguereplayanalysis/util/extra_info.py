def get_field_dimensions():
    from rocketleaguereplayanalysis.parser.frames import get_frames

    frames = get_frames()

    ball_loc = {'x': [], 'y': []}

    for frame in frames:
        ball_loc['x'].append(frame['ball']['loc']['x'])
        ball_loc['y'].append(frame['ball']['loc']['y'])

    center_x = ball_loc['x'][0]
    center_y = ball_loc['y'][0]

    max_x = max(ball_loc['x'])
    min_x = min(ball_loc['x'])
    x_w = max(max_x - center_x, center_x - min_x) * 2

    max_y = max(ball_loc['y'])
    min_y = min(ball_loc['y'])
    y_w = max(max_y - center_y, center_y - min_y) * 2

    return {
        'ball_loc': ball_loc,
        'center_x': center_x,
        'center_y': center_y,
        'min_x': min_x,
        'min_y': min_y,
        'max_x': max_x,
        'max_y': max_y,
        'x_size': x_w,
        'y_size': y_w,
    }


def fix_pressure_possession_values():
    from rocketleaguereplayanalysis.parser.frames import get_frames

    frames = get_frames()

    for i, frame in enumerate(frames):
        max_pressure = (frames[i]['pressure']['team0'] +
                        frames[i]['pressure']['team1'])

        max_possession = (frames[i]['possession']['team0'] +
                          frames[i]['possession']['team1'])

        if max_pressure > 0:
            frames[i]['pressure']['team0'] = (frames[i]['pressure']['team0'] /
                                              max_pressure)
            frames[i]['pressure']['team1'] = (frames[i]['pressure']['team1'] /
                                              max_pressure)
        else:
            frames[i]['pressure']['team0'] = .5
            frames[i]['pressure']['team1'] = .5

        if max_possession > 0:
            frames[i]['possession']['team0'] = (
                    frames[i]['possession']['team0'] /
                    max_possession)
            frames[i]['possession']['team1'] = (
                    frames[i]['possession']['team1'] /
                    max_possession)
        else:
            frames[i]['possession']['team0'] = .5
            frames[i]['possession']['team1'] = .5


def parse_pressure():
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.util.sync import \
        get_sync_delta_type

    field_dimensions = get_field_dimensions()
    frames = get_frames()

    frames[0]['pressure'] = {'team0': 0, 'team1': 0}

    for i, frame in enumerate(frames):
        if field_dimensions['ball_loc']['y'][i] > \
                field_dimensions['center_y']:

            frame['pressure'] = {
                'team0': (frames[i - 1]['pressure']['team0'] +
                          frame['time'][get_sync_delta_type()]),
                'team1': frames[i - 1]['pressure']['team1']
            }

        elif field_dimensions['ball_loc']['y'][i] < \
                field_dimensions['center_y']:
            frame['pressure'] = {
                'team0': frames[i - 1]['pressure']['team0'],
                'team1': (frames[i - 1]['pressure']['team1'] +
                          frame['time'][get_sync_delta_type()])
            }

        else:
            if i > 0:
                frame['pressure'] = {
                    'team0': frames[i - 1]['pressure']['team0'],
                    'team1': frames[i - 1]['pressure']['team1']
                }
            else:
                frame['pressure'] = {
                    'team0': 0,
                    'team1': 0
                }


def parse_possession():
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.util.sync import \
        get_sync_delta_type

    frames = get_frames()

    frames[0]['possession'] = {'team0': 0, 'team1': 0}

    for i, frame in enumerate(frames):
        if frame['ball']['last_hit'] == 0:
            frame['possession'] = {
                'team0': (frames[i - 1]['possession']['team0'] +
                          frame['time'][get_sync_delta_type()]),
                'team1': frames[i - 1]['possession']['team1']}

        elif frame['ball']['last_hit'] == 1:
            frame['possession'] = {
                'team0': frames[i - 1]['possession']['team0'],
                'team1': (frames[i - 1]['possession']['team1'] +
                          frame['time'][get_sync_delta_type()])
            }
        else:
            if i > 0:
                frame['possession'] = {
                    'team0': frames[i - 1]['possession']['team0'],
                    'team1': frames[i - 1]['possession']['team1']
                }
            else:
                frame['possession'] = {'team0': 0, 'team1': 0}


def parse_total_boost():
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_team_id, get_player_info

    frames = get_frames()
    team0_mod = 0
    team1_mod = 0

    for player_id in get_player_info():
        if get_player_team_id(player_id) == 'team0':
            team0_mod += 1
        elif get_player_team_id(player_id) == 'team1':
            team1_mod += 1

    for i, frame in enumerate(frames):
        frame['total_boost'] = {'team0': 0, 'team1': 0}
        for player_id in frame['cars']:
            if get_player_team_id(player_id):
                frame['total_boost'][get_player_team_id(player_id)] += \
                    frame['cars'][player_id]['boost']

        if team0_mod:
            frame['total_boost']['team0'] = frame['total_boost'][
                                                'team0'] / team0_mod
        if team1_mod:
            frame['total_boost']['team1'] = frame['total_boost'][
                                                'team1'] / team1_mod
