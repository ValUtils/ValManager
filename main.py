from storage import *
from riot import *
from api import *
from pick import pick as pickFunc
from getpass import getpass
from sys import argv

def pick(options):
    return pickFunc(options)[0]

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
    mode, action, user, cfg = menu()
    passwd = getPass(user)
    if (mode == "config"):
        config(action, user, passwd, cfg)
    elif (mode == "loadout"):
        loadout(action, user, passwd, cfg)

def config(action, user, passwd, cfg):
    headers = getHeaders(user, passwd)
    if (action == "dump"):
        configWrite(getPreference(headers), cfg)
    elif (action == "import"):
        configWrite(getPreference(headers), f'{user}.bck.json')
        importFromFile(cfg, headers)
    elif (action == "restore"):
        importFromFile(f'{user}.bck.json', headers)

def loadout(action, user, passwd, cfg):
    passwd = getPass(user)

    [headers, RSO, id_token] = getAuth(user, passwd)
    region = getRegion(id_token,headers)

    if (action == "dump"):
        loadWrite(getLoadOut(RSO, headers, region), cfg, user)
    elif (action == "import"):
        loadWrite(getLoadOut(RSO, headers, region), 'backup.json', user)
        setLoadOut(RSO, headers, region, loadRead(cfg, user))
    elif (action == "restore"):
        setLoadOut(RSO, headers, region, loadRead("backup.json", user))

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
