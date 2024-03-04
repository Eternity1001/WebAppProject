class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables
        

        self.method = ""
        self.path = ""
        self.http_version = ""

        # Location Change for those below but not above

        self.body = b""
        self.headers = {}
        self.cookies = {}

        # For All
        splitString = request.split(b"\r\n\r\n", 1)
        strSplitString = splitString[0].decode("UTF-8")
        keyValue = ""
        
        


        # For Body

        self.body = splitString[1]

        # For Method 

        method = strSplitString.split("/", 1)
        method = method[0].strip(" ")        
        self.method = method

        # For Path

        pathString = strSplitString.split("HTTP")
        path = pathString[0].split(f"{self.method}")
        path = path[1].lstrip(" ").rstrip(" ")
        self.path = path

        # For HTTP Versions

        newPath = strSplitString.split(f"{self.path}", 1)
        
        newPath = newPath[1].split("\r\n", 1)
        
        newPath = newPath[0].lstrip(" ").rstrip(" ")        
        self.http_version = newPath
        # For Header

        header = strSplitString.split("\r\n", 1)
        header = header[1].split("\r\n")

                              
                    
        for i in header:                   
            i = i.split(":", 1)
            key = i[0].lstrip(" ").rstrip(" ")
            value = i[1].lstrip(" ").rstrip(" ")
            self.headers[key] = value

        if self.headers.get("Cookie"):
            cookie = self.headers["Cookie"]
            cookie = cookie.split(";")
            for i in cookie:
                i = i.split("=", 1)
                key = i[0].lstrip(" ").rstrip(" ")
                value = i[1].lstrip(" ").rstrip(" ")
                keyValue = keyValue + key + "=" + value + ";"
                self.cookies[key] = value
               
        if self.headers.get("Set-Cookie"):
            cookie = self.headers["Set-Cookie"]
            cookie = self.headers['Set-Cookie'].split("=", 1)
            key = cookie[0].lstrip(" ").rstrip(" ")
            value = cookie[1].lstrip(" ").rstrip(" ")
            self.cookies[key] = value
        

def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str
    print(request.path)

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct


def test2():
    testString = b"POST /public/image HTTP/2.0 \r\n Real: Not \r\n Cookie: Hope=Dead; doctorAppoint=2/15/24; working=Not \r\n Life: Alive:Dead \r\n Pain: True \r\n Set-Cookie: Work=Not \r\n\r\n Yew Ha"
    request = Request(testString)
    
    headerAnswer = {"Real": "Not", "Cookie": "Hope=Dead; doctorAppoint=2/15/24; working=Not", "Life": "Alive:Dead", "Pain" : "True", "Set-Cookie": "Work=Not" }
    cookieAnwer = {"Hope":"Dead","doctorAppoint":"2/15/24","working":"Not", "Work":"Not"}
    
    
    path = "/public/image"
    assert path == request.path
    assert request.http_version == 'HTTP/2.0'
    
    assert request.method == "POST" 
    assert request.body == b" Yew Ha"  
    
    for i in headerAnswer:
        assert i in request.headers
        assert headerAnswer[i] == request.headers[i]
    
    for i in cookieAnwer:
        assert i in cookieAnwer
        assert request.cookies[i] == cookieAnwer[i]   
    
     
def test3():
    testString = b"GET / HTTP/1.2\r\n Hello: World\r\n\r\n YeHaw Holy \r\n Haha"
    rq = Request(testString)

    assert(rq.method == "GET")
    assert(rq.path) == "/"
    assert(rq.http_version) == "HTTP/1.2"
    assert "Hello" in rq.headers
    assert rq.headers["Hello"] == "World"
     

if __name__ == '__main__':
    test1()
    test2()
    test3()
