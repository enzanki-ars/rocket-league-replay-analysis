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


def get_xp_level(xp):
    levels = [(1000, 1),
              (2000, 2),
              (3250, 3),
              (4750, 4),
              (6500, 5),
              (9250, 6),
              (13000, 7),
              (17750, 8),
              (23500, 9),
              (30250, 10),
              (38750, 11),
              (49000, 12),
              (61000, 13),
              (74750, 14),
              (90250, 15),
              (108250, 16),
              (128750, 17),
              (151750, 18),
              (177250, 19),
              (205250, 20),
              (236500, 21),
              (271000, 22),
              (308750, 23),
              (349750, 24),
              (394000, 25),
              (442250, 26),
              (494500, 27),
              (550750, 28),
              (611000, 29),
              (675250, 30),
              (744250, 31),
              (818000, 32),
              (896500, 33),
              (979750, 34),
              (1067750, 35),
              (1161250, 36),
              (1260250, 37),
              (1364750, 38),
              (1474750, 39),
              (1590250, 40),
              (1712000, 41),
              (1840000, 42),
              (1974250, 43),
              (2114750, 44),
              (2261500, 45),
              (2415250, 46),
              (2576000, 47),
              (2743750, 48),
              (2918500, 49),
              (3100250, 50),
              (3289750, 51),
              (3487000, 52),
              (3692000, 53),
              (3904750, 54),
              (4125250, 55),
              (4354250, 56),
              (4591750, 57),
              (4837750, 58),
              (5092250, 59),
              (5355250, 60),
              (5627500, 61),
              (5909000, 62),
              (6199750, 63),
              (6499750, 64),
              (6809000, 65),
              (7128250, 66),
              (7457500, 67),
              (7796750, 68),
              (8146000, 69),
              (8505250, 70),
              (8875250, 71),
              (9256000, 72),
              (9647500, 73),
              (10049750, 74),
              (10462750, 75)]

    for xp_limit, xp_level in levels:
        if xp <= xp_limit:
            return xp_level


def get_xp_title(xp_level):
    titles = [(9, 'Rookie'),
              (19, 'Semi-Pro'),
              (29, 'Pro'),
              (39, 'Veteran'),
              (49, 'Expert'),
              (59, 'Master'),
              (73, 'Legend'),
              (75, 'Rocketeer')]

    for level, title in titles:
        if xp_level <= level:
            return title


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
                if 'TAGame.PRI_TA:TotalXP' in update.keys():
                    player_info[player_id]['xp'] = \
                        update['TAGame.PRI_TA:TotalXP']
                    player_info[player_id]['xp_level'] = \
                        get_xp_level(update['TAGame.PRI_TA:TotalXP'])
                    player_info[player_id]['xp_title'] = \
                        get_xp_title(player_info[player_id]['xp_level'])
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


def get_player_team_id(player_id):
    if get_player_info()[player_id]['team'] == team0:
        return 'team0'
    elif get_player_info()[player_id]['team'] == team1:
        return 'team1'
    else:
        return None


def get_player_team_name(player_id):
    if get_player_info()[player_id]['team'] == team0:
        return 'Blue'
    elif get_player_info()[player_id]['team'] == team1:
        return 'Orange'
    else:
        return 'Unknown'


def get_player_team_color(player_id):
    if get_player_info()[player_id]['team'] == team0:
        return '0x7f7fff'
    elif get_player_info()[player_id]['team'] == team1:
        return '0xffb27f'
    else:
        return '0xc0c0c0'


def get_team_name(team):
    if team == team0:
        return 'Blue'
    elif team == team1:
        return 'Orange'
    elif team == 'team0':
        return 'Blue'
    elif team == 'team1':
        return 'Orange'
    else:
        return 'Unknown'


def get_team_color(team):
    if team == team0:
        return '0x7f7fff'
    elif team == team1:
        return '0xffb27f'
    elif team == 'team0':
        return '0x7f7fff'
    elif team == 'team1':
        return '0xffb27f'
    else:
        return '0xc0c0c0'


def get_player_info():
    return player_info
