import re
# from request import Request
from util.request import Request
class Router:
    

    def __init__(self):
        self.routeHolder = []

    def add_route(self, httpMethod, path, method):  
        
        information = Information(httpMethod, path, method)
        self.routeHolder.append(information)
    
    def route_request(self, request:Request):
        
        
        for i in self.routeHolder:
            if i.compare(request):
                return i.returnFunctionValue(request)
            
        return b"HTTP/1.1 404 Not Found \r\nContent-Type: text/plain\r\nContent-Length: 36\r\nX-Content-Type-Options: nosniff \r\n\r\nThe Requested Content Does Not Exist"
            


# I dont know what causing a out of index error. May it because bc my regex is wrong but I dont know what wrong with my regex then

class Information:
    
    def __init__(self, http, path, method):
        
        self.http = http
        self.path = path
        self.method = method
        
    
    def compare(self,request:Request):
        
        regexHttp = re.compile(self.http)
        regexPath = re.compile(self.path)

        if regexHttp.match(request.method):
            if regexPath.match(request.path):
                return True
        return False
    
    def returnFunctionValue(self, request):
        return self.method(request)
    
    def printInfo(self):
        return(self.http, self.path)
        
        
        