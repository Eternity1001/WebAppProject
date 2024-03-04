import socketserver
from util.router import Router
from util.request import Request
from pymongo import MongoClient 
import json

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        received_data = self.request.recv(2048)

        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        
        request = Request(received_data)

        router = Router()
        
        a = 1
        if a == 1:
            router.add_route("GET", "^/$", self.sendHTML)
            router.add_route("GET", "^/public", self.sendGeneric)
            router.add_route("POST","^/chat-messages$", self.storeMessage)
            router.add_route("GET", '^/chat-messages/', self.getSingleMessage)
            router.add_route("GET", '^/chat-messages', self.sendMessage)
            router.add_route("DELETE", '^/chat-messages/', self.deleteMessage)
            router.add_route("PUT", '^/chat-messages/', self.updateMessage)
            a = 0
        self.request.sendall(router.route_request(request))
        # TODO: Parse the HTTP request and use self.request.sendall(response) to send your response

    def sendHTML(self, request: Request):
        visit = 1
        if request.cookies.get("visits"):
            visit = int(request.cookies["visits"]) + 1

        with open("/ root/public/index.html") as reader:
            content = reader.read()
            content = content.replace("{{visits}}", f"{visit}")
            length = len(content.encode("utf-8"))
            response = f"{request.http_version} 200 OK \r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {length}\r\nX-Content-Type-Options: nosniff \r\nSet-Cookie: visits={visit}; Max-Age=3600\r\n\r\n {content}"
            response = response.encode()
            return response
            
    def sendGeneric(self, request: Request):

        contentType = {'.css': "text/css", '.js': 'text/javascript', ".jpg": "image/jpeg", ".ico": "image/x-icon"}

        fileType = ''
        for i in contentType:
            if request.path.__contains__(i):
                fileType = contentType[i]

        with open(f"/ root{request.path}", 'rb') as reader:
            content = reader.read()
            length = len(content)
            response = f"{request.http_version} 200 OK\r\nContent-Type: {fileType}\r\nContent-Length: {length}\r\nX-Content-Type-Options: nosniff\r\n\r\n"
            response = response.encode() + content
            
            return response

    def dataBase(self):
        client = MongoClient("mongo")
        db = client["CSE312"]
        collection = db["CSE312"]
        
        return collection
    
    def getId(self):
        
        collection = self.dataBase()        
        highestId =   0      
        for i in collection.find():
            
            id = int(i["id"])
            
            if highestId <= id:
                highestId = id

        return highestId
               
    def storeMessage(self, request:Request):      
               
        collection = self.dataBase()
        dictChatInfo = json.loads(request.body)
        message: str = dictChatInfo["message"]
                                  
        if len(message) > 0:    
            replaceContent = {"&": "&amp;", "<":"&lt;", ">":"&gt;"}       
            for i in replaceContent:
                if message.__contains__(i):
                    message = message.replace(i, replaceContent[i])
                            
            dictChatInfo.update({"message": message})   
            
            if dictChatInfo.get("username") and dictChatInfo.get("id"):
                collection.insert_one(dictChatInfo)
                dictChatInfo.pop("_id")
                body = json.dumps(dictChatInfo)
                body = body.encode()
                response = f"{request.http_version} 201 Created \r\nContent-Type: application/json\r\nX-Content-Type-Options: nosniff\r\nContent-Length: {len(body)}\r\n\r\n"
                response = response.encode() + body
                return response

            dictChatInfo["username"] = "Guest"
            dictChatInfo["id"] = str(self.getId() + 1)
            collection.insert_one(dictChatInfo)      
            dictChatInfo.pop("_id")
            
            body = json.dumps(dictChatInfo)
            body = body.encode()
            response = f"{request.http_version} 201 Created \r\nContent-Type: application/json\r\nX-Content-Type-Options: nosniff\r\nContent-Length: {len(body)}\r\n\r\n"
            response = response.encode() + body
            return response

    def sendMessage(self, request:Request):
        collection = self.dataBase()
        
        allMessages = []
        for i in collection.find():
            i.pop("_id")
            allMessages.append(i)
            
        
        preparedMessages = json.dumps(allMessages)
        preparedMessages = preparedMessages.encode()
        response = f"{request.http_version} 200 OK \r\nContent-Type: application/json\r\nContent-Length:{len(preparedMessages)} \r\nX-Content-Type-Options: nosniff\r\n\r\n"
        response = response.encode() + preparedMessages    
        return response   

    
    def getSingleMessage(self, request: Request):
        
        messageId = request.path.split("/")
        messageId = messageId[2]
        collection = self.dataBase()
        message = ''
        
        for i in collection.find():
            if i["id"] == messageId:
                i.pop("_id")
                message = i
        if len(message) > 0: 
            message = json.dumps(message)
            message = message.encode()
            response = f"{request.http_version} 200 OK \r\nContent-Type: application/json\r\nContent-Length:{len(message)} \r\nX-Content-Type-Options: nosniff\r\n\r\n"
            response = response.encode() + message
            return response
  
            
        response = b"HTTP/1.1 404 Not Found \r\nContent-Type: text/plain\r\nContent-Length: 36\r\nX-Content-Type-Options: nosniff \r\n\r\nThe Requested Content Does Not Exist"
        return response
        
    def deleteMessage(self, request:Request):
        
        collection = self.dataBase()
        id = request.path.split("/")[2]
        for i in collection.find():
            if i["id"] == id:
                collection.delete_one(i)
                response = f"{request.http_version} 204 No Content\r\nContent-Type: text/plain\r\nContent-Length: 0\r\nX-Content-Type-Options: nosniff\r\n\r\n"
                response = response.encode()
                return response


        response = b"HTTP/1.1 404 Not Found \r\nContent-Type: text/plain\r\nContent-Length: 36\r\nX-Content-Type-Options: nosniff \r\n\r\nThe Requested Content Does Not Exist"
        return response
                
    def updateMessage(self, request:Request):
        
        collection = self.dataBase()
        id = request.path.split("/")[2]
        info = json.loads(request.body)
        
        for i in collection.find():
            if i["id"] == id:
                collection.delete_one(i)
                info["id"] = id
                collection.insert_one(info)
                info.pop("_id")
                info = json.dumps(info)
                info = info.encode()
                response = f"{request.http_version} 200 OK \r\nContent-Type: application/json\r\nContent-Length: {len(info)}\r\nX-Content-Type-Options: nosniff\r\n\r\n"
                response = response.encode() + info
                return response
 
 
        response = b"HTTP/1.1 404 Not Found \r\nContent-Type: text/plain\r\nContent-Length: 36\r\nX-Content-Type-Options: nosniff \r\n\r\nThe Requested Content Does Not Exist"
        return response
        
                



        
def main():
    
    host = "0.0.0.0"
    port = 8080

    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))

    server.serve_forever()


if __name__ == "__main__":
    main()
