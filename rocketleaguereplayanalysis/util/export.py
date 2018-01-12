def get_all_data():
    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.util.extra_info import get_field_dimensions

    from rocketleaguereplayanalysis.data.object_numbers import team0, team1, \
        get_team_color, get_team_name
    return {
        'team_info': {
            'number': {
                'team0': team0,
                'team1': team1
            },
            'name': {
                'note': 'Not Fully Implemented Yet',
                'team0': get_team_name(team0),
                'team1': get_team_name(team1),
            },
            'color': {
                'note': 'Not Fully Implemented Yet',
                'team0': get_team_color(team0),
                'team1': get_team_color(team1),
            }
        },
        'player_info': get_player_info(),
        'field_size': get_field_dimensions(),
        'frames': get_frames()
    }


def export_parsed_data_json():
    import json
    import os

    from rocketleaguereplayanalysis.render.do_render import get_video_prefix

    video_prefix = get_video_prefix()

    with open(os.path.join(video_prefix + '-export-parsed-data.json'),
              'w') as export_file:
        json.dump(get_all_data(), export_file)


def flatten(d, parent_key='', sep='_'):
    import collections

    items = []
    for k, v in d.items():
        new_key = parent_key + sep + str(k) if parent_key else str(k)
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def export_parsed_data_csv():
    import csv
    import os

    from rocketleaguereplayanalysis.render.do_render import get_video_prefix

    video_prefix = get_video_prefix()

    with open(os.path.join(video_prefix + '-export-parsed-data.csv'),
              'w', newline='') as csvfile:
        fieldnames = flatten(get_all_data()['frames'][0]).keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')

        writer.writeheader()
        for frame in get_all_data()['frames']:
            writer.writerow(flatten(frame))
