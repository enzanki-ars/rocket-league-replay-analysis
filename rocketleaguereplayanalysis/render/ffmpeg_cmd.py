def create_ffmpeg_cmd_files(video_prefix):
    create_ffmpeg_cmd_files_from_path(video_prefix, 'time-game-time',
                                      ['time', 'game_time'])
    create_ffmpeg_cmd_files_from_path(video_prefix, 'time-real-replay-time',
                                      ['time', 'real_replay_time'])
    create_ffmpeg_cmd_files_from_path(video_prefix, 'player-throttle',
                                      ['cars', 'player_num', 'throttle'])
    create_ffmpeg_cmd_files_from_path(video_prefix, 'player-steering',
                                      ['cars', 'player_num', 'steer'])
    create_ffmpeg_cmd_files_from_path(video_prefix, 'player-ping',
                                      ['cars', 'player_num', 'ping'])
    create_ffmpeg_cmd_files_from_path(video_prefix, 'player-boost',
                                      ['cars', 'player_num', 'boost'])
    create_ffmpeg_cmd_files_from_path(video_prefix, 'player-sleep',
                                      ['cars', 'player_num', 'sleep'])
    create_ffmpeg_cmd_files_from_path(video_prefix, 'player-drift',
                                      ['cars', 'player_num', 'drift'])
    create_ffmpeg_cmd_files_from_path(video_prefix, 'player-scoreboard-score',
                                      ['cars', 'player_num', 'scoreboard',
                                       'score'])
    create_ffmpeg_cmd_files_from_path(video_prefix, 'player-scoreboard-goals',
                                      ['cars', 'player_num', 'scoreboard',
                                       'goals'])
    create_ffmpeg_cmd_files_from_path(video_prefix,
                                      'player-scoreboard-assists',
                                      ['cars', 'player_num', 'scoreboard',
                                       'assists'])
    create_ffmpeg_cmd_files_from_path(video_prefix, 'player-scoreboard-saves',
                                      ['cars', 'player_num', 'scoreboard',
                                       'saves'])
    create_ffmpeg_cmd_files_from_path(video_prefix, 'player-scoreboard-shots',
                                      ['cars', 'player_num', 'scoreboard',
                                       'shots'])

    pass


def create_ffmpeg_cmd_files_from_path(video_prefix, name, path):
    import functools
    import os

    from tqdm import tqdm

    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info
    from rocketleaguereplayanalysis.parser.frames import get_frames

    if os.path.exists(os.path.join(video_prefix, name + '.txt')):
        os.remove(os.path.join(video_prefix, name + '.txt'))

    for player in get_player_info().keys():
        if os.path.exists(os.path.join(video_prefix,
                                       name + '-' + str(player) + '.txt')):
            os.remove(os.path.join(video_prefix,
                                   name + '-' + str(player) + '.txt'))

    frames = get_frames()

    if 'player_num' in path:
        for player in get_player_info().keys():
            with open(os.path.join(video_prefix,
                                   name + '-' + str(player) + '.txt'),
                      'a') as f:
                new_path = list(replace_in_array(path, 'player_num', player))
                player_num = str(player)
                for i in tqdm(range(0, len(frames)),
                              desc='Video Output - ' + name + '-' + player_num,
                              ascii=True):
                    f.write(str(frames[i]['time']['real_replay_time']) +
                            " drawtext@" + name + "-" + player_num +
                            " reinit 'text=" +
                            str(functools.reduce(lambda d, key: d[key],
                                                 new_path, frames[i])) +
                            "';\n")
    else:
        with open(os.path.join(video_prefix,
                               name + '.txt'), 'a') as f:
            for i in tqdm(range(0, len(frames)), desc='Video Output - ' + name,
                          ascii=True):
                f.write(str(frames[i]['time']['real_replay_time']) +
                        " drawtext@" + name +
                        " reinit 'text=" +
                        str(functools.reduce(lambda d, key: d[key],
                                             path, frames[i])) + "';\n")


def replace_in_array(it, find, replacement):
    array = []
    for item in it:
        if find == item:
            array.append(replacement)
        else:
            array.append(item)
    return array
