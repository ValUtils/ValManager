from bidict import bidict
from ValVault import get_users

from .storage import *

def alias_write(data):
	json_write(data, settingsPath / "alias.json")

def alias_read():
	data = json_read(settingsPath / "alias.json")
	biData = bidict(data)
	return biData

def get_alias(alias):
	aliases = alias_read()
	if (alias in aliases):
		return aliases[alias]
	return alias

def get_aliased():
	aliases = alias_read()
	dbUsers = get_users()
	users = []

	for user in dbUsers:
		if (user in aliases.inverse):
			users.append(aliases.inverse[user])
			continue
		users.append(user)

	return users
