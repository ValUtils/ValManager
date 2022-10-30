from ValLib import Auth, User
from ValLib.api import *
from ValVault import get_auth

from .storage import *

def config(action, user: User, cfg):
	auth: Auth = get_auth(user)
	if (action == "dump"):
		save_to_file(cfg, auth)
	elif (action == "import"):
		save_to_file(f'{user.username}.bck.json', auth)
		import_from_file(cfg, auth)
	elif (action == "restore"):
		import_from_file(f'{user.username}.bck.json', auth)
	elif (action == "backup"):
		save_to_file(f'{user.username}.bck.json', auth)

def config_write(data,file):
	json_write(data, settingsPath / "configs" / file)

def config_read(file):
	return json_read(settingsPath / "configs" / file)

def config_list():
	files = list_dir(settingsPath / "configs")
	files.sort(key=lambda f: "bck.json" in f)
	return files

def import_from_file(cfg, auth):
	data = config_read(cfg)
	req = set_preference(auth, data)
	print(f'Config status code: {req.status_code}')

def save_to_file(cfg, auth):
	data = get_preference(auth)
	config_write(data, cfg)
