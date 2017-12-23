def render_possession(out_prefix):
    import os
    from pathlib import Path

    from tqdm import tqdm

    from rocketleaguereplayanalysis.data.data_loader import get_data_start, \
        get_data_end
    from rocketleaguereplayanalysis.parser.frames import get_frames

    if not os.path.exists(os.path.join(out_prefix, 'possession')):
        path = Path(os.path.join(out_prefix, 'possession'))
        path.mkdir(parents=True)

    for i in tqdm(range(get_data_start(), get_data_end()),
                  desc='Possession Render',
                  ascii=True):
        render_frame(frames=get_frames(),
                     frame_num=i,
                     out_prefix=out_prefix)


def render_frame(frames, frame_num, out_prefix):
    import os

    import cairosvg

    from rocketleaguereplayanalysis.main import frame_num_format, \
        bar_comparison_template
    from rocketleaguereplayanalysis.data.object_numbers import team_blue, \
        team_orange

    blue_max_width = 146.672

    with open(os.path.join(out_prefix, 'possession',
                           frame_num_format.format(frame_num) + '.png'),
              'wb') as file_out:
        total = frames[frame_num]['possession'][team_blue] + \
                frames[frame_num]['possession'][team_orange]
        if total > 0:
            blue_percent = (frames[frame_num]['possession'][team_blue]) / total
            orange_percent = (frames[frame_num]['possession'][
                                  team_orange]) / total
        else:
            blue_percent = .5
            orange_percent = .5

        blue_width = blue_percent * blue_max_width

        cairosvg.svg2png(bytestring=bytes(
                bar_comparison_template.format(
                        type='Possession',
                        blue_width=blue_width,
                        blue_percent='{0:03.0f}'.format(blue_percent * 100),
                        orange_percent='{0:03.0f}'.format(
                                orange_percent * 100),
                ), 'UTF-8'), write_to=file_out)
