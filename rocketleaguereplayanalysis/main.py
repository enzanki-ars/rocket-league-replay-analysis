import argparse
import os
import time

from rocketleaguereplayanalysis.data.actor_data import parse_actor_data
from rocketleaguereplayanalysis.data.data_loader import load_data, \
    set_data_start, set_data_end
from rocketleaguereplayanalysis.data.object_numbers import \
    parse_player_info, get_player_info, get_player_team_name
from rocketleaguereplayanalysis.parser.frames import load_frames
from rocketleaguereplayanalysis.render.minimap import render_field
from rocketleaguereplayanalysis.render.player_data_drive import \
    render_player_data_drive
from rocketleaguereplayanalysis.render.player_data_scoreboard import \
    render_player_data_scoreboard
from rocketleaguereplayanalysis.render.player_data_scoreboard_with_drive \
    import render_player_data_scoreboard_with_drive
from rocketleaguereplayanalysis.render.possession import render_possession
from rocketleaguereplayanalysis.render.pressure import render_pressure
from rocketleaguereplayanalysis.render.transcode import render_video
from rocketleaguereplayanalysis.util.data_explorer import data_explorer_cli

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
                        default='video_minimap')

    # Optional args
    parser.add_argument('--data_start',
                        help='Number of frames to render (start).',
                        type=int)
    parser.add_argument('--data_end',
                        help='Number of frames to render (end).',
                        type=int)

    args = parser.parse_args()

    out_prefix = os.path.basename(args.game_json)

    load_data(args.game_json)
    parse_actor_data()
    parse_player_info()
    load_frames()

    video_prefix = os.path.join('renders', out_prefix.split('.')[0])
    if args.data_start:
        set_data_start(args.data_start)
    if args.data_end:
        set_data_end(args.data_end)

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
        print('Unexpected Argument Error:',
              'process_type is', args.process_type)


def do_render_minimap(video_prefix):
    render_field(video_prefix)
    render_video(video_prefix, 'minimap')


def do_render_pressure(video_prefix):
    render_pressure(video_prefix)
    render_video(video_prefix, 'pressure', overlay='bar-comparison')


def do_render_possession(video_prefix):
    render_possession(video_prefix)
    render_video(video_prefix, 'possession', overlay='bar-comparison')


def do_render_player_data_scoreboard_with_drive(video_prefix):
    render_player_data_scoreboard_with_drive(video_prefix)
    for player_id in get_player_info().keys():
        team_color = get_player_team_name(player_id)

        render_video(video_prefix,
                     os.path.join('player-data-scoreboard-with-drive',
                                  str(player_id)),
                     overlay='player-data-scoreboard-with-drive-' +
                             team_color)


def do_render_player_data_scoreboard(video_prefix):
    render_player_data_scoreboard(video_prefix)
    for player_id in get_player_info().keys():
        team_color = get_player_team_name(player_id)

        render_video(video_prefix,
                     os.path.join('player-data-scoreboard',
                                  str(player_id)),
                     overlay='player-data-scoreboard-' + team_color)


def do_render_player_data_drive(video_prefix):
    render_player_data_drive(video_prefix)
    for player_id in get_player_info().keys():
        team_color = get_player_team_name(player_id)

        render_video(video_prefix,
                     os.path.join('player-data-drive', str(player_id)),
                     overlay='player-data-drive-' + team_color)


if __name__ == "__main__":
    main()
