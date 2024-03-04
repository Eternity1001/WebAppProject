
def extract_credentials(request):
    conversion = {'!': '%21' ,'@':'%40', '#':'%23', '$':'%24', '^':'%5E', '&':'%26', '(':'%28', ')':'%29', '-':'%2D', '_':'%5F', '=':'%3D', '%':'%25' }

    methodStr = {'/registration': ["username_reg=","&password_reg="],
                 '/login': ["username_login=", '&password_login=']
                 }
    
    body = request.body.decode().split(f"{methodStr[request.path][0]}", 1)[1]
    body = body.split(f"{methodStr[request.path][1]}", 1)     
    
    encodedPassword:str = body[1]
    
    for i in conversion:
        encodedPassword = encodedPassword.replace(conversion[i], i)
    
        
    usernameAndPassword = [body[0].lstrip(' ').rstrip(" "), encodedPassword.lstrip(" ".rstrip(" "))] 
    return usernameAndPassword


def validate_password(password:str):
    
    charDict = {'a': 'Lowercase', 'b': 'Lowercase', 'c': 'Lowercase', 'd': 'Lowercase', 'e': 'Lowercase', 'f': 'Lowercase', 'g': 'Lowercase', 'h': 'Lowercase', 'i': 'Lowercase', 'j': 'Lowercase', 'k': 'Lowercase', 'l': 'Lowercase', 'm': 'Lowercase', 'n': 'Lowercase', 'o': 'Lowercase', 'p': 'Lowercase', 'q': 'Lowercase', 'r': 'Lowercase', 's': 'Lowercase', 't': 'Lowercase', 'u': 'Lowercase', 'v': 'Lowercase', 'w': 'Lowercase', 'x': 'Lowercase', 'y': 'Lowercase', 'z': 'Lowercase', 'A': 'Uppercase', 'B': 'Uppercase', 'C': 'Uppercase', 'D': 'Uppercase', 'E': 'Uppercase', 'F': 'Uppercase', 'G': 'Uppercase', 'H': 'Uppercase', 'I': 'Uppercase', 'J': 'Uppercase', 'K': 'Uppercase', 'L': 'Uppercase', 'M': 'Uppercase', 'N': 'Uppercase', 'O': 'Uppercase', 'P': 'Uppercase', 'Q': 'Uppercase', 'R': 'Uppercase', 'S': 'Uppercase', 'T': 'Uppercase', 'U': 'Uppercase', 'V': 'Uppercase', 'W': 'Uppercase', 'X': 'Uppercase', 'Y': 'Uppercase', 'Z': 'Uppercase', '0': 'Numbers', '1': 'Numbers', '2': 'Numbers', '3': 'Numbers', '4': 'Numbers', '5': 'Numbers', '6': 'Numbers', '7': 'Numbers', '8': 'Numbers', '9': 'Numbers', '!': 'Special', '@': 'Special', '#': 'Special', '$': 'Special', '%': 'Special', '^': 'Special', '&': 'Special', '(': 'Special', ')': 'Special', '-': 'Special', '_': 'Special', '=': 'Special'}
    
    valid_pass_requirement = {'Lowercase':True, 'Uppercase':True, 'Numbers':True, "Special": True}
    
    passwordCheck = {}
    
    if len(password) < 8:
        return False
     
    for i in password:
        if charDict.get(i):
            passwordCheck.update({charDict[i]: True})
        else: 
            return False
    if sorted(passwordCheck) != sorted(valid_pass_requirement):
        return False
    
    return True

