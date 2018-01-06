def create_ffmpeg_cmd_files():
    create_ffmpeg_cmd_files_from_path(['frames', 'frame_num', 'time',
                                       'game_time'])
    create_ffmpeg_cmd_files_from_path(['frames', 'frame_num', 'time',
                                       'real_replay_time'])
    create_ffmpeg_cmd_files_from_path(['frames', 'frame_num', 'cars',
                                       'player_num', 'throttle'])
    create_ffmpeg_cmd_files_from_path(['frames', 'frame_num', 'cars',
                                       'player_num', 'steer'])
    create_ffmpeg_cmd_files_from_path(['frames', 'frame_num', 'cars',
                                       'player_num', 'ping'])
    create_ffmpeg_cmd_files_from_path(['frames', 'frame_num', 'cars',
                                       'player_num', 'boost'])
    create_ffmpeg_cmd_files_from_path(['frames', 'frame_num', 'cars',
                                       'player_num', 'sleep'])
    create_ffmpeg_cmd_files_from_path(['frames', 'frame_num', 'cars',
                                       'player_num', 'drift'])
    create_ffmpeg_cmd_files_from_path(['frames', 'frame_num', 'cars',
                                       'player_num', 'scoreboard', 'score'])
    create_ffmpeg_cmd_files_from_path(['frames', 'frame_num', 'cars',
                                       'player_num', 'scoreboard', 'goals'])
    create_ffmpeg_cmd_files_from_path(['frames', 'frame_num', 'cars',
                                       'player_num', 'scoreboard', 'assists'])
    create_ffmpeg_cmd_files_from_path(['frames', 'frame_num', 'cars',
                                       'player_num', 'scoreboard', 'saves'])
    create_ffmpeg_cmd_files_from_path(['frames', 'frame_num', 'cars',
                                       'player_num', 'scoreboard', 'shots'])

    pass


def create_ffmpeg_cmd_files_from_path(path):
    import functools
    import os

    from tqdm import tqdm

    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info
    from rocketleaguereplayanalysis.parser.frames import get_frames
    from rocketleaguereplayanalysis.util.export import get_all_data
    from rocketleaguereplayanalysis.render.do_render import get_video_prefix

    all_data = get_all_data()
    frames = get_frames()
    player_info = get_player_info()

    video_prefix = get_video_prefix()

    name = '-'.join(path)
    if os.path.exists(os.path.join(video_prefix, name + '.txt')):
        os.remove(os.path.join(video_prefix, name + '.txt'))

    for player in player_info.keys():
        if os.path.exists(os.path.join(name + '-' + str(player) + '.txt')):
            os.remove(os.path.join(video_prefix,
                                   name + '-' + str(player) + '.txt'))

    last_val = None

    if 'player_num' in path:
        for player in player_info.keys():

            new_path = list(replace_in_array(path, 'player_num', player))
            new_name = '-'.join(str(x) for x in new_path)

            with open(os.path.join(video_prefix, new_name + '.txt'),
                      'a') as f:

                if 'frame_num' in path:
                    for i in tqdm(range(0, len(frames)),
                                  desc='Video Output - ' + new_name,
                                  ascii=True):
                        frame_path = list(
                                replace_in_array(new_path, 'frame_num', i))

                        curr_val = str(functools.reduce(lambda d, key: d[key],
                                                        frame_path, all_data))

                        if curr_val != last_val:
                            write_to_file(f, new_name, i, curr_val)
                        last_val = curr_val
                else:
                    curr_val = str(functools.reduce(lambda d, key: d[key],
                                                    new_path, all_data))
                    if curr_val != last_val:
                        write_to_file(f, new_name, 0, curr_val)
                    last_val = curr_val

    else:
        with open(os.path.join(video_prefix,
                               name + '.txt'), 'a') as f:
            if 'frame_num' in path:
                for i in tqdm(range(0, len(frames)),
                              desc='Video Output - ' + name,
                              ascii=True):
                    frame_path = list(replace_in_array(path, 'frame_num', i))

                    curr_val = str(functools.reduce(lambda d, key: d[key],
                                                    frame_path,
                                                    all_data))

                    if curr_val != last_val:
                        write_to_file(f, name, i, curr_val)

                    last_val = curr_val
            else:
                curr_val = str(functools.reduce(lambda d, key: d[key],
                                                path,
                                                all_data))

                write_to_file(f, name, 0, curr_val)


def write_to_file(file, name, frame_num, value):
    from rocketleaguereplayanalysis.parser.frames import get_frames

    file.write(str(get_frames()[frame_num]['time']['real_replay_time']) +
               " drawtext@" + name +
               " reinit 'text=" + value + "';\n")


def replace_in_array(it, find, replacement):
    array = []
    for item in it:
        if find == item:
            array.append(replacement)
        else:
            array.append(item)
    return array
