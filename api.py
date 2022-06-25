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

def getLoadOut(RSO, headers, region):
    apiURL = f'https://pd.{region}.a.pvp.net/personalization/v2/players/{RSO}/playerloadout'
    data = getAPI(apiURL, headers)
    del data['Subject']
    del data['Version']
    return data

def setLoadOut(RSO, headers, region, data):
    apiURL = f'https://pd.{region}.a.pvp.net/personalization/v2/players/{RSO}/playerloadout'
    data = putAPI(apiURL, headers, data)
    return data

def getRegion(id_token, headers):
    data = {
        "id_token": id_token
    }
    apiURL = 'https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant'
    data = putAPI(apiURL, headers, data)
    jsonData = json.loads(data.text)
    region = jsonData["affinities"]["live"]
    return region