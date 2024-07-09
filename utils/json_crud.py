import json
import os
from .crud import get_users_count

path = os.path.join(os.path.dirname(__file__), 'files', 'users_count.json')
config_path = os.path.join(os.path.dirname(__file__), 'files', 'config.json')


def get_config():
    with open(config_path, "r") as read_file:
        return json.load(read_file)


def file_was_created():
    if os.path.exists(path):
        return True
    else:
        return False


def create_file():
    data = {"count": get_users_count()}
    with open(path, "w") as write_file:
        json.dump(data, write_file)


def get_users_count_from_js():
    if not file_was_created():
        create_file()
    with open(path, "r") as read_file:
        return json.load(read_file)


def update_file():
    if not file_was_created():
        create_file()
        return
    data = {"count": get_users_count()}
    with open(path, "w") as write_file:
        json.dump(data, write_file)


def db_was_modify():
    if not file_was_created():
        create_file()
        return False
    before = get_users_count_from_js()['count']
    after = get_users_count()
    if before != after:
        return True
    else:
        return False
