import os
import pickle


def load():
    info_path = os.path.join(os.path.dirname(__file__), './info.p')

    with open(info_path, 'rb') as f:
        info = pickle.load(f)
        return info


def save(info):
    info_path = os.path.join(os.path.dirname(__file__), './info.p')
    with open(info_path, 'wb') as f:
        pickle.dump(info, f, protocol=pickle.HIGHEST_PROTOCOL)
