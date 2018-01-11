def create_ffmpeg_cmd_files_from_path(path, filter_type,
                                      reinit=None, modify=None):
    import functools
    import os

    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.util.export import get_all_data
    from rocketleaguereplayanalysis.render.do_render import get_video_prefix

    all_data = get_all_data()
    frames = get_frames()
    player_info = get_player_info()

    video_prefix = get_video_prefix()

    name = '-'.join(str(x) for x in path)
    if not os.path.exists(os.path.join(video_prefix)):
        os.makedirs(os.path.join(video_prefix))

    last_val = None

    if 'player_num' in path:
        for player in player_info.keys():

            new_path = list(replace_in_array(path, 'player_num', player))
            new_name = '-'.join(str(x) for x in new_path)

            if os.path.exists(os.path.join(video_prefix, new_name + '.txt')):
                os.remove(os.path.join(video_prefix, new_name + '.txt'))

            with open(os.path.join(video_prefix, new_name + '.txt'),
                      'a') as f:

                if 'frame_num' in path:
                    for i in range(0, len(frames)):
                        frame_path = list(
                                replace_in_array(new_path, 'frame_num', i))

                        curr_val = functools.reduce(lambda d, key: d[key],
                                                    frame_path, all_data)

                        if curr_val != last_val or i == 0:
                            write_to_file(f, new_name, i, filter_type, reinit,
                                          curr_val, modify)
                        last_val = curr_val
                else:
                    curr_val = functools.reduce(lambda d, key: d[key],
                                                new_path, all_data)
                    write_to_file(f, new_name, 0, filter_type, reinit,
                                  curr_val, modify)

    else:
        if os.path.exists(os.path.join(video_prefix, name + '.txt')):
            os.remove(os.path.join(video_prefix, name + '.txt'))

        with open(os.path.join(video_prefix,
                               name + '.txt'), 'a') as f:
            if 'frame_num' in path:
                for i in range(0, len(frames)):
                    frame_path = list(replace_in_array(path, 'frame_num', i))

                    curr_val = functools.reduce(lambda d, key: d[key],
                                                frame_path,
                                                all_data)

                    if curr_val != last_val or i == 0:
                        write_to_file(f, name, i, filter_type, reinit,
                                      curr_val,
                                      modify)

                    last_val = curr_val
            else:
                curr_val = functools.reduce(lambda d, key: d[key],
                                            path,
                                            all_data)

                write_to_file(f, name, 0, filter_type, reinit, curr_val,
                              modify)


def write_to_file(file, name, frame_num, filter_type, reinit, value,
                  modify=None):
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.data.object_numbers import \
        get_team_color

    file.write(str(get_frames()[frame_num]['time']['real_replay_time']) +
               " " + filter_type + "@" + name +
               " reinit '")

    if reinit:
        for i, reinit_what in enumerate(reinit.keys(), start=1):
            mod_value = value
            if modify:
                for modify_style in modify.keys():
                    if modify_style == 'add':
                        mod_value = mod_value + modify[modify_style]
                    elif modify_style == 'subtract':
                        mod_value = mod_value - modify[modify_style]
                    elif modify_style == 'multiply':
                        mod_value = mod_value * modify[modify_style]
                    elif modify_style == 'divide':
                        mod_value = mod_value / modify[modify_style]
                    elif modify_style == 'mod':
                        mod_value = mod_value % modify[modify_style]
                    elif modify_style == 'replace':
                        for check in modify[modify_style].keys():
                            if check == str(mod_value):
                                mod_value = modify[modify_style][check]
                                break
                    elif modify_style == 'replace_color':
                        mod_value = get_team_color(mod_value)

            file.write(
                reinit_what + '=' + reinit[reinit_what].format(mod_value))
            if i != len(reinit):
                file.write(":")
            else:
                file.write("';")

        file.write("\n")


def replace_in_array(it, find, replacement):
    array = []
    for item in it:
        if find == item:
            array.append(replacement)
        else:
            array.append(item)
    return array
