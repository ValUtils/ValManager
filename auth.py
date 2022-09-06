from getpass import getpass as inputPass
from riot import authenticate

def reAuth():
    print(f"Wrong username or password, type username and password to retry!")
    username = input("User: ")
    password = inputPass("Password: ")
    return authenticate(username, password)

def getAuth(username, password):
    try:
        return authenticate(username, password)
    except BaseException as err:
        if (err.args[0] == "auth_failure"):
            return reAuth()
