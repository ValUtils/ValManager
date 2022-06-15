import os
import platform
import json

def getFilePath(file):
	return os.path.join(settingsPath, file)

def getCfgPath(file):
	return os.path.join("configs", file)

def saveToDrive(data, file):
	f = open(getFilePath(file), "w")
	f.write(data)
	f.close()

def readFromDrive(file):
	f = open(getFilePath(file), "r")
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
	jsonWrite(data, getCfgPath(file))

def configRead(file):
	return jsonRead(getCfgPath(file))

def configList():
	return listDir("configs")

def listDir(dir):
	directory = getFilePath(dir)
	contents = os.listdir(directory)
	files = []
	for f in contents:
		isFile = os.path.isfile(os.path.join(directory, f))
		if (isFile):
			files.append(f)
	return files

def createPaths(paths):
	for path in paths:
		if(os.path.isdir(path)):
			continue
		os.mkdir(path)

def setPath():
	global settingsPath
	if (platform.system() == "Windows"):
		appdata = os.getenv('APPDATA')
		settingsPath = appdata + "\\ValConfig"
		cfgPath = getFilePath("configs")
		createPaths([settingsPath, cfgPath])

setPath()