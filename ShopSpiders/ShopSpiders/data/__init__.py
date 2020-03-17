"""Init File to """
from os import path


def get_data_file(filename):
    data_path = path.join('data', filename)
    return data_path
