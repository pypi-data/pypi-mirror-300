import os


def createDirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False