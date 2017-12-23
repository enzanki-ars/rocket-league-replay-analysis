frames = None


def get_frames():
    global frames
    return frames


def load_frames():
    global frames

    import copy

    from tqdm import tqdm

    from rocketleaguereplayanalysis.data.data_loader import get_data, \
        max_data_end
    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info, get_game_event_num
    from rocketleaguereplayanalysis.parser.frame_data import \
        update_game_data, update_car_data, update_player_data, update_ball_data

    data = get_data()

    current_ball_object = None
    current_car_objects = {}
    player_info = get_player_info()
    game_event_num = get_game_event_num()

    frames = [len(data['Frames'])]
    frames[0] = {
        'time': {
            'replay_time': data['Frames'][0]['Delta'],
            'server_time': data['Frames'][0]['Time'],
            'game_time': 300,
            'replay_delta': data['Frames'][0]['Delta'],
            'server_delta': data['Frames'][0]['Delta'],
            'real_replay_delta': data['Frames'][0]['Delta']
        },
        'ball': {'loc': {'x': 0, 'y': 0, 'z': 0},
                 'rot': {'x': 0, 'y': 0, 'z': 0},
                 'sleep': True,
                 'last_hit': None},
        'cars': {}
    }

    for player_id in player_info.keys():
        current_car_objects[player_id] = None
        frames[0]['cars'][player_id] = {
            'loc': {'x': None, 'y': None, 'z': None},
            'rot': {'x': 0, 'y': 0, 'z': 0},
            'ang_vel': {'x': 0, 'y': 0, 'z': 0},
            'lin_vel': {'x': 0, 'y': 0, 'z': 0},
            'throttle': .5,
            'steer': .5,
            'ping': 0,
            'boost': 0,
            'sleep': True,
            'drift': False,
            '2nd_cam': False,
            'driving': False,
            'scoreboard': {
                'score': 0,
                'goals': 0,
                'assists': 0,
                'saves': 0,
                'shots': 0
            }
        }

    for i in tqdm(range(0, max_data_end()), desc='Parsing Frame Data',
                  ascii=True):

        if i > 0:
            frames.append(copy.deepcopy(frames[i - 1]))

        server_time = data['Frames'][i]['Time']
        replay_time = frames[i - 1]['time']['replay_time'] + \
                      data['Frames'][i]['Delta']
        server_delta = data['Frames'][i]['Time'] - \
                       data['Frames'][i - 1]['Time']
        replay_delta = data['Frames'][i]['Delta']

        if replay_delta == 0:
            # There seems to have been a goal here.
            real_replay_delta = replay_delta
        else:
            real_replay_delta = server_delta

        frames[i]['time'] = {
            'replay_time': replay_time,
            'server_time': server_time,
            'replay_delta': replay_delta,
            'server_delta': server_delta,
            'real_replay_delta': real_replay_delta
        }

        for update in data['Frames'][i]['ActorUpdates']:
            actor_id = update['Id']

            if 'ClassName' in update and \
                    ('TAGame.Ball_TA' in update['ClassName']):
                current_ball_object = actor_id
            if 'ClassName' in update and \
                    ('TAGame.Car_TA' in update['ClassName']):
                player = update['Engine.Pawn:PlayerReplicationInfo']['ActorId']
                current_car_objects[player] = update['Id']

            if actor_id == current_ball_object:
                update_ball_data(update, frames, i)
            elif actor_id in player_info.keys():
                update_player_data(update, frames, i, actor_id)
            elif actor_id == game_event_num:
                update_game_data(update, frames, i)
            else:
                for player_id in current_car_objects:
                    if actor_id == current_car_objects[player_id]:
                        update_car_data(update, frames, i, player_id)

        for actor_id in data['Frames'][i]['DeletedActorIds']:
            if actor_id == current_ball_object:
                frames[i]['ball'] = {'loc': {'x': 0, 'y': 0, 'z': 0},
                                     'rot': {'x': 0, 'y': 0, 'z': 0},
                                     'sleep': True}
            else:
                for player_id in current_car_objects:
                    if actor_id == current_car_objects[player_id]:
                        current_car_objects[player_id] = None
                        frames[i]['cars'][player_id]['loc'] = {'x': None,
                                                               'y': None,
                                                               'z': None}
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
                        frames[i]['cars'][player_id]['drift'] = False
                        frames[i]['cars'][player_id]['2nd_cam'] = False
                        frames[i]['cars'][player_id]['driving'] = False
