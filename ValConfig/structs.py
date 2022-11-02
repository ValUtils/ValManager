from dataclasses import dataclass
from ValLib import Auth

@dataclass
class AuthLoadout():
	username:str
	region: str
	auth: Auth
