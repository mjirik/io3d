import os
import pathlib


def remove_if_exists(filename):
    """
    Delete file if exists. Do not panic if the file does not exist.
    """
    if os.path.exists(filename):
        os.remove(filename)

def unique_path(name_pattern):
    """
    path = unique_path(pathlib.Path.cwd(), 'test{:03d}.txt')

    :param directory:
    :param name_pattern:
    :return:
    """

    # path = pathlib.Path(directory)
 #    directory = \
 # \
    counter = 0
    while True:
        counter += 1
        path = pathlib.Path(str(name_pattern).format(counter))
        if not path.exists():
            return path

