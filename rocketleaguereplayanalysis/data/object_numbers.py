ball_objects = []
car_objects = {}
player_info = {}
game_event_num = None
team0 = None
team1 = None


def parse_game_event_num():
    from rocketleaguereplayanalysis.data.actor_data import get_actor_data

    global game_event_num

    game_event_num = 1

    for obj in get_actor_data():
        if 'TAGame.GameEvent_Soccar_TA' in get_actor_data()[obj]:
            game_event_num = obj
            return


def get_game_event_num():
    return game_event_num


def parse_player_info():
    from rocketleaguereplayanalysis.data.data_loader import get_data

    global player_info, team0, team1

    player_info = {}

    for i in range(0, len(get_data())):
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
                if 'Engine.PlayerReplicationInfo:Team' in update.keys():
                    player_info[player_id]['team'] = \
                        update['Engine.PlayerReplicationInfo:Team']['ActorId']
            elif 'ClassName' in update and update['ClassName'] == \
                    'TAGame.Team_Soccar_TA':
                if update['TypeName'] == 'Archetypes.Teams.Team0':
                    team0 = update['Id']
                elif update['TypeName'] == 'Archetypes.Teams.Team1':
                    team1 = update['Id']
                else:
                    print('wat? Teams don\'t seem to make sense...')
                    print('Found Team 0 (Usually Blue):  ', team0)
                    print('Found Team 1 (Usually Orange):', team1)
                    print('Weird Team:                   ', update['Id'])


def get_player_team_name(player_id):
    if get_player_info()[player_id]['team'] == team0:
        team_name = 'Blue'
    elif get_player_info()[player_id]['team'] == team1:
        team_name = 'Orange'
    else:
        team_name = 'Unknown'

    return team_name


def get_player_team_color(player_id):
    if get_player_info()[player_id]['team'] == team0:
        team_color = '0x7f7fff'
    elif get_player_info()[player_id]['team'] == team1:
        team_color = '0xffb27f'
    else:
        team_color = '0xc0c0c0'

    return team_color


def get_team_name(team):
    if team == team0:
        team_name = 'Blue'
    elif team == team1:
        team_name = 'Orange'
    elif team == 'team0':
        team_name = 'Blue'
    elif team == 'team1':
        team_name = 'Orange'
    else:
        team_name = 'Unknown'

    return team_name


def get_team_color(team):
    if team == team0:
        team_color = '0x7f7fff'
    elif team == team1:
        team_color = '0xffb27f'
    elif team == 'team0':
        team_color = '0x7f7fff'
    elif team == 'team1':
        team_color = '0xffb27f'
    else:
        team_color = '0xc0c0c0'

    return team_color


def get_player_info():
    return player_info
