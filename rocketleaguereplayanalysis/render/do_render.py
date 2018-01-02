import os


def do_render_minimap(video_prefix):
    from rocketleaguereplayanalysis.util.transcode import render_video

    render_video(video_prefix, 'minimap')


def do_render_pressure(video_prefix):
    from rocketleaguereplayanalysis.util.transcode import render_video

    render_video(video_prefix, 'pressure', overlay='bar-comparison')


def do_render_possession(video_prefix):
    from rocketleaguereplayanalysis.util.transcode import render_video

    render_video(video_prefix, 'possession', overlay='bar-comparison')


def do_render_player_data_scoreboard(video_prefix):
    from rocketleaguereplayanalysis.util.transcode import render_video
    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info, get_player_team_name

    for player_id in get_player_info().keys():
        team_color = get_player_team_name(player_id)

        render_video(video_prefix,
                     os.path.join('player-data-scoreboard',
                                  str(player_id)),
                     overlay='player-data-scoreboard-' + team_color)


def do_render_player_data_drive(video_prefix):
    from rocketleaguereplayanalysis.util.transcode import render_video
    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info, get_player_team_name

    for player_id in get_player_info().keys():
        team_color = get_player_team_name(player_id)

        render_video(video_prefix,
                     os.path.join('player-data-drive', str(player_id)),
                     overlay='player-data-drive-' + team_color)
