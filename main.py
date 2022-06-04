from pick import pick as pickFunc
from getpass import getpass
from sys import argv
from riot import getHeaders
import requests
import json
import zlib
import base64

def pick(options):
    return pickFunc(options)[0]

def jsonRead(file):
    f = open(file, "r")
    rawData = f.read()
    data = json.loads(rawData)
    f.close()
    return data

def decode( b64string ):
    decoded_data = base64.b64decode( b64string )
    return zlib.decompress( decoded_data , -15)


def encode( string_val ):
    zlibbed_str = zlib.compress( string_val )
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode( compressed_string )

def toData( b64string ):
    inflated_data = decode(b64string)
    return json.loads(inflated_data)

def toMagic( data ):
    stringify = json.dumps(data).encode("utf-8")
    return encode(stringify).decode("utf-8")

def getPreference():
    apiURL = 'https://playerpreferences.riotgames.com/playerPref/v3/getPreference/Ares.PlayerSettings'
    rawData = requests.get(apiURL, headers=headers)
    jsonData = json.loads(rawData.text)
    data = toData(jsonData["data"])
    return data

def setPreference(data):
    rawData = {
        "type": "Ares.PlayerSettings",
        "data": toMagic(data)
    }
    apiURL = 'https://playerpreferences.riotgames.com/playerPref/v3/savePreference'
    req = requests.put(apiURL, headers=headers, json=rawData)
    return req

def dumpToFile(cfg):
    f = open(cfg, "w")
    f.write(json.dumps(getPreference(),indent=4))
    f.close()

def importFromFile(cfg):
    data = jsonRead(cfg)
    req = setPreference(data)
    print(f'Status code: {req.status_code}')

def getUsers():
    users = jsonRead("users.json")
    return list(users.keys())

def getPass(user):
    users = jsonRead("users.json")
    if user in users:
        return users[user]
    return ""

def main():
    action, user, cfg = menu()
    passwd = getPass(user)
    
    if (user == "None" or passwd == ""):
        user = input("User: ")
        passwd = getpass("Password: ")

    global headers
    headers = getHeaders(user, passwd)

    if (action == "dump"):
        dumpToFile(cfg)
    elif (action == "import"):
        dumpToFile(f'{user}.bck.json')
        importFromFile(cfg)
    elif (action == "restore"):
        importFromFile(f'{user}.bck.json')

def menu():
    if (len(argv) == 1):
        return getOptions()
    if (len(argv) == 4):
        s, action, user, cfg = argv
        return [action, user, cfg]


def getOptions():
    action = pick(["dump", "import", "restore"])
    users = getUsers()
    users.append("None")
    user = pick(users)
    if (action == "restore"):
        return [action, user, ""]
    cfg = input("Config file: ")
    return [action, user, cfg]

if __name__ == "__main__":
    main()
