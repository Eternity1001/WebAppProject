# from router import Router
# from request import Request
from util.request import Request
from util.router import Router



def testFunction(request:Request):
    return b'Good Test and '
    
def testFunction2(request:Request):
    
    return b"I can't fucking pass this class because of stupid dogshit index error that I dont know what causing"


def basicRouterTest():
    
    router = Router()
    
    insertList = [['GET', '^/public/index.html', testFunction], 
                  ['GET', '/public/index', testFunction2],
                  ['GET', '/publicindex.html', testFunction2],
                  ["GET", '/public/index.html$', testFunction2],
                  ['POST', '^/public/function.js$', testFunction],
                  ['POST', '/util/router', testFunction2],
            
                  ]
    
    for i in insertList:
        router.add_route(i[0],i[1],i[2])
        
        
    request = [ Request(b"GET /public/index.html HTTP/2\r\nContent-Type:Plain/html\r\n\r\n Sadge"),
                Request(b"GET /public/index HTTP/2\r\nContent-Type:Plain/html\r\n\r\n Sadge"),
                Request(b"GET /publicindex.html HTTP/2\r\nContent-Type:Plain/html\r\n\r\n Sadge"),
                Request(b"GET /public/index.html$ HTTP/2\r\nContent-Type:Plain/html\r\n\r\n Sadge"),
                Request(b"DELETE /public/index.html HTTP/2\r\nContent-Type:Plain/html\r\n\r\n Sadge"),
                Request(b"POST /public/function.jsjs HTTP/2\r\nContent-Type:Plain/html\r\n\r\n Sadge"),
                Request(b"POST /util/router HTTP/2\r\nContent-Type:Plain/html\r\n\r\n Sadge")
              ]
    
    for i in request:
        
        print(router.route_request(i))
        

        
        
    
        
            
    
    
    
    




def test():
    basicRouterTest()
    
    
test()