"""Init File to """
from os import path


def get_data_file(filename):
    DATA_PATH = path.join('data', filename)
    return DATA_PATH