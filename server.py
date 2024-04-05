import socketserver
from util.router import Router
from util.request import Request
from pymongo import MongoClient
from util.register import Register
from util.file_handle import FileHandler
import json

router = Router()
register = Register()
fileHandler = FileHandler()


class MyTCPHandler(socketserver.BaseRequestHandler):
    a = 1

    def handle(self):
        received_data = self.request.recv(2048)

        print(self.client_address)
        # print("--- received data ---")
        # print(received_data)
        # print("--- end of data ---\n\n")
        request = Request(received_data)

        current_length = len(request.body)
        length = request.headers.get('Content-Length')

        if length:
            while current_length < int(length):
                data_stream = self.request.recv(2048)
                received_data = received_data + data_stream
                current_length = current_length + len(data_stream)
            current_length = 0

        request = Request(received_data)

        if self.a == 1:
            router.add_route("GET", "^/$", self.sendHTML)
            router.add_route("GET", "^/public", self.sendGeneric)
            router.add_route("POST", "^/chat-messages$", self.storeMessage)
            router.add_route("GET", '^/chat-messages/', self.getSingleMessage)
            router.add_route("GET", '^/chat-messages', self.sendMessage)
            router.add_route("DELETE", '^/chat-messages/', self.deleteMessage)
            router.add_route("PUT", '^/chat-messages/', self.updateMessage)
            router.add_route("POST", '^/register', register.store)
            router.add_route("POST", '^/login', register.login)
            router.add_route("POST", '^/logout', register.logout)
            router.add_route("POST", "^/fileUpload", fileHandler.handle_file)
            self.a = 0
        self.request.sendall(router.route_request(request))
        # TODO: Parse the HTTP request and use self.request.sendall(response) to send your response

    def sendHTML(self, request: Request):
        visit = 1
        if request.cookies.get("visits"):
            visit = int(request.cookies["visits"]) + 1
        userStatus = register.verifyUser(request)
        if userStatus[0]:
            with open("/ root/public/index.html") as reader:
                content = reader.read()
                content = content.replace("{{visits}}", f"{visit}")
                content = content.replace("""{{Register: 
        <form action="/register" method="post" enctype="application/x-www-form-urlencoded">
            <label>Username:
                <input id="reg-form-username" type="text" name="username_reg"/>
            </label>
            <br/>
            <label>Password:&nbsp;
                <input id="reg-form-pass" type="password" name="password_reg">
            </label>
            <input type="submit" value="Post">
        </form>

        Login:
        <form action="/login" method="post" enctype="application/x-www-form-urlencoded">
            <label>Username:
                <input id="login-form-username" type="text" name="username_login"/>
            </label>
            <br/>
            <label>Password:&nbsp;
                <input id="login-form-pass" type="password" name="password_login">
            </label>
            <input type="submit" value="Post">
        </form>}}""", ' ')
                content = content.replace("""          
        {{<form action="/logout" method="post" enctype="application/x-www-form-urlencoded"> 
            <button type="submit" value="Post"> LogOut </button>
        </form>}}""", '''<form action="/logout" method="post" enctype="application/x-www-form-urlencoded"> 
            <button type="submit" value="Post"> Logout </button>
        </form>''')
                content = content.replace("""            {{<div id="some" class="hello"> </div>}}
""", f"""            <div id="{userStatus[1]['x-ref']}" class="hello"> </div>
""")
                length = len(content.encode("utf-8"))
                response = f"{request.http_version} 200 OK \r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {length}\r\nX-Content-Type-Options: nosniff \r\nSet-Cookie: visits={visit}; Max-Age=3600\r\n\r\n {content}"
                response = response.encode()
                return response

        else:
            with open("/ root/public/index.html") as reader:
                content = reader.read()
                content = content.replace("{{visits}}", f"{visit}")
                content = content.replace("""          
        {{<form action="/logout" method="post" enctype="application/x-www-form-urlencoded"> 
            <button type="submit" value="Post"> LogOut </button>
        </form>}}""", ' ')
                content = content.replace("""{{Register: 
        <form action="/register" method="post" enctype="application/x-www-form-urlencoded">
            <label>Username:
                <input id="reg-form-username" type="text" name="username_reg"/>
            </label>
            <br/>
            <label>Password:&nbsp;
                <input id="reg-form-pass" type="password" name="password_reg">
            </label>
            <input type="submit" value="Post">
        </form>

        Login:
        <form action="/login" method="post" enctype="application/x-www-form-urlencoded">
            <label>Username:
                <input id="login-form-username" type="text" name="username_login"/>
            </label>
            <br/>
            <label>Password:&nbsp;
                <input id="login-form-pass" type="password" name="password_login">
            </label>
            <input type="submit" value="Post">
        </form>}}""", """Register: 
        <form action="/register" method="post" enctype="application/x-www-form-urlencoded">
            <label>Username:
                <input id="reg-form-username" type="text" name="username_reg"/>
            </label>
            <br/>
            <label>Password:&nbsp;
                <input id="reg-form-pass" type="password" name="password_reg">
            </label>
            <input type="submit" value="Post">
        </form>

        Login:
        <form action="/login" method="post" enctype="application/x-www-form-urlencoded">
            <label>Username:
                <input id="login-form-username" type="text" name="username_login"/>
            </label>
            <br/>
            <label>Password:&nbsp;
                <input id="login-form-pass" type="password" name="password_login">
            </label>
            <input type="submit" value="Post">
        </form>""")
                content = content.replace("""            {{<div id="some" class="hello"> </div>}}
""", f"""            <div id="{register.lastKnownXREF}" class="hello"> </div>""")
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
        highestId = 0
        for i in collection.find():

            id = int(i["id"])

            if highestId <= id:
                highestId = id

        return highestId

    def storeMessage(self, request: Request):

        collection = self.dataBase()
        dictChatInfo = json.loads(request.body)
        message: str = dictChatInfo["message"]

        if len(message) > 0:
            replaceContent = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}
            for i in replaceContent:
                if message.__contains__(i):
                    message = message.replace(i, replaceContent[i])

            dictChatInfo.update({"message": message})

            if request.cookies.get('auth'):

                userStatus = register.verifyUser(request)
                i = userStatus[1]
                if userStatus[0] and dictChatInfo['XSRF'] == i['x-ref']:
                    if i['expire'] == 'False':
                        dictChatInfo.update({"username": i['user']})
                        dictChatInfo["id"] = str(self.getId() + 1)
                        collection.insert_one(dictChatInfo)
                        dictChatInfo.pop("_id")
                        body = json.dumps(dictChatInfo)
                        body = body.encode()
                        response = f"{request.http_version} 201 Created \r\nContent-Type: application/json\r\nX-Content-Type-Options: nosniff\r\nContent-Length: {len(body)}\r\n\r\n"
                        response = response.encode() + body
                        return response

                response = f"{request.http_version} 403 Forbidden\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\nContent-Length: 14\r\n\r\nIncorrect User"
                response = response.encode()
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

    def sendMessage(self, request: Request):
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

    def deleteMessage(self, request: Request):

        collection = self.dataBase()
        id = request.path.split("/")[2]

        if request.cookies['auth']:
            userStatus = register.verifyUser(request)

            if userStatus[0] and userStatus[1]['expire'] == 'False':
                for j in collection.find():
                    if j["id"] == id and j['username'] == userStatus[1]['user']:
                        collection.delete_one(j)
                        response = f"{request.http_version} 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 5\r\nX-Content-Type-Options: nosniff\r\n\r\nfound"
                        response = response.encode()
                        return response
        response = f"{request.http_version} 403 Forbidden\r\nContent-Type: text/plain\r\nContent-Length: 14\r\nX-Content-Type-Options: nosniff\r\n\r\nincorrect user"
        response = response.encode()
        return response

    def updateMessage(self, request: Request):

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
