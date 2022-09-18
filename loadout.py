from ValVault import getAuth, User

from .structs import AuthLoadout
from .storage import *
from .api import *

def loadout(action, user: User, cfg):
	auth = getAuth(user)
	region = getRegion(auth)
	loadAuth = AuthLoadout(user.username, region, auth)

	if (action == "dump"):
		saveToFile(cfg, loadAuth)
	elif (action == "import"):
		saveToFile("backup.json", loadAuth)
		importFromFile(cfg, loadAuth)
	elif (action == "restore"):
		importFromFile("backup.json", loadAuth)
		setLoadOut(loadAuth, loadRead("backup.json", user))
	elif (action == "backup"):
		saveToFile("backup.json", loadAuth)

def loadWrite(data, file, sub):
	createPath(settingsPath / "loadouts" / sub)
	jsonWrite(data, settingsPath / "loadouts" / sub / file)

def loadRead(file, sub):
	return jsonRead(settingsPath / "loadouts" / sub / file)

def loadList(sub):
	return listDir(settingsPath / "loadouts" / sub)

def importFromFile(cfg, loadAuth: AuthLoadout):
	data = loadRead(cfg, loadAuth.username)
	req = setLoadOut(loadAuth.auth, loadAuth.region, data)
	print(f'Status code: {req.status_code}')

def saveToFile(cfg, loadAuth: AuthLoadout):
	data = getLoadOut(loadAuth)
	loadWrite(data, cfg, loadAuth.username)