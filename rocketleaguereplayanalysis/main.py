import argparse
import os
import sys
from pprint import pprint

import rocketleaguereplayanalysis.assets
from rocketleaguereplayanalysis.util.asset_loc import get_assets_path, \
    set_assets_path
from rocketleaguereplayanalysis.data.data_loader import load_data
from rocketleaguereplayanalysis.render.do_render import set_video_prefix, \
    render
from rocketleaguereplayanalysis.util.data_explorer import data_explorer_cli
from rocketleaguereplayanalysis.util.export import export_parsed_data_json, \
    export_parsed_data_csv
from rocketleaguereplayanalysis.util.extra_info import get_field_dimensions
from rocketleaguereplayanalysis.util.sync import set_sync_delta_type, \
    set_sync_time_type

version = 'v1.4.0-alpha1'

frame_num_format = '{0:05d}'


def main():
    parser = argparse.ArgumentParser(prog='rocketleaguereplayanalysis')

    # Required args
    parser.add_argument('game_json', help='The name of the game json.')

    available_assets_builtin = []

    if getattr(sys, 'frozen', False):
        set_assets_path(os.path.join(sys._MEIPASS, 'assets'))
    else:
        set_assets_path(os.path.join(rocketleaguereplayanalysis.assets.__path__[0]))

    for file in os.listdir(get_assets_path()):
        if file.endswith('.json'):
            available_assets_builtin.append(file[:-1 * len('.json')])

    parser.add_argument('--render',
                        choices=available_assets_builtin,
                        nargs='+',
                        help='Select which renders are created. '
                             'Multiple renders can be separated by a space.',
                        default=None)

    parser.add_argument('--data_explorer',
                        help='Explore the given data.',
                        action='store_true')
    parser.add_argument('--export_parsed_data_json',
                        help='Export the parsed data as JSON.',
                        action='store_true')
    parser.add_argument('--export_parsed_data_csv',
                        help='Export the parsed data as CSV.',
                        action='store_true')
    parser.add_argument('--show_field_size',
                        help='Show the calculated field size.',
                        action='store_true')
    parser.add_argument('--sync_to_live_recording',
                        help='Instead of syncing to a recording of the '
                             'in-game replay, sync to a recording of the '
                             'game played live.  In other words, if you have '
                             'recorded the game as you were playing it, set '
                             'this argument to sync to that recording. If '
                             'you recorded the replay after the game ended, '
                             'do not add this argument to sync to that '
                             'recording.',
                        action='store_true')
    parser.add_argument('--version',
                        action='version',
                        help='Print version and exit (' + version + ')',
                        version='%(prog)s ' + version)

    args = parser.parse_args()

    out_prefix = os.path.basename(args.game_json)

    if args.sync_to_live_recording:
        set_sync_delta_type('server_delta')
        set_sync_time_type('server_time')
    else:
        set_sync_delta_type('real_replay_delta')
        set_sync_time_type('real_replay_time')

    print('Parsing data...')
    load_data(args.game_json)
    print('Data successfully parsed.')

    set_video_prefix(os.path.join('renders', out_prefix.split('.')[0]))

    if not args.render \
            and not args.data_explorer \
            and not args.show_field_size \
            and not args.export_parsed_data_json \
            and not args.export_parsed_data_csv:
        print('No action selected. Exiting. (See --help for more info '
              'if you expected a video renders or the ability to easily '
              'explore the data.)')
    else:
        if args.show_field_size:
            pprint(get_field_dimensions())
        if args.export_parsed_data_json:
            print('Exporting data...')
            export_parsed_data_json()
            print('Export successful.')
        if args.export_parsed_data_csv:
            print('Exporting data...')
            export_parsed_data_csv()
            print('Export successful.')
        if args.data_explorer:
            data_explorer_cli()
            exit()
        if args.render:
            print('Rendering video...')
            for render_type in args.render:
                render(render_type)
            print('Render completed.')


if __name__ == "__main__":
    main()
