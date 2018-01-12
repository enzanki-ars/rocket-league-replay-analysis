sync_delta_type = 'real_replay_delta'
sync_time_type = 'real_replay_time'


def set_sync_delta_type(delta_type):
    global sync_delta_type

    sync_delta_type = delta_type


def set_sync_time_type(time_type):
    global sync_time_type

    sync_time_type = time_type


def get_sync_delta_type():
    global sync_delta_type

    return sync_delta_type


def get_sync_time_type():
    global sync_time_type

    return sync_time_type
