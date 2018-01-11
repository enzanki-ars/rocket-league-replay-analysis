video_prefix = None


def get_video_prefix():
    global video_prefix

    return video_prefix


def set_video_prefix(prefix):
    global video_prefix

    video_prefix = prefix


def render(filename):
    import json
    import os
    from rocketleaguereplayanalysis.main import assets_path_builtin
    from rocketleaguereplayanalysis.render.ffmpeg_cmd import \
        create_ffmpeg_cmd_files_from_path, replace_in_array
    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info
    from rocketleaguereplayanalysis.util.transcode import \
        render_video

    with open(os.path.join(assets_path_builtin, filename + '.json')) as f:
        render_paths = json.load(f)

    is_player_render = False

    for render_cmd in render_paths:
        if 'modify' in render_cmd:
            create_ffmpeg_cmd_files_from_path(path=render_cmd['varaible_path'],
                                              filter_type=render_cmd['filter'],
                                              reinit=render_cmd['reinit'],
                                              modify=render_cmd['modify'])
        else:
            create_ffmpeg_cmd_files_from_path(path=render_cmd['varaible_path'],
                                              filter_type=render_cmd['filter'],
                                              reinit=render_cmd['reinit'])

        if 'player_num' in render_cmd['varaible_path']:
            is_player_render = True

    if is_player_render:
        for player in get_player_info().keys():
            extra_cmd_filter = ''

            for i, render_cmd in enumerate(render_paths, start=1):
                new_path = list(replace_in_array(render_cmd['varaible_path'],
                                                 'player_num', player))
                new_name = '-'.join(str(x) for x in new_path)

                extra_cmd_filter += 'sendcmd=f=' + new_name + '.txt,' + \
                                    render_cmd['filter'] + '@' + new_name

                if render_cmd['filter'] == 'drawtext':
                    extra_cmd_filter += '=fontfile=\\\'' + \
                                        os.path.join(assets_path_builtin,
                                                     'OpenSans.ttf').replace('\\', '\\\\') + '\\\''
                    if 'options' in render_cmd:
                        extra_cmd_filter += ':'
                else:
                    if 'options' in render_cmd:
                        extra_cmd_filter += '='

                if 'options' in render_cmd:
                    for j, option_what in enumerate(
                            render_cmd['options'].keys(),
                            start=1):
                        extra_cmd_filter += option_what + '=' + \
                                            str(render_cmd['options'][
                                                    option_what])

                        if j != len(render_cmd['options'].keys()):
                            extra_cmd_filter += ':'

                if i != len(render_paths):
                    extra_cmd_filter += ','

            render_video(str(player) + '-' + filename,
                         overlay=os.path.join(assets_path_builtin, filename),
                         extra_cmd=['-vf', extra_cmd_filter])
    else:
        extra_cmd_filter = ''

        for i, render_cmd in enumerate(render_paths, start=1):
            name = '-'.join(str(x) for x in render_cmd['varaible_path'])

            extra_cmd_filter += 'sendcmd=f=' + name + '.txt,' + \
                                render_cmd['filter'] + '@' + name + '='

            if render_cmd['filter'] == 'drawtext':
                extra_cmd_filter += '=fontfile=\\\'' + \
                                    os.path.join(assets_path_builtin,
                                                 'OpenSans.ttf').replace('\\', '\\\\') + '\\\''
                if 'options' in render_cmd:
                    extra_cmd_filter += ':'
            else:
                if 'options' in render_cmd:
                    extra_cmd_filter += '='

            if 'options' in render_cmd:
                for j, option_what in enumerate(render_cmd['options'].keys(),
                                                start=1):
                    extra_cmd_filter += option_what + '=' + \
                                        str(render_cmd['options'][option_what])

                    if j != len(render_cmd['options'].keys()):
                        extra_cmd_filter += ':'

            if i != len(render_paths):
                extra_cmd_filter += ','

        render_video(filename,
                     overlay=os.path.join(assets_path_builtin, filename),
                     extra_cmd=['-vf', extra_cmd_filter])
