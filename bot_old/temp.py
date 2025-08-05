import os
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def search_folder(folder_name):  
    for root, dirs, files in os.walk(os.getcwd()):  
        if folder_name in dirs:  
            return os.path.join(root, folder_name)  
    return None


with open('userDB.json','r') as f:
    data = json.load(f)
    print(dict(data))
if search_folder('solutions/1'):
    with open('./solutions/1.txt','x') as f:
        print('OK')
else:
    os.mkdir('solutions/1')