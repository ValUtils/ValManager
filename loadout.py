from storage import *
from api import *
from auth import getAuth

def loadout(action, user, passwd, cfg):
    auth = getAuth(user, passwd)
    region = getRegion(auth)

    if (action == "dump"):
        saveToFile(cfg, auth, region, user)
    elif (action == "import"):
        saveToFile("backup.json", auth, region, user)
        importFromFile(cfg, auth, region, user)
    elif (action == "restore"):
        importFromFile("backup.json", auth, region, user)
        setLoadOut(auth, region, loadRead("backup.json", user))

def loadWrite(data, file, sub):
    createPath(settingsPath / "loadouts" / sub)
    jsonWrite(data, settingsPath / "loadouts" / sub / file)

def loadRead(file, sub):
    return jsonRead(settingsPath / "loadouts" / sub / file)

def loadList(sub):
    return listDir(settingsPath / "loadouts" / sub)

def importFromFile(cfg, auth, region, sub):
    data = loadRead(cfg, sub)
    req = setLoadOut(auth, region, data)
    print(f'Status code: {req.status_code}')

def saveToFile(cfg, auth, region, sub):
    data = getLoadOut(auth, region)
    loadWrite(data, cfg, sub)