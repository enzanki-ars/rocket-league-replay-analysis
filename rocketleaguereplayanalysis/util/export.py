def get_all_data():
    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.util.extra_info import get_field_dimensions

    from rocketleaguereplayanalysis.data.object_numbers import team0, team1
    return {
        'team_info': {
            'number': {
                'team0': team0,
                'team1': team1
            },
            'name': {
                'note': 'Not Fully Implemented Yet',
                'team0': 'Blue',
                'team1': 'Orange'
            }
        },
        'player_info': get_player_info(),
        'field_size': get_field_dimensions(),
        'frames': get_frames()
    }


def export_parsed_data():
    import json
    import os

    from rocketleaguereplayanalysis.render.do_render import get_video_prefix

    video_prefix = get_video_prefix()

    with open(os.path.join(video_prefix + '-export-parsed-data.json'),
              'w') as export_file:
        json.dump(get_all_data(), export_file)
