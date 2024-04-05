import os
from pymongo import MongoClient
from util.multipart import parse_multipart
from util.request import Request


class FileHandler:

    def __init__(self ):
        pass

    def handle_file(self, request):

        data = parse_multipart(request)


        response = f'{request.http_version} 302 Found \r\nContent-Type: text/plain\r\nContent-Length: 8\r\nX-Content-Type-Options: nosniff\r\nLocation: http://localhost:8080\r\n\r\nUploaded'
        response = response.encode()

        return response

    def data_base(self):
        client = MongoClient("mongo")
        db = client["CSE312"]
        collection = db["CSE312"]

        return collection

    def write_to_file(self, extension, request, content):
        directory_path = "../public/fileUploads"
        uploaded_file_name = ''
        file_names = [f for f in os.listdir(directory_path)]

        if len(file_names) > 0:
            file = file_names[-1].split("_")
            uploaded_file_name = file[0] + str(int(file[1][0:-4]) + 1) + extension

        file_path = os.path.join(directory_path, uploaded_file_name)

        with open(file_path, 'wb') as file:
            file.write(content)


