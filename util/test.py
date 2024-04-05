# import os
#
# directory_path = "../public/fileUploads"
# filename = "file_111.txt"
# file_path = os.path.join(directory_path, filename)
# #
# #
# # with open(file_path, "wb") as file:
# #     file.write(b"Hello, this is my file content.")
#
# directory_path = "../public/fileUploads"
# file_names = [f for f in os.listdir(directory_path)]
#
# if len(file_names) > 0:
#     file = file_names[-1].split("_")
#     newFile = file[0] + str(int(file[1][0:-4]) + 1) + file[1][-4:]
#     print(newFile)