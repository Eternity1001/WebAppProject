import re

class Router:
    

    def __init__(self) -> None:
        pass
    
    routeHolder = {}
    
    def add_route(self, httpMethod, path, method):  
        
        path = r'' + path
        info = [path, method]

        if self.routeHolder.get(httpMethod):
            
            listOfInfo = self.routeHolder[httpMethod]
            listOfInfo.append(info)
            return
        self.routeHolder[httpMethod] = [info]
        return 
    
    def route_request(self, request):
        
        if self.routeHolder.get(request.method):
            
            for i in self.routeHolder[request.method]:
                
                if len(i) == 2:
                    if re.match(i[0], request.path):
                        return i[1](request)
        
        return b"HTTP/1.1 404 Not Found \r\nContent-Type: text/plain\r\nContent-Length: 36\r\nX-Content-Type-Options: nosniff \r\n\r\nThe Requested Content Does Not Exist"


# def some(request):
    
#     return request.body
        
# def test():
    
#     router = Router()
#     request = [Request(b'GET /public/functions.js HTTP/1.1\r\nHost: localhost:8080\r\n\r\nfunction.js'),
#                Request(b'GET /public/webrtc.js HTTP/1.1\r\nHost: localhost:8080\r\n\r\nwebrtc.js'),
#                Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\n\r\nindex page'), 
#                Request(b'GET /public/style.css HTTP/1.1\r\nHost: localhost:8080\r\n\r\nstyleseheet'),
#                Request(b'POST /register HTTP/1.1\r\nHost: localhost:8080\r\n\r\nusername_reg=qwersadf+&password_reg=sd+wqrfas%21%40%234+f434'),
#                Request(b'GET /public/functions.js HTTP/1.1\r\nHost: localhost:8080\r\n\r\nfunction.js')
#                ]
    
#     router.add_route("GET", "^/public/functions.js$", some)
#     router.add_route("POST", "^/register$", some)
#     router.add_route("GET", "^/$", some)
#     router.add_route("GET", "^/public/functions.js$", some)
#     router.add_route("GET", "^/public/functions.js$", some)

#     for i in request:
#         print(router.route_request(i))

# test()