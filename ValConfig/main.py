from ValVault.terminal import User, init_vault, get_pass

from .loadout import loadout
from .config import config
from .tui import menu


def main():
    init_vault()
    mode, action, username, cfg = menu()
    user = User(username, get_pass(username))
    if mode == "config":
        config(action, user, cfg)
    elif mode == "loadout":
        loadout(action, user, cfg)
