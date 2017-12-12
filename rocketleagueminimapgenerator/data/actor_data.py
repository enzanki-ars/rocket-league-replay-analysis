actor_data = {}


def get_actor_data():
    return actor_data


def parse_actor_data():
    global actor_data
    from rocketleagueminimapgenerator.data.data_loader import get_data, get_data_end

    for frame in get_data()['Frames'][:get_data_end()]:
        for update in frame['ActorUpdates']:

            actor_id = update['Id']

            if actor_id not in actor_data.keys():
                actor_data[actor_id] = []

            if 'ClassName' in update.keys():
                if update['ClassName'] not in actor_data[actor_id]:
                    actor_data[actor_id].append(update['ClassName'])
