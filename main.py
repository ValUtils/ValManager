from storage import *
from parsing import *
from pick import pick as pickFunc
from getpass import getpass
from sys import argv
from riot import getHeaders
import requests
import json

def pick(options):
    return pickFunc(options)[0]

def getPreference(headers):
    apiURL = 'https://playerpreferences.riotgames.com/playerPref/v3/getPreference/Ares.PlayerSettings'
    rawData = requests.get(apiURL, headers=headers)
    jsonData = json.loads(rawData.text)
    data = toData(jsonData["data"])
    return data

def setPreference(data, headers):
    rawData = {
        "type": "Ares.PlayerSettings",
        "data": toMagic(data)
    }
    apiURL = 'https://playerpreferences.riotgames.com/playerPref/v3/savePreference'
    req = requests.put(apiURL, headers=headers, json=rawData)
    return req

def importFromFile(cfg, headers):
    data = configRead(cfg)
    req = setPreference(data, headers)
    print(f'Status code: {req.status_code}')

def getUsers():
    users = jsonRead("users.json")
    return list(users.keys())

def getPass(user):
    users = jsonRead("users.json")
    if user in users:
        return users[user]
    return getpass("Password: ")

def main():
    action, user, cfg = menu()
    passwd = getPass(user)

    headers = getHeaders(user, passwd)

    if (action == "dump"):
        configWrite(getPreference(headers), cfg)
    elif (action == "import"):
        configWrite(getPreference(headers), f'{user}.bck.json')
        importFromFile(cfg, headers)
    elif (action == "restore"):
        importFromFile(f'{user}.bck.json', headers)

def menu():
    if (len(argv) == 1):
        return getOptions()
    if (len(argv) == 4):
        s, action, user, cfg = argv
        return [action, user, cfg]

def getUser():
    users = getUsers()
    users.append("New...")
    choice = pick(users)
    if (choice == "New..."):
        return input("User: ")
    return choice

def getCFG(new):
    configs = configList()
    if (new):
        configs.append("New...")
    choice = pick(configs)
    if (choice == "New..."):
        return input("Config file: ")
    return choice

def getOptions():
    action = pick(["dump", "import", "restore"])
    user = getUser()
    if (action == "restore"):
        return [action, user, ""]
    cfg = getCFG(action == "dump")
    return [action, user, cfg]

if __name__ == "__main__":
    main()
