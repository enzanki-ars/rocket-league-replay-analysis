import os

video_prefix = None


def get_video_prefix():
    global video_prefix

    return video_prefix


def set_video_prefix(prefix):
    global video_prefix

    video_prefix = prefix


def do_render_minimap():
    from rocketleaguereplayanalysis.util.transcode import render_video

    render_video('minimap')


def do_render_pressure():
    from rocketleaguereplayanalysis.util.transcode import render_video

    render_video('pressure', overlay='bar-comparison')


def do_render_possession():
    from rocketleaguereplayanalysis.util.transcode import render_video

    render_video('possession', overlay='bar-comparison')


def do_render_player_data_scoreboard():
    from rocketleaguereplayanalysis.util.transcode import render_video
    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info, get_player_team_name

    for player_id in get_player_info().keys():
        team_color = get_player_team_name(player_id)

        render_video(os.path.join('player-data-scoreboard',
                                  str(player_id)),
                     overlay='player-data-scoreboard-' + team_color)


def do_render_player_data_drive():
    from rocketleaguereplayanalysis.util.transcode import render_video
    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info, get_player_team_name

    for player_id in get_player_info().keys():
        team_color = get_player_team_name(player_id)

        render_video(os.path.join('player-data-drive', str(player_id)),
                     overlay='player-data-drive-' + team_color)
