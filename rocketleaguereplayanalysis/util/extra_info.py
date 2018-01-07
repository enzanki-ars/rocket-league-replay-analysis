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


def parse_pressure():
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.data.object_numbers import team0, \
        team1

    field_dimensions = get_field_dimensions()
    frames = get_frames()

    frames[0]['pressure'] = {team0: 0, team1: 0}

    for i, frame in enumerate(frames):
        if field_dimensions['ball_loc']['y'][i] > \
                field_dimensions['center_y']:
            frame['pressure'] = {
                team0: (frames[i - 1]['pressure'][team0] +
                        frame['time']['real_replay_delta']),
                team1: frames[i - 1]['pressure'][team1]
            }

        elif field_dimensions['ball_loc']['y'][i] < \
                field_dimensions['center_y']:
            frame['pressure'] = {
                team0: frames[i - 1]['pressure'][team0],
                team1: (frames[i - 1]['pressure'][team1] +
                        frame['time']['real_replay_delta'])
            }

        else:
            if i > 0:
                frame['pressure'] = {
                    team0: frames[i - 1]['pressure'][team0],
                    team1: frames[i - 1]['pressure'][team1]
                }
            else:
                frame['pressure'] = {
                    team0: 0,
                    team1: 0
                }


def parse_possession():
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.data.object_numbers import team0, \
        team1

    frames = get_frames()

    frames[0]['possession'] = {team0: 0, team1: 0}

    for i, frame in enumerate(frames):
        if frame['ball']['last_hit'] == team0:
            frame['possession'] = {
                team0: (frames[i - 1]['possession'][team0] +
                        frame['time']['real_replay_delta']),
                team1: frames[i - 1]['possession'][team1]}

        elif frame['ball']['last_hit'] == team1:
            frame['possession'] = {
                team0: frames[i - 1]['possession'][team0],
                team1: (frames[i - 1]['possession'][team1] +
                        frame['time']['real_replay_delta'])
            }
        else:
            if i > 0:
                frame['possession'] = {
                    team0: frames[i - 1]['possession'][team0],
                    team1: frames[i - 1]['possession'][team1]
                }
            else:
                frame['possession'] = {team0: 0, team1: 0}
