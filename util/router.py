import re

class Router:
    

    def __init__(self) -> None:
        self.routeHolder = {}

    
    
    def add_route(self, httpMethod, path, method):  
        
        path = r'' + path
        info = [path, method]

        # Convert the path to regex String
        # it stored in the following format http method like Get then a list of path and functions corresponding to the http method so
        # {GET: [["/public/index.html", function], ["/public/images/cat.png", sendGeneric]], 
        # 'DELETE': [["/chat-messages/", deleteMessage]]}


        if self.routeHolder.get(httpMethod):
            
            listOfInfo = self.routeHolder[httpMethod]
            listOfInfo.append(info)
            self.routeHolder.update({httpMethod: listOfInfo})
            return
        self.routeHolder[httpMethod] = [info]
        return 
    
    def route_request(self, request):
        
        # Checks if the http method GET, POST, DELETE etc exist and get the correspond list to those methods 
        # Loop through the list where i is list containing [path, method]
        # if regex matches the path, we call function and it always the first function that was added 
        
        if self.routeHolder.get(request.method):
            
            for i in self.routeHolder[request.method]:
                # len check was to see if auto wont break but it still break for some reason. It not needed but I dont know what break auto lab
                if len(i) == 2:
                    if re.match(i[0], request.path):
                        return i[1](request)
        
        return b"HTTP/1.1 404 Not Found \r\nContent-Type: text/plain\r\nContent-Length: 36\r\nX-Content-Type-Options: nosniff \r\n\r\nThe Requested Content Does Not Exist"


# Need the request line like this or auto lab break. THe testing get commented out during submmiting 

# from request import Request


# def testFunction(request):
    
#     response = f"Test Function was called"
#     return response


# def testFunction2(request):
#     response = b"Test Function 2 was called now return Binary"
#     return response
    

# def test1():
#     router = Router()
    
#     routes = [{"method": "GET", 'path':"^/index", 'function': testFunction},
#               {"method": "POST", 'path':"/$", 'function': testFunction},
#               {"method": "PUT", 'path':"^/public/cat.png$", 'function': testFunction},
#               {"method": "DELETE", 'path':"^/index", 'function': testFunction2},
#               {"method": "GET", 'path':"^/index", 'function': testFunction2},
#               {"method": "POST", 'path':"^/chat-message$", 'function': testFunction}]
#     requestRoutes = [Request(b"GET /index HTTP/1.1 200 Ok \r\nContent-Type: text/plain \r\n\r\nThis Request 1"), 
#                      Request(b"POST / HTTP/1.1 200 Ok \r\nContent-Type: text/plain \r\n\r\nThis Request 2"),
#                      Request(b"PUT /public/cat.png HTTP/1.1 200 Ok \r\nContent-Type: text/plain \r\n\r\nThis Request 3"),
#                      Request(b"DELETE /index HTTP/1.1 200 Ok \r\nContent-Type: text/plain \r\n\r\nThis Request 4"),
#                      Request(b"GET /index HTTP/1.1 200 Ok \r\nContent-Type: text/plain \r\n\r\nThis Request 5"),
#                      Request(b"POST /chat-message HTTP/1.1 200 Ok \r\nContent-Type: text/plain \r\n\r\nThis Request 6"),
#                      Request(b"POST /chat-message12 HTTP/1.1 200 Ok \r\nContent-Type: text/plain \r\n\r\nNot Found")
                        
#     ]
#     expectedAnswers = ["Test Function was called", 'Test Function was called', 'Test Function was called', b"Test Function 2 was called now return Binary", 'Test Function was called', 'Test Function was called',  
#                        b"HTTP/1.1 404 Not Found \r\nContent-Type: text/plain\r\nContent-Length: 36\r\nX-Content-Type-Options: nosniff \r\n\r\nThe Requested Content Does Not Exist"
# ]
    
    
#     for i in routes:
        
#         router.add_route(i['method'], i['path'], i['function'])
        
    
#     for i in range(len(requestRoutes)):
        
#         assert router.route_request(requestRoutes[i]) == expectedAnswers[i]
            
# def test2():
    
#     router = Router()
    
#     routes = [{"method": "GET", 'path':"^/public/images/kitten.jpg$", 'function': testFunction2}]
    
#     requestRoutes = [Request(b"GET /public/images/kitten.jpg HTTP/1.1 200 Ok \r\nContent-Type: text/plain \r\n\r\nThis Request 1"), 
#                      Request(b"GET /index HTTP/1.1 200 Ok \r\nContent-Type: text/plain \r\n\r\nThis Request 2")]
    
#     expectedAnswer = [b"Test Function 2 was called now return Binary", 
#                       b"HTTP/1.1 404 Not Found \r\nContent-Type: text/plain\r\nContent-Length: 36\r\nX-Content-Type-Options: nosniff \r\n\r\nThe Requested Content Does Not Exist"]
    
    
#     router.add_route(routes[0]['method'], routes[0]['path'], routes[0]['function'])
    
#     for i in range(len(requestRoutes)):

        
#         assert router.route_request(requestRoutes[i]) == expectedAnswer[i]    
    
    
    
    
    
    
    
    
    
        


def test():
    test1()
    test2()
    
    return

test()