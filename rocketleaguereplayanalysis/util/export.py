def export_parsed_data(prefix):
    import json
    import os

    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.util.extra_info import get_field_dimensions

    export = {
        'player_info': get_player_info(),
        'field_size': get_field_dimensions(),
        'frames': get_frames()
    }

    with open(os.path.join(prefix + '-export-parsed-data.json'),
              'w') as export_file:
        json.dump(export, export_file)
