frames = None


def get_frames():
    global frames
    return frames


def load_frames():
    global frames

    import copy

    from tqdm import tqdm

    from rocketleagueminimapgenerator.data.data_loader import get_data, \
        get_data_end
    from rocketleagueminimapgenerator.data.object_numbers import \
        get_ball_obj_nums, get_car_obj_nums, get_player_info, \
        get_game_event_num
    from rocketleagueminimapgenerator.parser.frame_data import \
        update_game_data, update_car_data, update_player_data, update_ball_data

    data = get_data()

    ball_objects = get_ball_obj_nums()
    car_objects = get_car_obj_nums()
    player_info = get_player_info()
    game_event_num = get_game_event_num()

    data_end = get_data_end()

    frames = [len(data['Frames'])]
    frames[0] = {'time': data['Frames'][0]['Time'],
                 'delta': 0,
                 'ball': {'loc': {'x': 0, 'y': 0, 'z': 0},
                          'rot': {'x': 0, 'y': 0, 'z': 0},
                          'sleep': True},
                 'cars': {},
                 'game_data': {
                     'sec_remaining': 300
                 }}

    for player_id in player_info.keys():
        frames[0]['cars'][player_id] = {
            'loc': {'x': -10000, 'y': -10000, 'z': -10000},
            'rot': {'x': 0, 'y': 0, 'z': 0},
            'ang_vel': {'x': 0, 'y': 0, 'z': 0},
            'lin_vel': {'x': 0, 'y': 0, 'z': 0},
            'throttle': .5,
            'steer': .5,
            'ping': 0,
            'boost': 0,
            'sleep': True,
            'scoreboard': {
                'score': 0,
                'goals': 0,
                'assists': 0,
                'saves': 0,
                'shots': 0
            }
        }

    for i in tqdm(range(0, data_end), desc='Parsing Frame Data', ascii=True):

        if i > 0:
            frames.append(copy.deepcopy(frames[i - 1]))

        frames[i]['time'] = data['Frames'][i]['Time']
        frames[i]['delta'] = frames[i]['time'] - frames[i - 1]['time']

        for update in data['Frames'][i]['ActorUpdates']:
            actor_id = update['Id']

            if actor_id in ball_objects:
                update_ball_data(update, frames, i)
            elif actor_id in player_info.keys():
                update_player_data(update, frames, i, actor_id)
            elif actor_id in car_objects:
                player_id = car_objects[actor_id]

                update_car_data(update, frames, i, player_id)
            elif actor_id == game_event_num:
                update_game_data(update, frames, i)

        for delete in data['Frames'][i]['DeletedActorIds']:
            actor_id = delete

            if actor_id in ball_objects:
                frames[i]['ball'] = {'loc': {'x': 0, 'y': 0, 'z': 0},
                                     'rot': {'x': 0, 'y': 0, 'z': 0},
                                     'sleep': True}
            elif actor_id in car_objects:
                player_id = car_objects[actor_id]

                frames[i]['cars'][player_id]['loc'] = {'x': -10000,
                                                       'y': -10000,
                                                       'z': -10000}
                frames[i]['cars'][player_id]['rot'] = {'x': 0,
                                                       'y': 0,
                                                       'z': 0}
                frames[i]['cars'][player_id]['ang_vel'] = {'x': 0,
                                                           'y': 0,
                                                           'z': 0}
                frames[i]['cars'][player_id]['lin_vel'] = {'x': 0,
                                                           'y': 0,
                                                           'z': 0}
                frames[i]['cars'][player_id]['throttle'] = .5
                frames[i]['cars'][player_id]['steer'] = .5
                frames[i]['cars'][player_id]['ping'] = 0
                frames[i]['cars'][player_id]['boost'] = 0
                frames[i]['cars'][player_id]['sleep'] = True
