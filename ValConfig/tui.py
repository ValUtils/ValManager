from argparse import ArgumentParser
from getpass import getpass as inputPass

from pick import pick as pickFunc

from ValVault.terminal import get_aliases, get_name, new_user

from . import config, loadout
from .backup import backup_list


def pick(options):
    return pickFunc(options)[0]


def menu():
    args = get_args()
    return fill_args(args)


def get_args():
    parser = ArgumentParser(
        "valconfig", description="Save your Valorant configurations and loadouts")
    parser.add_argument("-u", "--user", )
    parser.add_argument("-m", "--mode", choices=["config", "loadout"])
    parser.add_argument(
        "-a", "--action", choices=["dump", "import", "backup", "restore"])
    parser.add_argument("-c", "--config")
    return parser.parse_args()


def fill_args(args):
    args.mode = args.mode or pick(["config", "loadout"])
    args.action = args.action or pick(["backup", "dump", "import", "restore"])
    args.user = args.user or get_user()
    args.config = args.config or pick_data_file(
        args.mode, args.action, args.user)
    return [args.mode, args.action, args.user, args.config]


def get_user():
    users = get_aliases()
    users.append("New...")
    choice = pick(users)
    if choice != "New...":
        return get_name(choice)
    user = input("User: ")
    passwd = inputPass("Password: ")
    new_user(user, passwd)
    return user


def choose_file(fileList, action):
    if action == "dump":
        fileList.append("New...")
    choice = pick(fileList)
    if choice == "New...":
        return input("Filename: ")
    return choice


def pick_config(action, username):
    if action == "restore":
        return pickFunc(backup_list(username))[1]
    return choose_file(config.list(), action)


def pick_data_file(mode, action, username):
    if action not in ["dump", "import", "restore"]:
        return
    if mode == "loadout":
        return choose_file(loadout.list(username), action)
    if mode == "config":
        return pick_config(action, username)
