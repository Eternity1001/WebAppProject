from pymongo import MongoClient 
from bcrypt import hashpw, gensalt, checkpw
from util.request import Request
from util.auth import *
import hashlib
from uuid import uuid1

class Register:
    
    lastKnownXREF = ''
       
    def dataBase(self):
        client = MongoClient("mongo")
        db = client["login"]
        collection = db["login"]
        return collection
    

    # Sign Up
    def store(self, request:Request):
        
        loginInfo = extract_credentials(request)
        
        if validate_password(loginInfo[1]):            
            salt = gensalt()
            password = loginInfo[1].encode()
            hashedPassword = hashpw(password, salt)
            collection = self.dataBase()
            collection.insert_one({"user":loginInfo[0], 'password':hashedPassword, 'salt': salt, 'expire':'N/A', 'token': 'N/A', 'x-ref':'N/A' })
            response = f'{request.http_version} 302 Found \r\nContent-Type: text/plain\r\nContent-Length: 28\r\nX-Content-Type-Options: nosniff\r\nLocation: http://localhost:8080\r\n\r\nCorrect username or password'
            response = response.encode()
            return response
        response = f'{request.http_version} 302 Found \r\nContent-Type: text/plain\r\nContent-Length: 30\r\nX-Content-Type-Options: nosniff\r\nLocation: http://localhost:8080\r\n\r\nIncorrect username or password'
        response = response.encode()
        return response
            
            
    def login(self, request):
        
        loginInfo = extract_credentials(request)
        collection = self.dataBase()
        password = loginInfo[1].encode()
        
        for i in collection.find():
        
            if i['user'] == loginInfo[0] and checkpw(password, i['password']):
                token = str(uuid1())
                xrefToken = str(uuid1())
                xref = hashlib.sha256(xrefToken.encode()).hexdigest()
                self.lastKnownXREF = xref
                hashedToken = hashlib.sha512(token.encode()).digest()
                complete = {'user': i['user'], 'password':i['password'], 'salt':i['salt'], 'expire':'False', 'token':hashedToken, 'x-ref':xref}
                collection.delete_one(i)
                collection.insert_one(complete)
                response = f'{request.http_version} 302 Found \r\nContent-Type: text/plain\r\nContent-Length: 28\r\nX-Content-Type-Options: nosniff\r\nSet-Cookie: auth={token}; Max-Age=3600; HttpOnly\r\nLocation: http://localhost:8080\r\n\r\nCorrect username or password'
                response = response.encode()
                return response
            
        response = f'{request.http_version} 302 Found \r\nContent-Type: text/plain\r\nContent-Length: 28\r\nX-Content-Type-Options: nosniff\r\nLocation: http://localhost:8080\r\n\r\ninvalid username or password'
        response = response.encode()
        return response        

    def verifyUser(self, request:Request):
        if request.cookies.get('auth'):
            for i in self.dataBase().find():
                if i['expire'] == 'False' and (i['token']) == (hashlib.sha512(request.cookies['auth'].encode()).digest()):
                    return [True, i]
                
        return [False, {'x-ref':'N/A'}]
    
    def logout(self, request:Request):
        if request.cookies.get("auth"):
            for i in self.dataBase().find():
                if (i['token']) == (hashlib.sha512(request.cookies['auth'].encode()).digest()):
                    newDict = {'user':i['user'], 'password':i['password'], 'salt': i['salt'], 'expire':"True", 'token':request.cookies['auth'], 'x-ref': i['x-ref']}
                    self.dataBase().delete_one(i)
                    self.dataBase().insert_one(newDict)
                    response = f'{request.http_version} 302 Found \r\nContent-Type: text/plain\r\nContent-Length: 10\r\nX-Content-Type-Options: nosniff\r\nLocation: http://localhost:8080\r\n\r\nLogged out'
                    response = response.encode()
                    return response
        response = f'{request.http_version} 302 Found \r\nContent-Type: text/plain\r\nContent-Length: 13\r\nX-Content-Type-Options: nosniff\r\nLocation: http://localhost:8080\r\n\r\nFailed logout'
        response = response.encode()
        return response 