def update_game_data(frame_data, frames, i):
    if 'updated_replication_value' in frame_data['value'].keys():
        for updated_data in frame_data['value']['updated_replication_value']:
            if updated_data['name'] == \
                    'TAGame.GameEvent_Soccar_TA:SecondsRemaining':
                frames[i]['game_data']['sec_remaining'] = \
                    updated_data['value']['int_attribute_value']


def update_car_data(frame_data, frames, i, player_id):
    from rocketleagueminimapgenerator.parser.location import \
        parse_loc_spawn, parse_rot_spawn, parse_loc_update, parse_rot_update, \
        parse_sleep_update, parse_lin_vel_update, parse_ang_vel_update

    if 'spawned_replication_value' in frame_data['value'].keys():

        loc = parse_loc_spawn(frame_data)
        rot = parse_rot_spawn(frame_data)
        if loc:
            frames[i]['cars'][player_id]['loc'].update(loc)
        if rot:
            frames[i]['cars'][player_id]['rot'].update(rot)
    elif 'updated_replication_value' in frame_data['value'].keys():
        for updated_data in \
                frame_data['value']['updated_replication_value']:
            if updated_data['name'] == \
                    'TAGame.RBActor_TA:ReplicatedRBState':
                loc = parse_loc_update(updated_data)
                rot = parse_rot_update(updated_data)
                ang_vel = parse_ang_vel_update(updated_data)
                lin_vel = parse_lin_vel_update(updated_data)
                sleep = parse_sleep_update(updated_data)

                if loc:
                    frames[i]['cars'][player_id]['loc'].update(loc)
                if rot:
                    frames[i]['cars'][player_id]['rot'].update(rot)
                if ang_vel:
                    frames[i]['cars'][player_id]['ang_vel'].update(ang_vel)
                if lin_vel:
                    frames[i]['cars'][player_id]['lin_vel'].update(lin_vel)
                if sleep:
                    frames[i]['cars'][player_id]['sleep'] = sleep
            elif updated_data['name'] == \
                    'TAGame.CarComponent_Boost_TA:ReplicatedBoostAmount':
                frames[i]['cars'][player_id]['boost'] = \
                    updated_data['value']['byte_attribute_value'] / 255
            elif updated_data['name'] == \
                    'TAGame.Vehicle_TA:ReplicatedThrottle':
                frames[i]['cars'][player_id]['throttle'] = \
                    updated_data['value']['byte_attribute_value'] / 255
            elif updated_data['name'] == 'TAGame.Vehicle_TA:ReplicatedSteer':
                frames[i]['cars'][player_id]['steer'] = \
                    updated_data['value']['byte_attribute_value'] / 255


def update_player_data(frame_data, frames, i, actor_id):
    if 'updated_replication_value' in frame_data['value'].keys():
        for updated_data in frame_data['value']['updated_replication_value']:
            if updated_data['name'] == 'Engine.PlayerReplicationInfo:Ping':
                frames[i]['cars'][actor_id]['ping'] = \
                    updated_data['value']['byte_attribute_value']
            elif updated_data['name'] == 'TAGame.PRI_TA:MatchScore':
                frames[i]['cars'][actor_id]['scoreboard']['score'] = \
                    updated_data['value']['int_attribute_value']
            elif updated_data['name'] == 'TAGame.PRI_TA:MatchGoals':
                frames[i]['cars'][actor_id]['scoreboard']['goals'] = \
                    updated_data['value']['int_attribute_value']
            elif updated_data['name'] == 'TAGame.PRI_TA:MatchAssists':
                frames[i]['cars'][actor_id]['scoreboard']['assists'] = \
                    updated_data['value']['int_attribute_value']
            elif updated_data['name'] == 'TAGame.PRI_TA:MatchSaves':
                frames[i]['cars'][actor_id]['scoreboard']['saves'] = \
                    updated_data['value']['int_attribute_value']
            elif updated_data['name'] == 'TAGame.PRI_TA:MatchShots':
                frames[i]['cars'][actor_id]['scoreboard']['shots'] = \
                    updated_data['value']['int_attribute_value']


def update_ball_data(frame_data, frames, i):
    from rocketleagueminimapgenerator.parser.location import \
        parse_loc_spawn, parse_rot_spawn, parse_loc_update, parse_rot_update, \
        parse_sleep_update

    if 'spawned_replication_value' in frame_data['value'].keys():
        loc = parse_loc_spawn(frame_data)
        rot = parse_rot_spawn(frame_data)
        if loc:
            frames[i]['ball']['loc'].update(loc)
        if rot:
            frames[i]['ball']['rot'].update(rot)
    elif 'updated_replication_value' in frame_data['value'].keys():
        for updated_data in \
                frame_data['value']['updated_replication_value']:
            if updated_data['name'] == 'TAGame.RBActor_TA:ReplicatedRBState':
                loc = parse_loc_update(updated_data)
                rot = parse_rot_update(updated_data)
                sleep = parse_sleep_update(updated_data)
                if loc:
                    frames[i]['ball']['loc'].update(loc)
                if rot:
                    frames[i]['ball']['rot'].update(rot)
                if sleep:
                    frames[i]['ball']['sleep'] = sleep
