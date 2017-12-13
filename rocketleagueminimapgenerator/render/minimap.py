def render_field(out_prefix):
    import os
    from pathlib import Path

    from tqdm import tqdm

    from rocketleagueminimapgenerator.parser.frames import get_frames
    from rocketleagueminimapgenerator.data.data_loader import get_data_start, \
        get_data_end
    from rocketleagueminimapgenerator.util.config import get_config

    frames = get_frames()

    ball_loc = {'x': [], 'y': []}

    for frame in frames:
        ball_loc['x'].append(frame['ball']['loc']['x'])
        ball_loc['y'].append(frame['ball']['loc']['y'])

    max_x = max(ball_loc['x'])
    min_x = min(ball_loc['x'])
    x_w = max_x - min_x

    # Make divisible by 2
    x_size = ((x_w - (x_w % (2 * get_config('size_modifier')))) /
              get_config('size_modifier'))

    max_y = max(ball_loc['y'])
    min_y = min(ball_loc['y'])
    y_w = max_y - min_y

    # Make divisible by 2
    y_size = ((y_w - (y_w % (2 * get_config('size_modifier')))) /
              get_config('size_modifier'))

    if not os.path.exists(os.path.join(out_prefix, 'minimap')):
        path = Path(os.path.join(out_prefix, 'minimap'))
        path.mkdir(parents=True)

    for i in tqdm(range(get_data_start(), get_data_end()),
                  desc='Minimap Render',
                  ascii=True):
        render_frame(ball_loc=ball_loc, frames=frames, frame_num=i,
                     min_x=min_x, min_y=min_y, out_prefix=out_prefix,
                     x_size=x_size, y_size=y_size)


def render_frame(ball_loc, frames, frame_num,
                 min_x, min_y, x_size, y_size, out_prefix):
    import math
    import os

    import cairosvg

    from rocketleagueminimapgenerator.main import frame_num_format, \
        car_template, field_template
    from rocketleagueminimapgenerator.data.object_numbers import \
        get_player_team_name
    from rocketleagueminimapgenerator.util.config import \
        get_config

    with open(os.path.join(out_prefix, 'minimap',
                           frame_num_format.format(frame_num) + '.png'),
              'wb') as file_out:
        car_placement = ''

        car_size = get_config('car_size')

        r = car_size / 2

        tri_pt_x_const = r / 2 * math.sqrt(3)
        tri_pt_y_const = r / math.sqrt(3)

        for car_id in frames[frame_num]['cars'].keys():
            x = frames[frame_num]['cars'][car_id]['loc']['x']
            y = frames[frame_num]['cars'][car_id]['loc']['y']

            if x is None and y is None:
                car_x = ((frames[frame_num]['cars'][car_id]['loc']['x']
                          - min_x) / get_config('size_modifier'))
                car_y = ((frames[frame_num]['cars'][car_id]['loc']['y']
                          - min_y) / get_config('size_modifier'))

                player_team = get_player_team_name(car_id)

                car_placement += car_template.format(
                        team_id=player_team,
                        car_pos_x=car_x,
                        car_pos_y=car_y,

                        car_triangle_pt1_x=car_x,
                        car_triangle_pt1_y=car_y - r,

                        car_triangle_pt2_x=car_x - tri_pt_x_const,
                        car_triangle_pt2_y=car_y + tri_pt_y_const,

                        car_triangle_pt3_x=car_x + tri_pt_x_const,
                        car_triangle_pt3_y=car_y + tri_pt_y_const,

                        car_angle=(
                            frames[frame_num]['cars'][car_id]['rot']['y'] +
                            270),

                        car_size=car_size,
                        arrow_move=car_size * 1.5
                )

        cairosvg.svg2png(bytestring=bytes(
                field_template.format(x_size=x_size,
                                      y_size=y_size,
                                      center_pos_x=x_size / 2,
                                      center_pos_y=y_size / 2,
                                      center_size=get_config('center_size'),
                                      ball_pos_x=(ball_loc['x'][frame_num] -
                                                  min_x) / get_config(
                                              'size_modifier'),
                                      ball_pos_y=(ball_loc['y'][frame_num] -
                                                  min_y) / get_config(
                                              'size_modifier'),
                                      ball_size=get_config('ball_size'),
                                      car_placement=car_placement
                                      ), 'UTF-8'), write_to=file_out)
