from pick import pick as pickFunc
from getpass import getpass as inputPass
from sys import argv
from ValVault import (
	init as init_auth,
	get_pass,
	new_user,
	User
)

from .storage import *
from .loadout import loadout, load_list
from .config import config, config_list
from .alias import get_aliased, get_alias

def pick(options):
	return pickFunc(options)[0]

def main():
	init_auth()
	mode, action, user, cfg = menu()
	if (mode == "config"):
		config(action, user, cfg)
	elif (mode == "loadout"):
		loadout(action, user, cfg)

def menu():
	if (len(argv) == 1):
		return get_options()
	if (len(argv) == 5):
		s, mode, action, username, cfg = argv
		user = User(username, get_pass(username))
		return [mode, action, user, cfg]

def get_user():
	users = get_aliased()
	users.append("New...")
	choice = pick(users)
	if (choice != "New..."):
		return get_alias(choice)
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

def get_options():
	mode = pick(["config", "loadout"])
	action = pick(["backup", "dump", "import", "restore"])
	username = get_user()
	user = User(username, get_pass(username))
	if (action in ["restore", "backup"]):
		return [mode, action, user, ""]
	if (mode == "config"):
		cfg = choose_file(config_list(), action == "dump")
	elif (mode == "loadout"):
		cfg = choose_file(load_list(username), action == "dump")
	return [mode, action, user, cfg]
