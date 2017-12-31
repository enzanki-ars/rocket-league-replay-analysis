import argparse
import os
import time
from pprint import pprint

from rocketleaguereplayanalysis.data.data_loader import load_data, \
    set_data_start, set_data_end
from rocketleaguereplayanalysis.util.data_explorer import data_explorer_cli
from rocketleaguereplayanalysis.util.do_render import do_render_minimap, \
    do_render_pressure, do_render_possession, \
    do_render_player_data_scoreboard_with_drive, \
    do_render_player_data_scoreboard, do_render_player_data_drive
from rocketleaguereplayanalysis.util.export import export_parsed_data
from rocketleaguereplayanalysis.util.extra_info import get_field_dimensions

version = 'v1.3.1-dev'

with open(os.path.join('assets', 'field-template.svg'), 'r') as svg_file:
    field_template = svg_file.read()

with open(os.path.join('assets', 'bar-comparison-template.svg'),
          'r') as svg_file:
    bar_comparison_template = svg_file.read()

with open(os.path.join('assets', 'player-data-drive-overlay-template.svg'),
          'r') as svg_file:
    player_data_drive_template = svg_file.read()

with open(
        os.path.join('assets', 'player-data-scoreboard-overlay-template.svg'),
        'r') as svg_file:
    player_data_scoreboard_template = svg_file.read()

with open(os.path.join('assets',
                       'player-data-scoreboard-with-drive'
                       '-overlay-template.svg'),
          'r') as svg_file:
    player_data_scoreboard_with_drive_template = svg_file.read()

car_template = '<circle class="team-{team_id} stroke-black" ' \
               'cx="{car_pos_x}" cy="{car_pos_y}" r="{car_size}"/>' \
               '<polygon class="team-{team_id} stroke-black" ' \
               'points="' \
               '{car_triangle_pt1_x},{car_triangle_pt1_y} ' \
               '{car_triangle_pt2_x},{car_triangle_pt2_y} ' \
               '{car_triangle_pt3_x},{car_triangle_pt3_y} " ' \
               'transform="rotate({car_angle} {car_pos_x} {car_pos_y})' \
               'translate(0 -{arrow_move})"/>'
frame_num_format = '{0:04d}'


def main():
    parser = argparse.ArgumentParser(prog='rocketleaguereplayanalysis')

    # Required args
    parser.add_argument('game_json', help='The name of the game json.')

    parser.add_argument('--process_type',
                        choices=['video_minimap',
                                 'video_pressure',
                                 'video_possession',
                                 'video_player_data_drive',
                                 'video_player_data_scoreboard',
                                 'video_player_data_scoreboard_with_drive',
                                 'video_all',
                                 'data_explorer'],
                        default=None)

    # Optional args
    parser.add_argument('--data_start',
                        help='Number of frames to render (start).',
                        type=int)
    parser.add_argument('--data_end',
                        help='Number of frames to render (end).',
                        type=int)
    parser.add_argument('--export_parsed_data',
                        help='Export the parsed data.',
                        action='store_const',
                        const=True,
                        default=False)
    parser.add_argument('--show_field_size',
                        help='Show the calculated field size.',
                        action='store_const',
                        const=True,
                        default=False)
    parser.add_argument('--version',
                        action='version',
                        help='Print version and exit (' + version + ')',
                        version='%(prog)s ' + version)

    args = parser.parse_args()

    out_prefix = os.path.basename(args.game_json)

    load_data(args.game_json)

    video_prefix = os.path.join('renders', out_prefix.split('.')[0])
    if args.data_start:
        set_data_start(args.data_start)
    if args.data_end:
        set_data_end(args.data_end)
    if args.show_field_size:
        pprint(get_field_dimensions())
    if args.export_parsed_data:
        print('Exporting data.')
        export_parsed_data(video_prefix)
        print('Export successful.')

    if args.process_type == 'video_minimap':
        do_render_minimap(video_prefix)
    elif args.process_type == 'video_pressure':
        do_render_pressure(video_prefix)
    elif args.process_type == 'video_possession':
        do_render_possession(video_prefix)
    elif args.process_type == 'video_player_data_drive':
        do_render_player_data_drive(video_prefix)
    elif args.process_type == 'video_player_data_scoreboard':
        do_render_player_data_scoreboard(video_prefix)
    elif args.process_type == 'video_player_data_scoreboard_with_drive':
        do_render_player_data_scoreboard_with_drive(video_prefix)
    elif args.process_type == 'video_all':
        do_render_minimap(video_prefix)
        do_render_pressure(video_prefix)
        do_render_possession(video_prefix)
        do_render_player_data_drive(video_prefix)
        do_render_player_data_scoreboard(video_prefix)
        do_render_player_data_scoreboard_with_drive(video_prefix)
    elif args.process_type == 'data_explorer':
        time.sleep(.5)
        data_explorer_cli()
    else:
        print('No process_type selected. Exiting. (See help for more info if '
              'you expected a video render or the ability to easily explore '
              'the data.)')


if __name__ == "__main__":
    main()
