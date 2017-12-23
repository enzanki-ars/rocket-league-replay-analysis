def get_field_dimensions():
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.util.config import get_config

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

    # Make divisible by 2
    x_size = ((x_w - (x_w % (2 * get_config('size_modifier')))) /
              get_config('size_modifier'))

    max_y = max(ball_loc['y'])
    min_y = min(ball_loc['y'])
    y_w = max(max_y - center_y, center_y - min_y) * 2

    # Make divisible by 2
    y_size = ((y_w - (y_w % (2 * get_config('size_modifier')))) /
              get_config('size_modifier'))

    return {
        'ball_loc': ball_loc,
        'center_x': center_x,
        'center_y': center_y,
        'min_x': min_x,
        'min_y': min_y,
        'max_x': max_x,
        'max_y': max_y,
        'x_size': x_size,
        'y_size': y_size,
    }


def get_pressure():
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.data.object_numbers import team_blue, \
        team_orange

    field_dimensions = get_field_dimensions()
    frames = get_frames()

    pressure = {team_blue: [], team_orange: []}

    for i, frame in enumerate(frames):
        if field_dimensions['ball_loc']['x'][i] < \
                field_dimensions['center_y']:
            pressure[team_blue].append(pressure[team_blue][i - 1] +
                                       frame['time']['real_replay_delta'])
            pressure[team_orange].append(pressure[team_orange][i - 1])

        elif field_dimensions['ball_loc']['x'][i] > \
                field_dimensions['center_y']:
            pressure[team_blue].append(pressure[team_blue][i - 1])
            pressure[team_orange].append(pressure[team_orange][i - 1] +
                                         frame['time']['real_replay_delta'])
        else:
            if i > 0:
                pressure[team_blue].append(pressure[team_blue][i - 1])
                pressure[team_orange].append(pressure[team_orange][i - 1])
            else:
                pressure[team_blue].append(0)
                pressure[team_orange].append(0)

    return pressure
