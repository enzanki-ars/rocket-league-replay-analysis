frames = None


def get_frames():
    global frames
    return frames


def load_frames():
    global frames

    import copy

    from tqdm import tqdm

    from rocketleaguereplayanalysis.data.data_loader import get_data, \
        get_data_end
    from rocketleaguereplayanalysis.data.object_numbers import \
        get_player_info, get_game_event_num
    from rocketleaguereplayanalysis.parser.frame_data import \
        update_game_data, update_car_data, update_player_data, update_ball_data

    data = get_data()

    current_ball_object = None
    current_car_objects = {}
    player_info = get_player_info()
    game_event_num = get_game_event_num()

    data_end = get_data_end()

    frames = [len(data['Frames'])]
    frames[0] = {'time': data['Frames'][0]['Time'],
                 'delta': data['Frames'][0]['Delta'],
                 'ball': {'loc': {'x': 0, 'y': 0, 'z': 0},
                          'rot': {'x': 0, 'y': 0, 'z': 0},
                          'sleep': True},
                 'cars': {},
                 'game_data': {
                     'sec_remaining': 300
                 }}

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

    for i in tqdm(range(0, data_end), desc='Parsing Frame Data', ascii=True):

        if i > 0:
            frames.append(copy.deepcopy(frames[i - 1]))

        frames[i]['time'] = data['Frames'][i]['Time']

        replay_delta = data['Frames'][i]['Delta']

        calc_delta = data['Frames'][i]['Time'] - data['Frames'][i - 1]['Time']

        if replay_delta == 0:
            # There seems to have been a goal here.
            frames[i]['delta'] = replay_delta
        else:
            frames[i]['delta'] = calc_delta

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
