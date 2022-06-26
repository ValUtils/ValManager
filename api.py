from riot import makeHeaders
from parsing import *
import requests
import json

def getAPI(url, auth):
    rawData = requests.get(url, headers=makeHeaders(auth))
    jsonData = json.loads(rawData.text)
    return jsonData

def putAPI(url, auth, data):
    req = requests.put(url, headers=makeHeaders(auth), json=data)
    return req

def getPreference(auth):
    apiURL = 'https://playerpreferences.riotgames.com/playerPref/v3/getPreference/Ares.PlayerSettings'
    jsonData = getAPI(apiURL, auth)
    data = toData(jsonData["data"])
    return data

def setPreference(data, auth):
    rawData = {
        "type": "Ares.PlayerSettings",
        "data": toMagic(data)
    }
    apiURL = 'https://playerpreferences.riotgames.com/playerPref/v3/savePreference'
    req = putAPI(apiURL, auth, rawData)
    return req

def getLoadOut(auth, region):
    apiURL = f'https://pd.{region}.a.pvp.net/personalization/v2/players/{auth["user_id"]}/playerloadout'
    data = getAPI(apiURL, auth)
    del data['Subject']
    del data['Version']
    return data

def setLoadOut(auth, region, data):
    apiURL = f'https://pd.{region}.a.pvp.net/personalization/v2/players/{auth["user_id"]}/playerloadout'
    data = putAPI(apiURL, auth, data)
    return data

def getRegion(auth):
    data = {
        "id_token": auth["id_token"]
    }
    apiURL = 'https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant'
    data = putAPI(apiURL, auth, data)
    jsonData = json.loads(data.text)
    region = jsonData["affinities"]["live"]
    return region