from ValVault import get_auth, User

from .structs import AuthLoadout
from .storage import *
from .api import *

def loadout(action, user: User, cfg):
	auth = get_auth(user)
	region = get_region(auth)
	loadAuth = AuthLoadout(user.username, region, auth)

	if (action == "dump"):
		save_to_file(cfg, loadAuth)
	elif (action == "import"):
		save_to_file("backup.json", loadAuth)
		import_from_file(cfg, loadAuth)
	elif (action == "restore"):
		import_from_file("backup.json", loadAuth)
		set_load_out(loadAuth, load_read("backup.json", user.username))
	elif (action == "backup"):
		save_to_file("backup.json", loadAuth)

def load_write(data, file, sub):
	create_path(settingsPath / "loadouts" / sub)
	json_write(data, settingsPath / "loadouts" / sub / file)

def load_read(file, sub):
	return json_read(settingsPath / "loadouts" / sub / file)

def load_list(sub):
	return list_dir(settingsPath / "loadouts" / sub)

def import_from_file(cfg, loadAuth: AuthLoadout):
	data = load_read(cfg, loadAuth.username)
	req = set_load_out(loadAuth, data)
	print(f'Loadout status code: {req.status_code}')

def save_to_file(cfg, loadAuth: AuthLoadout):
	data = get_load_out(loadAuth)
	load_write(data, cfg, loadAuth.username)