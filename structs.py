from dataclasses import dataclass
from ValVault import Auth

@dataclass
class AuthLoadout(Auth):
	username:str
	region: str
	auth: Auth
