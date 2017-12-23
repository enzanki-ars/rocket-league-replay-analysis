def export_parsed_data(prefix):
    import json
    import os

    from pprint import pprint

    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info
    from rocketleaguereplayanalysis.parser.frames import get_frames

    export = {
        'player_info': get_player_info(),
        'frames': get_frames()
    }

    with open(os.path.join(prefix + '-export-parsed-data.json'), 'w') as export_file:
        json.dump(export, export_file)
