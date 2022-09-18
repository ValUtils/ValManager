from dataclasses import dataclass
from ValVault import Auth

@dataclass
class AuthLoadout():
	username:str
	region: str
	auth: Auth
