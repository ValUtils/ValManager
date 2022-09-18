from pick import pick as pickFunc
from getpass import getpass as inputPass
from sys import argv
from ValVault import (
	init as init_auth,
	getUsers,
	getPass,
	newUser,
	User
)

from .storage import *
from .loadout import loadout, loadList
from .config import config, configList

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
		return getOptions()
	if (len(argv) == 5):
		s, mode, action, username, cfg = argv
		user = User(username, getPass(username))
		return [mode, action, user, cfg]

def getUser():
	users = getUsers()
	users.append("New...")
	choice = pick(users)
	if (choice != "New..."):
		return choice
	user = input("User: ")
	passwd = inputPass("Password: ")
	newUser(user, passwd)
	return user

def filterList(array: list[str], string: str):
	filteredList = [s for s in array if string not in s]
	array.clear()
	array.extend(filteredList)

def chooseFile(fileList, dump):
	if (dump):
		fileList.append("New...")
		filterList(fileList, "backup.json")
		filterList(fileList, ".bck.json")
	choice = pick(fileList)
	if (choice == "New..."):
		return input("Filename: ")
	return choice

def getOptions():
	mode = pick(["config", "loadout"])
	action = pick(["backup", "dump", "import", "restore"])
	username = getUser()
	user = User(username, getPass(username))
	if (action in ["restore", "backup"]):
		return [mode, action, user, ""]
	if (mode == "config"):
		cfg = chooseFile(configList(), action == "dump")
	elif (mode == "loadout"):
		cfg = chooseFile(loadList(username), action == "dump")
	return [mode, action, user, cfg]
