def parse_loc_update(updated_data):
    update = updated_data['TAGame.RBActor_TA:ReplicatedRBState']

    returned_data = {}
    if 'Position' in update:
        if 'X' in update['Position']:
            returned_data['x'] = update['Position']['X']
        if 'Y' in update['Position']:
            returned_data['y'] = update['Position']['Y']
        if 'Z' in update['Position']:
            returned_data['z'] = update['Position']['Z']

    return returned_data


def parse_rot_update(updated_data):
    update = updated_data['TAGame.RBActor_TA:ReplicatedRBState']

    returned_data = {}

    if 'rotation' in update:
        if 'X' in update['Rotation']:
            returned_data['x'] = update['Rotation']['X'] * 360
        if 'Y' in update['rotation']:
            returned_data['y'] = update['Rotation']['Y'] * 360
        if 'Z' in update['rotation']:
            returned_data['z'] = update['Rotation']['Z'] * 360

    return returned_data


def parse_ang_vel_update(updated_data):
    update = updated_data['TAGame.RBActor_TA:ReplicatedRBState']

    returned_data = {}
    if 'angular_velocity' in update and update['AngularVelocity']:
        if 'X' in update['AngularVelocity']:
            returned_data['x'] = update['AngularVelocity']['X']
        if 'Y' in update['AngularVelocity']:
            returned_data['y'] = update['AngularVelocity']['Y']
        if 'Z' in update['AngularVelocity']:
            returned_data['z'] = update['AngularVelocity']['Z']

    return returned_data


def parse_lin_vel_update(updated_data):
    update = updated_data['TAGame.RBActor_TA:ReplicatedRBState']

    returned_data = {}
    if 'LinearVelocity' in update and update['LinearVelocity']:
        if 'X' in update['LinearVelocity']:
            returned_data['x'] = update['LinearVelocity']['X']
        if 'Y' in update['LinearVelocity']:
            returned_data['y'] = update['LinearVelocity']['Y']
        if 'Z' in update['LinearVelocity']:
            returned_data['z'] = update['LinearVelocity']['Z']

    return returned_data


def parse_sleep_update(updated_data):
    update = updated_data['TAGame.RBActor_TA:ReplicatedRBState']

    if 'Sleeping' in update:
        return update['Sleeping']
