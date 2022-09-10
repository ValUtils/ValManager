from storage import *
from pick import pick as pickFunc
from getpass import getpass as inputPass
from loadout import loadout, loadList
from config import config, configList
from auth import getUsers, getPass, newUser
from sys import argv

def pick(options):
    return pickFunc(options)[0]

def main():
    mode, action, user, cfg = menu()
    passwd = getPass(user)
    if (mode == "config"):
        config(action, user, passwd, cfg)
    elif (mode == "loadout"):
        loadout(action, user, passwd, cfg)

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
    if (choice != "New..."):
        return choice
    user = input("User: ")
    passwd = inputPass("Password: ")
    newUser(user, passwd)
    return user

def filterList(array: list[str], string: str):
    filteredList = [s for s in array if string not in s]
    array.clear()
    array.extend(filteredList)

def chooseFile(fileList, dump):
    if (dump):
        fileList.append("New...")
        filterList(fileList, "backup.json")
        filterList(fileList, ".bck.json")
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
