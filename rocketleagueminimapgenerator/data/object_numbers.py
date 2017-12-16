ball_objects = []
car_objects = {}
player_info = {}
game_event_num = None
team_blue = None
team_orange = None


def parse_game_event_num():
    from rocketleagueminimapgenerator.data.actor_data import get_actor_data

    global game_event_num

    game_event_num = 1

    for obj in get_actor_data():
        if 'TAGame.GameEvent_Soccar_TA' in get_actor_data()[obj]:
            game_event_num = obj
            return


def get_game_event_num():
    return game_event_num


def parse_player_info():
    from tqdm import tqdm
    from rocketleagueminimapgenerator.data.data_loader import get_data, \
        get_data_end

    global player_info, team_blue, team_orange

    player_info = {}

    for i in tqdm(range(0, get_data_end()), desc='Parsing Player Info',
                  ascii=True):
        for update in get_data()['Frames'][i]['ActorUpdates']:
            if 'ClassName' in update and update['ClassName'] == \
                    'TAGame.PRI_TA':
                player_id = update['Id']

                if player_id not in player_info:
                    player_info[player_id] = {}
                if 'Engine.PlayerReplicationInfo:PlayerName' in update.keys():
                    player_info[player_id]['name'] = \
                        update['Engine.PlayerReplicationInfo:PlayerName']
                if 'TAGame.PRI_TA:ClientLoadouts' in update.keys():
                    player_info[player_id]['items'] = \
                        update['TAGame.PRI_TA:ClientLoadouts']

        for player in get_data()['Properties']['PlayerStats']:
            for player_id in player_info:
                if 'name' in player_info[player_id] \
                        and player_info[player_id]['name'] == player['Name']:
                    player_info[player_id]['team'] = player['Team']

    team_nums = []
    for player in player_info:
        if 'team' in player_info[player]:
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
