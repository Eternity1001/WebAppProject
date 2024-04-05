import re
from util.request import Request


class Router:

    def __init__(self):
        self.routeHolder = []

    def add_route(self, httpMethod, path, method):

        information = Information(httpMethod, path, method)
        self.routeHolder.append(information)

    def route_request(self, request: Request):

        for i in self.routeHolder:
            if i.compare(request):
                return i.return_function_value(request)

        return b"HTTP/1.1 404 Not Found \r\nContent-Type: text/plain\r\nContent-Length: 36\r\nX-Content-Type-Options: nosniff \r\n\r\nThe Requested Content Does Not Exist"


class Information:

    def __init__(self, http, path, method):

        self.http = http
        self.path = path
        self.method = method

    def compare(self, request: Request):

        regexHttp = re.compile(self.http)
        regexPath = re.compile(self.path)

        if regexHttp.match(request.method):
            if regexPath.match(request.path):
                return True
        return False

    def return_function_value(self, request):
        return self.method(request)

    def print_info(self):
        return (self.http, self.path)