from util.request import Request
import re


class Multipart:

    def __init__(self):
        self.boundary = ''
        self.parts = []


class Part:

    def __init__(self):
        self.headers = {}
        self.name = ''
        self.content = b''


def parse_multipart(request: Request):
    multipart = Multipart()
    multipart.boundary = request.headers.get('Content-Type').split('boundary=')[1]
    rows_of_content = request.body.split(b'--' + multipart.boundary.encode())
    for content in rows_of_content:
        if content == b'--\r\n':
            break
        if len(content) <= 0:
            continue

        parts = Part()
        headers, body = content.split(b'\r\n\r\n', 1)
        parts.content = body[:-2]
        for header in headers.split(b'\r\n'):
            if len(header) <= 0:
                continue
            key, value = header.split(b':')
            parts.headers[key.decode().lstrip(" ").rstrip(" ")] = value.decode().lstrip(" ").rstrip(" ")

            for i in value.decode().split(';'):
                if re.match(' name', i):
                    name = i.split('name=')[-1].lstrip('"').rstrip('"')
                    parts.name = name
                    break
        multipart.parts.append(parts)

    return multipart



