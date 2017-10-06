render_type = 'player-data-scoreboard'


def render_player_data_scoreboard(out_prefix):
    import os
    from pathlib import Path

    from tqdm import tqdm

    from rocketleagueminimapgenerator.parser.frames import get_frames
    from rocketleagueminimapgenerator.data.data_loader import get_data_start, \
        get_data_end

    frames = get_frames()

    for player_id in frames[get_data_start()]['cars'].keys():
        if not os.path.exists(
                os.path.join(out_prefix, render_type, str(player_id))):
            path = Path(
                    os.path.join(out_prefix, render_type, str(player_id)))
            path.mkdir(parents=True)

    for i in tqdm(range(get_data_start(), get_data_end()),
                  desc='Player Data Scoreboard Render',
                  ascii=True):
        render_player_data_scoreboard_frame(frames=frames, frame_num=i,
                                            out_prefix=out_prefix)


def render_player_data_scoreboard_frame(frames, frame_num, out_prefix):
    import os

    import cairosvg

    from rocketleagueminimapgenerator.main import frame_num_format, \
        player_data_scoreboard_template
    from rocketleagueminimapgenerator.data.object_numbers import \
        get_player_info, get_player_team_name

    moving_data_width = 185.044  # 96.3549

    for player_id in frames[frame_num]['cars'].keys():
        with open(os.path.join(out_prefix, render_type, str(player_id),
                               frame_num_format.format(frame_num) + '.png'),
                  'wb') as file_out:
            player_frame_info = frames[frame_num]['cars'][player_id]
            player_scoreboard = player_frame_info['scoreboard']
            player_name = get_player_info()[player_id]['name']
            player_team = get_player_team_name(player_id)

            cairosvg.svg2png(bytestring=bytes(
                    player_data_scoreboard_template.format(
                            player_name=player_name,
                            team=player_team,
                            score='{0:04d}'.format(player_scoreboard['score']),
                            goals=player_scoreboard['goals'],
                            assists=player_scoreboard['assists'],
                            saves=player_scoreboard['saves'],
                            shots=player_scoreboard['shots'],
                            sleep=str(player_frame_info['sleep'])[0],
                            ping=player_frame_info['ping'],
                            throttle=(player_frame_info['throttle'] *
                                      moving_data_width),
                            steer=(player_frame_info['steer'] * 180) - 90
                    ), 'UTF-8'), write_to=file_out)
