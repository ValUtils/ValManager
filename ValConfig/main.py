from ValVault import init_vault

from .loadout import loadout
from .config import config
from .tui import menu

def main():
	init_vault()
	mode, action, user, cfg = menu()
	if (mode == "config"):
		config(action, user, cfg)
	elif (mode == "loadout"):
		loadout(action, user, cfg)
