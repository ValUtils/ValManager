from ValVault.terminal import User, get_pass, init_vault

from .config import config
from .loadout import loadout
from .tui import menu


def main():
    init_vault()
    mode, action, username, cfg = menu()
    user = User(username, get_pass(username))
    if mode == "config":
        config(action, user, cfg)
    elif mode == "loadout":
        loadout(action, user, cfg)
