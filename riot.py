import re
import ssl
import requests
from typing import Any
from parsing import encodeJSON
from collections import OrderedDict
from requests.adapters import HTTPAdapter

platform = {
	"platformType": "PC",
	"platformOS": "Windows",
	"platformOSVersion": "10.0.19042.1.256.64bit",
	"platformChipset": "Unknown"
}

FORCED_CIPHERS = [
    'ECDHE-ECDSA-AES128-GCM-SHA256',
    'ECDHE-ECDSA-CHACHA20-POLY1305',
    'ECDHE-RSA-AES128-GCM-SHA256',
    'ECDHE-RSA-CHACHA20-POLY1305',
    'ECDHE+AES128',
    'RSA+AES128',
    'ECDHE+AES256',
    'RSA+AES256',
    'ECDHE+3DES',
    'RSA+3DES'
]

userAgent = "RiotClient/51.0.0.4429735.4429735 rso-auth (Windows;10;;Professional, x64)"

def getToken(uri):
    pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    data = pattern.findall(uri)[0]
    access_token = data[0]
    id_token = data[1]
    return [access_token, id_token]

def post(session, access_token, url):
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Authorization': f'Bearer {access_token}',
    }
    r = session.post(url, headers=headers, json={})
    return r.json()

def authenticate(username, password):
    class SSLAdapter(HTTPAdapter):
        def init_poolmanager(self, *args: Any, **kwargs: Any) -> None:
            ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            ctx.set_ciphers(':'.join(FORCED_CIPHERS))
            kwargs['ssl_context'] = ctx
            return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

    session = requests.session()
    session.headers = OrderedDict({
        "User-Agent": userAgent,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "application/json, text/plain, */*"
    })
    session.mount('https://', SSLAdapter())

    setupAuth(session)

    access_token, id_token = getAuthToken(session, username, password)

    entitlements_token = getEntitlement(session, access_token)

    user_id = getUserInfo(session, access_token)

    session.close()

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': userAgent,
        'Authorization': f'Bearer {access_token}',
        'X-Riot-Entitlements-JWT': entitlements_token
    }

    return [headers, user_id, id_token]

def setupAuth(session):
    data = {
        'client_id': 'play-valorant-web-prod',
        'nonce': '1',
        'redirect_uri': 'https://playvalorant.com/opt_in',
        'response_type': 'token id_token',
        'scope': 'account openid',
    }

    session.post(f'https://auth.riotgames.com/api/v1/authorization', json=data)

def getAuthToken(session, username, password):
    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }

    r = session.put(f'https://auth.riotgames.com/api/v1/authorization', json=data)
    data = r.json()
    if ("error" in data):
        raise BaseException(data['error'])
    uri = data['response']['parameters']['uri']
    access_token, id_token = getToken(uri)
    return [access_token, id_token]

def getEntitlement(session, access_token):
    data = post(session, access_token, "https://entitlements.auth.riotgames.com/api/token/v1")
    return data['entitlements_token']

def getUserInfo(session, access_token):
    data = post(session, access_token, "https://auth.riotgames.com/userinfo")
    return data['sub']

def getVersion():
    data = requests.get('https://valorant-api.com/v1/version')
    data = data.json()['data']
    return data["riotClientVersion"]

def setHeaders(headers):
    headers['X-Riot-ClientPlatform'] = encodeJSON(platform)
    headers['X-Riot-ClientVersion'] = getVersion()

def getHeaders(username, password):
    headers = authenticate(username, password)[0]
    setHeaders(headers)
    return headers

def getAuth(username, password):
    auth = authenticate(username, password)
    setHeaders(auth[0])
    return auth