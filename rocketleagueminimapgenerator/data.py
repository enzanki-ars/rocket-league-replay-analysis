import json

data = None


def load_data(out_prefix):
    global data
    with open(out_prefix + '.json') as data_file:
        data = json.load(data_file)


def get_data():
    return data


def get_data_end():
    return len(data['content']['frames'])
