import requests
import json
from ValVault import makeHeaders

from .structs import Auth, AuthLoadout
from .parsing import *

def getAPI(url, auth: Auth):
	r = requests.get(url, headers=makeHeaders(auth))
	jsonData = json.loads(r.text)
	return jsonData

def putAPI(url, auth: Auth, data):
	req = requests.put(url, headers=makeHeaders(auth), json=data)
	return req

def getPreference(auth: Auth):
	apiURL = 'https://playerpreferences.riotgames.com/playerPref/v3/getPreference/Ares.PlayerSettings'
	jsonData = getAPI(apiURL, auth)
	data = toData(jsonData["data"])
	return data

def setPreference(auth: Auth, data):
	rawData = {
		"type": "Ares.PlayerSettings",
		"data": toMagic(data)
	}
	apiURL = 'https://playerpreferences.riotgames.com/playerPref/v3/savePreference'
	req = putAPI(apiURL, auth, rawData)
	return req

def getLoadOut(loadAuth: AuthLoadout):
	auth = loadAuth.auth
	apiURL = f'https://pd.{loadAuth.region}.a.pvp.net/personalization/v2/players/{auth.user_id}/playerloadout'
	data = getAPI(apiURL, auth)
	del data['Subject']
	del data['Version']
	return data

def setLoadOut(loadAuth: AuthLoadout, data):
	auth = loadAuth.auth
	apiURL = f'https://pd.{loadAuth.region}.a.pvp.net/personalization/v2/players/{auth.user_id}/playerloadout'
	data = putAPI(apiURL, auth, data)
	return data

def getRegion(auth: Auth):
	data = {
		"id_token": auth.id_token
	}
	apiURL = 'https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant'
	data = putAPI(apiURL, auth, data)
	jsonData = json.loads(data.text)
	region = jsonData["affinities"]["live"]
	return region