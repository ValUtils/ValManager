from ValVault import get_auth, Auth, User

from .storage import *
from .api import *

def config(action, user: User, cfg):
	auth: Auth = get_auth(user)
	if (action == "dump"):
		saveToFile(cfg, auth)
	elif (action == "import"):
		saveToFile(f'{user.username}.bck.json', auth)
		importFromFile(cfg, auth)
	elif (action == "restore"):
		importFromFile(f'{user.username}.bck.json', auth)
	elif (action == "backup"):
		saveToFile(f'{user.username}.bck.json', auth)

def configWrite(data,file):
	jsonWrite(data, settingsPath / "configs" / file)

def configRead(file):
	return jsonRead(settingsPath / "configs" / file)

def configList():
	files = listDir(settingsPath / "configs")
	files.sort(key=lambda f: "bck.json" in f)
	return files

def importFromFile(cfg, auth):
	data = configRead(cfg)
	req = setPreference(auth, data)
	print(f'Config status code: {req.status_code}')

def saveToFile(cfg, auth):
	data = getPreference(auth)
	configWrite(data, cfg)
