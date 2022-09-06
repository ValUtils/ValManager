from pathlib import Path
from os import getenv
import platform
import json

def saveToDrive(data, file):
    f = open(file, "w")
    f.write(data)
    f.close()

def readFromDrive(file):
    f = open(file, "r")
    data = f.read()
    f.close()
    return data

def jsonWrite(data, file):
    jsonData = json.dumps(data,indent=4)
    saveToDrive(jsonData, file)

def jsonRead(file):
    rawData = readFromDrive(file)
    data = json.loads(rawData)
    return data

def configWrite(data,file):
    jsonWrite(data, settingsPath / "configs" / file)

def configRead(file):
    return jsonRead(settingsPath / "configs" / file)

def configList():
    files = listDir(settingsPath / "configs")
    files.sort(key=lambda f: "bck.json" in f)
    return files

def loadWrite(data, file, sub):
    createPath(settingsPath / "loadouts" / sub)
    jsonWrite(data, settingsPath / "loadouts" / sub / file)

def loadRead(file, sub):
    return jsonRead(settingsPath / "loadouts" / sub / file)

def loadList(sub):
    return listDir(settingsPath / "loadouts" / sub)

def listDir(dir: Path):
    createPath(dir)
    files = [f.name for f in dir.iterdir() if f.is_file()]
    return files

def createPath(path: Path):
    if(path.is_dir()):
        return
    path.mkdir()

def setPath():
    global settingsPath
    if (platform.system() == "Windows"):
        appdata = Path(getenv('APPDATA'))
        settingsPath = appdata / "ValConfig"
        createPath(settingsPath)
    if (settingsPath):
        folders = ["configs", "loadouts"]
        for f in folders:
            createPath(settingsPath / f)

setPath()