from os import remove
from glob import glob

import core.config

def rm_lock_files(dir_path):
    for f in glob(f"{dir_path}/.~lock*"):
        remove(f)

def clean_up():
    for dir_path in dir(core.config):
        if dir_path[:2] != "__":
            exec(f"rm_lock_files(core.config.{dir_path})")


# TEST
if __name__ == "__main__":
    clean_up()