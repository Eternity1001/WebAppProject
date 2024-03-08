from pymongo import MongoClient 
from bcrypt import hashpw, gensalt, checkpw
from util.request import Request
from util.auth import *
from uuid import uuid1

class Register:
       
    def dataBase(self):
        client = MongoClient("mongo")
        db = client["login"]
        collection = db["login"]
        return collection
    
    # Database need to stroe {user: name, password: Hased password, salt: salt, token:token, expire:true or false, xref token}
    
    def store(self, request:Request):
        
        loginInfo = extract_credentials(request)
        
        if validate_password(loginInfo[1]):            
            salt = gensalt()
            password = loginInfo[1].encode()
            hashedPassword = hashpw(password, salt)
            collection = self.dataBase()
            collection.insert_one({"user":loginInfo[0], 'password':hashedPassword, 'salt': salt, 'expire':'N/A', 'token': 'N/A', 'x-ref':'N/A' })
            response = f'{request.http_version} 302 Found \r\nContent-Type: text/plain\r\nContent-Length: 28\r\nX-Content-Type-Options: nosniff\r\nLocation: http://localhost:8080\r\n\r\Coorect username or password'
            response = response.encode()
            return response
            
            
    def login(self, request):
        
        loginInfo = extract_credentials(request)
        collection = self.dataBase()

        password = loginInfo[1].encode()
        
        for i in collection.find():
            
            if i['user'] == loginInfo[0] and checkpw(password, i['salt']):
                
                salt = gensalt()
                token = uuid1().bytes
                hashedToken = hashpw(token, salt)
                collection.update_one({'user':i['user'], 'password':i['password']}, {'token':hashedToken, 'expire':False})
        self.readDataBase()
    def readDataBase(self):
        
        database = self.dataBase()
        
        for i in database.find():
            print(i)  
            
                
                
                
                
            
        
        
        
            

            
                        
