import argparse
import os
import time
from pprint import pprint

from rocketleaguereplayanalysis.data.data_loader import load_data
from rocketleaguereplayanalysis.render.do_render import do_render_minimap, \
    do_render_pressure, do_render_possession, \
    do_render_player_data_scoreboard, do_render_player_data_drive, \
    set_video_prefix
from rocketleaguereplayanalysis.render.ffmpeg_cmd import \
    create_ffmpeg_cmd_files
from rocketleaguereplayanalysis.util.data_explorer import data_explorer_cli
from rocketleaguereplayanalysis.util.export import export_parsed_data
from rocketleaguereplayanalysis.util.extra_info import get_field_dimensions

version = 'v1.4.0-dev'

frame_num_format = '{0:05d}'


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
                                 'video_all',
                                 'data_explorer'],
                        default=None)

    # Optional args
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

    print('Parsing data...')
    load_data(args.game_json)
    print('Data successfully parsed.')

    set_video_prefix(os.path.join('renders', out_prefix.split('.')[0]))

    if args.show_field_size:
        pprint(get_field_dimensions())
    if args.export_parsed_data:
        print('Exporting data...')
        export_parsed_data()
        print('Export successful.')

    if args.process_type == 'data_explorer':
        time.sleep(.5)
        data_explorer_cli()
        exit()

    print('Rendering video...')
    create_ffmpeg_cmd_files()
    print('Text files created.')

    print('Rendering is not ready yet. For that reason, this program '
          'will now terminate.')
    exit()

    if args.process_type == 'video_minimap':
        do_render_minimap()
    elif args.process_type == 'video_pressure':
        do_render_pressure()
    elif args.process_type == 'video_possession':
        do_render_possession()
    elif args.process_type == 'video_player_data_drive':
        do_render_player_data_drive()
    elif args.process_type == 'video_player_data_scoreboard':
        do_render_player_data_scoreboard()
    elif args.process_type == 'video_all':
        do_render_minimap()
        do_render_pressure()
        do_render_possession()
        do_render_player_data_drive()
        do_render_player_data_scoreboard()
    else:
        print('No process_type selected. Exiting. (See --help for more info '
              'if you expected a video renders or the ability to easily '
              'explore the data.)')


if __name__ == "__main__":
    main()
