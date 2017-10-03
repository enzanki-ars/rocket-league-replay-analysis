render_type = 'player-data-drive'


def render_player_data_drive(out_prefix):
    import os
    import shutil
    from pathlib import Path

    from tqdm import tqdm

    from rocketleagueminimapgenerator.parser.frames import get_frames
    from rocketleagueminimapgenerator.data.data_loader import get_data_start, \
        get_data_end

    frames = get_frames()

    for player_id in frames[get_data_start()]['cars'].keys():
        if os.path.exists(
                os.path.join(out_prefix, render_type, str(player_id))):
            shutil.rmtree(
                    os.path.join(out_prefix, render_type, str(player_id)))

        if not os.path.exists(
                os.path.join(out_prefix, render_type, str(player_id))):
            path = Path(
                    os.path.join(out_prefix, render_type, str(player_id)))
            path.mkdir(parents=True)

    for i in tqdm(range(get_data_start(), get_data_end()),
                  desc='Video Frame Out',
                  ascii=True):
        render_player_data_drive_frame(frames=frames, frame_num=i,
                                       out_prefix=out_prefix)


def render_player_data_drive_frame(frames, frame_num, out_prefix):
    import os

    import cairosvg

    from rocketleagueminimapgenerator.main import frame_num_format, \
        player_data_drive_template
    from rocketleagueminimapgenerator.data.object_numbers import \
        get_player_info

    moving_data_width = 185.044

    for player_id in frames[frame_num]['cars'].keys():
        with open(os.path.join(out_prefix, render_type, str(player_id),
                               frame_num_format.format(frame_num) + '.png'),
                  'wb') as file_out:
            player_frame_info = frames[frame_num]['cars'][player_id]
            player_scoreboard = player_frame_info['scoreboard']
            player_name = get_player_info()[player_id]['name']
            player_team = get_player_info()[player_id]['team']

            cairosvg.svg2png(bytestring=bytes(
                    player_data_drive_template.format(
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
                            steer=(player_frame_info['steer'] * 360)
                    ), 'UTF-8'), write_to=file_out)
