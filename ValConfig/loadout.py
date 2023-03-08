from ValVault import get_auth, User
from ValLib.api import get_region, get_load_out, set_load_out
from ValLib.structs import ExtraAuth

from .storage import *


def loadout(action, user: User, cfg):
    auth = get_auth(user)
    region = get_region(auth)
    loadAuth = ExtraAuth(user.username, region, auth)

    if (action == "dump"):
        save_to_file(cfg, loadAuth)
    elif (action == "import"):
        backup(loadAuth)
        import_from_file(cfg, loadAuth)
    elif (action == "restore"):
        restore(loadAuth)
    elif (action == "backup"):
        backup(loadAuth)


def load_write(data, file, sub):
    create_path(settingsPath / "loadouts" / sub)
    json_write(data, settingsPath / "loadouts" / sub / file)


def load_read(file, sub):
    return json_read(settingsPath / "loadouts" / sub / file)


def load_list(sub):
    return list_dir(settingsPath / "loadouts" / sub)


def import_from_file(cfg, loadAuth: ExtraAuth):
    data = load_read(cfg, loadAuth.username)
    req = set_load_out(loadAuth, data)
    print(f'Loadout status code: {req.status_code}')


def save_to_file(cfg, loadAuth: ExtraAuth):
    data = get_load_out(loadAuth)
    load_write(data, cfg, loadAuth.username)


def backup_file(loadAuth: ExtraAuth):
    file_name = f"{loadAuth.username}.json"
    backup_folder = settingsPath / "backup" / "_loadouts"
    return backup_folder / file_name


def backup(loadAuth: ExtraAuth):
    data = get_load_out(loadAuth)
    backup_path = backup_file(loadAuth)
    json_write(data, backup_path)


def restore(loadAuth: ExtraAuth):
    backup_path = backup_file(loadAuth)
    data = json_read(backup_path)
    set_load_out(loadAuth, data)
