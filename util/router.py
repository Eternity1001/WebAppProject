import re


class Router:

    def __init__(self) -> None:
        self.routeHolder = {}

    def add_route(self, httpMethod, path, method):

        path = r'' + path
        info = [path, method]

        if self.routeHolder.get(httpMethod):
            listOfInfo = self.routeHolder[httpMethod]
            listOfInfo.append(info)
            self.routeHolder.update({httpMethod: listOfInfo})
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
