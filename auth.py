from getpass import getpass as inputPass
from .riot import authenticate
from .password import EncryptedDB

db: EncryptedDB

def reAuth():
	print(f"Wrong username or password, type username and password to retry!")
	username = input("User: ")
	password = inputPass("Password: ")
	db.saveUser(username, password)
	return getAuth(username, password)

def getAuth(username, password):
	try:
		return authenticate(username, password)
	except BaseException as err:
		if (err.args[0] == "auth_failure"):
			return reAuth()

def getUsers():
	return db.getUsers()

def getPass(user):
	password = db.getPasswd(user)
	if not password:
		password = inputPass("Password: ")
	return password

def newUser(user, password):
	return db.saveUser(user, password)

def getValidPass():
	dbPassword = inputPass("Local password: ")
	if (not dbPassword):
		return getValidPass()
	return dbPassword

def init():
	global db
	dbPassword = getValidPass()
	db = EncryptedDB(dbPassword)

init()