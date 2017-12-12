ball_objects = []
car_objects = {}
player_info = {}
game_event_num = None
team_blue = None
team_orange = None


def parse_ball_obj_nums():
    from rocketleagueminimapgenerator.data.actor_data import get_actor_data

    global ball_objects

    ball_objects = []

    for i, obj in enumerate(get_actor_data()):
        if 'TAGame.Ball_TA' in get_actor_data()[obj]:
            ball_objects.append(i)


def get_ball_obj_nums():
    return ball_objects


def parse_game_event_num():
    from rocketleagueminimapgenerator.data.actor_data import get_actor_data

    global game_event_num

    game_event_num = 1

    for i, obj in enumerate(get_actor_data()):
        if 'TAGame.GameEvent_Soccar_TA' in get_actor_data()[obj]:
            game_event_num = i
            return


def get_game_event_num():
    return game_event_num


def parse_car_obj_nums():
    from rocketleagueminimapgenerator.data.data_loader import get_data, \
        get_data_end

    global car_objects

    car_objects = {}

    for frame in get_data()['Frames'][:get_data_end()]:
        for update in frame['ActorUpdates']:

            actor_id = update['Id']

            if 'Engine.Pawn:PlayerReplicationInfo' in update.keys():
                if actor_id not in car_objects.keys():
                    player_id = update['Engine.Pawn:PlayerReplicationInfo'][
                        'ActorId']
                    car_objects[actor_id] = player_id


def get_car_obj_nums():
    return car_objects


def parse_player_info():
    from tqdm import tqdm
    from rocketleagueminimapgenerator.data.data_loader import get_data, \
        get_data_end

    global player_info, team_blue, team_orange

    player_info = {}

    for car_id in get_car_obj_nums():
        if get_car_obj_nums()[car_id] not in player_info:
            player_info[get_car_obj_nums()[car_id]] = {}

    for i in tqdm(range(0, get_data_end()), desc='Parsing Player Info',
                  ascii=True):
        for update in get_data()['Frames'][i]['ActorUpdates']:
            if update['Id'] in player_info:
                player_id = update['Id']

                if 'Engine.PlayerReplicationInfo:Team' in update.keys():
                    if 'team' not in player_info[player_id].keys():
                        player_info[player_id]['team'] = \
                            update['Engine.PlayerReplicationInfo:Team'][
                                'ActorId']
                if 'Engine.PlayerReplicationInfo:PlayerName' in update.keys():
                    player_info[player_id]['name'] = \
                        update['Engine.PlayerReplicationInfo:PlayerName']
                if 'TAGame.PRI_TA:ClientLoadouts' in update.keys():
                    player_info[player_id]['items'] = \
                        update['TAGame.PRI_TA:ClientLoadouts']

    team_nums = []
    for player in player_info:
        team_nums.append(player_info[player]['team'])

    team_blue = min(team_nums)
    team_orange = max(team_nums)


def get_player_team_name(player_id):
    if get_player_info()[player_id]['team'] == team_blue:
        team_color = 'blue'
    elif get_player_info()[player_id]['team'] == team_orange:
        team_color = 'orange'
    else:
        team_color = 'grey'

    return team_color


def get_player_info():
    return player_info
