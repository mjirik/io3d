import os


def remove_if_exists(filename):
    """
    Delete file if exists. Do not panic if the file does not exist.
    """
    if os.path.exists(filename):
        os.remove(filename)

