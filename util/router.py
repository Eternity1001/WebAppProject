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
        print(self.http, self.path)
        
        
        
        
      
  # Previous attempt but got the same error 
            
# import re

# class Router:
    

#     def __init__(self) -> None:
#         self.routeHolder = {}

    
    
#     def add_route(self, httpMethod, path, method):  
        
#         path = r'' + path
#         info = [path, method]

#         # Convert the path to regex String
#         # it stored in the following format http method like Get then a list of path and functions corresponding to the http method so
#         # {GET: [["/public/index.html", function], ["/public/images/cat.png", sendGeneric]], 
#         # 'DELETE': [["/chat-messages/", deleteMessage]]}


#         if self.routeHolder.get(httpMethod):
            
#             listOfInfo = self.routeHolder[httpMethod]
#             listOfInfo.append(info)
#             self.routeHolder.update({httpMethod: listOfInfo})
#             return
#         self.routeHolder[httpMethod] = [info]
#         return 
    
#     def route_request(self, request):
        
#         # Checks if the http method GET, POST, DELETE etc exist and get the correspond list to those methods 
#         # Loop through the list where i is list containing [path, method]
#         # if regex matches the path, we call function and it always the first function that was added 
        
#         if self.routeHolder.get(request.method):
            
#             for i in self.routeHolder[request.method]:
#                 # len check was to see if auto wont break but it still break for some reason. It not needed but I dont know what break auto lab
#                 if len(i) == 2:
#                     if re.match(i[0], request.path):
#                         return i[1](request)
        
#         return b"HTTP/1.1 404 Not Found \r\nContent-Type: text/plain\r\nContent-Length: 36\r\nX-Content-Type-Options: nosniff \r\n\r\nThe Requested Content Does Not Exist"