from storage import *
from api import *
from auth import getAuth

def config(action, user, passwd, cfg):
    auth = getAuth(user, passwd)
    if (action == "dump"):
        configWrite(getPreference(auth), cfg)
    elif (action == "import"):
        configWrite(getPreference(auth), f'{user}.bck.json')
        importFromFile(cfg, auth)
    elif (action == "restore"):
        importFromFile(f'{user}.bck.json', auth)

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
    print(f'Status code: {req.status_code}')
