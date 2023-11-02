from ValVault.terminal import User, get_pass, init_vault

from . import config, loadout
from .tui import menu


def main():
    init_vault()
    mode, action, username, cfg = menu()
    user = User(username, get_pass(username))
    if mode == "config":
        config.action(action, user, cfg)
    elif mode == "loadout":
        loadout.action(action, user, cfg)
