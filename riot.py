import re
import ssl
import requests
from urllib3 import PoolManager
from collections import OrderedDict
from requests.adapters import HTTPAdapter

client_platform = 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9'

def authenticate(username, password):
    class SSLAdapter(HTTPAdapter):
        def init_poolmanager(self, *args: Any, **kwargs: Any) -> None:
            ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            ctx.set_ciphers("DEFAULT@SECLEVEL=1")
            kwargs['ssl_context'] = ctx
            return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

    headers = OrderedDict({
        'User-Agent': 'RiotClient/48.0.0.4342439.4342439 rso-auth (Windows;10;;Professional, x64)'
    })

    session = requests.session()
    session.mount('https://auth.riotgames.com/api/v1/authorization', SSLAdapter())
    session.headers = headers

    data = {
        'client_id': 'play-valorant-web-prod',
        'nonce': '1',
        'redirect_uri': 'https://playvalorant.com/opt_in',
        'response_type': 'token id_token',
    }
    r = session.post(f'https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)

    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }
    r = session.put(f'https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)
    pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    data = pattern.findall(r.json()['response']['parameters']['uri'])[0]
    access_token = data[0]

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': "entitlements.auth.riotgames.com",
        'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)',
        'Authorization': f'Bearer {access_token}',
    }
    r = session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={})
    entitlements_token = r.json()['entitlements_token']

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': "auth.riotgames.com",
        'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)',
        'Authorization': f'Bearer {access_token}'
    }

    r = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
    user_id = r.json()['sub']
    headers['X-Riot-Entitlements-JWT'] = entitlements_token
    del headers['Host']
    session.close()
    return headers

def getVersion():
    data = requests.get('https://valorant-api.com/v1/version')
    data = data.json()['data']
    return data["riotClientVersion"]

def getHeaders(username, password):
    headers = authenticate(username, password)
    headers['X-Riot-ClientPlatform'] = client_platform
    headers['X-Riot-ClientVersion'] = getVersion()
    return headers
