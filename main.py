from storage import *
from riot import *
from api import *
from pick import pick as pickFunc
from getpass import getpass as inputPass
from sys import argv

def pick(options):
    return pickFunc(options)[0]

def importFromFile(cfg, auth):
    data = configRead(cfg)
    req = setPreference(data, auth)
    print(f'Status code: {req.status_code}')

def getAuth(username, password):
    try:
        return authenticate(username, password)
    except BaseException as err:
        print("Auth error, type username and password to retry!")
        username = input("User: ")
        password = inputPass("Password: ")
        return authenticate(username, password)

def getUsers():
    users = jsonRead("users.json")
    return list(users.keys())

def getPass(user):
    users = jsonRead("users.json")
    if user in users:
        return users[user]
    return inputPass("Password: ")

def main():
    mode, action, user, cfg = menu()
    passwd = getPass(user)
    if (mode == "config"):
        config(action, user, passwd, cfg)
    elif (mode == "loadout"):
        loadout(action, user, passwd, cfg)

def config(action, user, passwd, cfg):
    auth = getAuth(user, passwd)
    if (action == "dump"):
        configWrite(getPreference(auth), cfg)
    elif (action == "import"):
        configWrite(getPreference(auth), f'{user}.bck.json')
        importFromFile(cfg, auth)
    elif (action == "restore"):
        importFromFile(f'{user}.bck.json', auth)

def loadout(action, user, passwd, cfg):
    passwd = getPass(user)

    auth = getAuth(user, passwd)
    region = getRegion(auth)

    if (action == "dump"):
        loadWrite(getLoadOut(auth, region), cfg, user)
    elif (action == "import"):
        loadWrite(getLoadOut(auth, region), 'backup.json', user)
        setLoadOut(auth, region, loadRead(cfg, user))
    elif (action == "restore"):
        setLoadOut(auth, region, loadRead("backup.json", user))

def menu():
    if (len(argv) == 1):
        return getOptions()
    if (len(argv) == 5):
        s, mode, action, user, cfg = argv
        return [mode, action, user, cfg]

def getUser():
    users = getUsers()
    users.append("New...")
    choice = pick(users)
    if (choice == "New..."):
        return input("User: ")
    return choice

def chooseFile(fileList, new):
    if (new):
        fileList.append("New...")
    choice = pick(fileList)
    if (choice == "New..."):
        return input("Filename: ")
    return choice

def getOptions():
    mode = pick(["config", "loadout"])
    action = pick(["dump", "import", "restore"])
    user = getUser()
    if (action == "restore"):
        return [mode, action, user, ""]
    if (mode == "config"):
        cfg = chooseFile(configList(), action == "dump")
    elif (mode == "loadout"):
        cfg = chooseFile(loadList(user), action == "dump")
    return [mode, action, user, cfg]

if __name__ == "__main__":
    main()
