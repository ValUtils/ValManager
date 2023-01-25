from pick import pick as pickFunc
from getpass import getpass as inputPass
from argparse import ArgumentParser
from ValVault import get_aliases, get_name, new_user

from .loadout import load_list
from .config import config_list


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
    args.config = args.config or choose_config(
        args.mode, args.action, args.user)
    return [args.mode, args.action, args.user, args.config]


def get_user():
    users = get_aliases()
    users.append("New...")
    choice = pick(users)
    if (choice != "New..."):
        return get_name(choice)
    user = input("User: ")
    passwd = inputPass("Password: ")
    new_user(user, passwd)
    return user


def filter_list(array: list[str], string: str):
    filteredList = [s for s in array if string not in s]
    array.clear()
    array.extend(filteredList)


def choose_file(fileList, dump):
    if (dump):
        fileList.append("New...")
        filter_list(fileList, "backup.json")
        filter_list(fileList, ".bck.json")
    choice = pick(fileList)
    if (choice == "New..."):
        return input("Filename: ")
    return choice


def choose_config(mode, action, username):
    if (action not in ["dump", "import"]):
        return
    dump = action == "dump"
    if (mode == "config"):
        return choose_file(config_list(), dump)
    if (mode == "loadout"):
        return choose_file(load_list(username), dump)
