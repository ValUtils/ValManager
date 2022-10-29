from bidict import bidict
from ValVault import get_users

from .storage import *

def aliasWrite(data):
	jsonWrite(data, settingsPath / "alias.json")

def aliasRead():
	data = jsonRead(settingsPath / "alias.json")
	biData = bidict(data)
	return biData

def getAlias(alias):
	aliases = aliasRead()
	if (alias in aliases):
		return aliases[alias]
	return alias

def getAliased():
	aliases = aliasRead()
	dbUsers = get_users()
	users = []

	for user in dbUsers:
		if (user in aliases.inverse):
			users.append(aliases.inverse[user])
			continue
		users.append(user)

	return users
