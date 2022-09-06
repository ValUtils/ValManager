from storage import *
from api import *
from auth import getAuth

def loadout(action, user, passwd, cfg):
    auth = getAuth(user, passwd)
    region = getRegion(auth)

    if (action == "dump"):
        loadWrite(getLoadOut(auth, region), cfg, user)
    elif (action == "import"):
        loadWrite(getLoadOut(auth, region), 'backup.json', user)
        setLoadOut(auth, region, loadRead(cfg, user))
    elif (action == "restore"):
        setLoadOut(auth, region, loadRead("backup.json", user))

def loadWrite(data, file, sub):
    createPath(settingsPath / "loadouts" / sub)
    jsonWrite(data, settingsPath / "loadouts" / sub / file)

def loadRead(file, sub):
    return jsonRead(settingsPath / "loadouts" / sub / file)

def loadList(sub):
    return listDir(settingsPath / "loadouts" / sub)
