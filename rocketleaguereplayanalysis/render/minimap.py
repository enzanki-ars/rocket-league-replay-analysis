def render_field(out_prefix):
    import os
    from pathlib import Path

    from tqdm import tqdm

    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.data.data_loader import get_data_start, \
        get_data_end

    frames = get_frames()

    if not os.path.exists(os.path.join(out_prefix, 'minimap')):
        path = Path(os.path.join(out_prefix, 'minimap'))
        path.mkdir(parents=True)

    for i in tqdm(range(get_data_start(), get_data_end()),
                  desc='Minimap Render',
                  ascii=True):
        render_frame(frames=frames,
                     frame_num=i,
                     out_prefix=out_prefix)


def render_frame(frames, frame_num, out_prefix):
    import math
    import os

    import cairosvg

    from rocketleaguereplayanalysis.main import frame_num_format, \
        car_template, field_template
    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_team_name
    from rocketleaguereplayanalysis.util.config import \
        get_config
    from rocketleaguereplayanalysis.util.extra_info import get_field_dimensions

    field_dim = get_field_dimensions()

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

            if x is not None and y is not None:
                car_x = ((frames[frame_num]['cars'][car_id]['loc']['x']
                          - field_dim['min_x']) / get_config(
                        'size_modifier'))
                car_y = ((frames[frame_num]['cars'][car_id]['loc']['y']
                          - field_dim['min_y']) / get_config(
                        'size_modifier'))

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
                field_template.format(
                        x_size=field_dim['x_size'],
                        y_size=field_dim['y_size'],
                        center_pos_x=field_dim['x_size'] / 2,
                        center_pos_y=field_dim['y_size'] / 2,
                        center_size=get_config('center_size'),
                        ball_pos_x=(field_dim['ball_loc']['x'][frame_num] -
                                    field_dim['min_x']) /
                                   get_config('size_modifier'),
                        ball_pos_y=(field_dim['ball_loc']['y'][frame_num] -
                                    field_dim['min_y']) /
                                   get_config('size_modifier'),
                        ball_size=get_config('ball_size'),
                        car_placement=car_placement
                ), 'UTF-8'), write_to=file_out)
