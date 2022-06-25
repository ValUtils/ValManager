from parsing import *
import requests
import json

def getAPI(url, headers):
    rawData = requests.get(url, headers=headers)
    jsonData = json.loads(rawData.text)
    return jsonData

def putAPI(url, headers, data):
    req = requests.put(url, headers=headers, json=data)
    return req

def getPreference(headers):
    apiURL = 'https://playerpreferences.riotgames.com/playerPref/v3/getPreference/Ares.PlayerSettings'
    jsonData = getAPI(apiURL, headers)
    data = toData(jsonData["data"])
    return data

def setPreference(data, headers):
    rawData = {
        "type": "Ares.PlayerSettings",
        "data": toMagic(data)
    }
    apiURL = 'https://playerpreferences.riotgames.com/playerPref/v3/savePreference'
    req = putAPI(apiURL, headers, rawData)
    return req
