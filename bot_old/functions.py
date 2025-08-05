import os, user
from typing import *
from pathlib import *
import hashlib
import json

User = type

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def search_folder(root_dir: Path, target_name: str) -> list[Path]:
    """
    Searches folder with name {target_name} in dir {root_dir}. Returns true if found, false oterwise
    """
    return len([folder for folder in root_dir.rglob(target_name) if folder.is_dir()])>0

def search_file(root_dir: Path, target_name: str) -> list[Path]:
    """
    Searches folder with name {target_name} in dir {root_dir}. Returns true if found, false oterwise
    """
    return len([file for file in root_dir.rglob(target_name) if file.is_file()])>0

def push(path: str, file: IO, filename: str = None) -> None:
    """
    Pushes {file} to {path}. If there is a filename, file will be pushed with name {filename}
    """

    if search_folder(Path.cwd(),path):
        
        with open(f'{path}/{filename}.pdf','x') as f:
            pass
        with open(f'{path}/{filename}.pdf','wb') as f:
            f.write(file.read())
    else:
        os.mkdir(f'{path}')

def search_user(uid):

    """
    Searches user in DB and returns JSON object of user.
    """

    return [obj for obj in json.load(open('userDB.json','r', encoding='utf-8'))['users'] if obj['uid']==str(uid)][0]

def admins_list():

    """
    Returns list of users' uids if they are admins.
    """

    return [obj['uid'] for obj in json.load(open('userDB.json','r', encoding='utf-8'))['users'] if obj['is_admin']]

def parse(info: str = 'Иванов И.И./0/ivanii/iiicontest') -> tuple:
    """ 
    Parses string to 4 variables. Returns (name, is_admin, nickname, yaContestName, adminKey)
    Dumps user's admin key and sets status 'used' to true if key is valid
    """
    name, adminKey, nickname, yaContestName = info.split('/')
    print(info.split('/'))
    keysDB = json.load(open('keys.json', encoding='utf-8'))
    key_used = any(hashlib.sha256(key.encode('utf-8')) == adminKey for key in keysDB['keys'].keys())

    hashedKeys = []


    for key in keysDB['keys'].keys():
        # print(key)
        hashedKeys.append(hashlib.sha256(key.encode('utf-8')).hexdigest())

    if adminKey in hashedKeys:
        for key in keysDB['keys']:
            if hashlib.sha256(key.encode('utf-8')).hexdigest() == adminKey:
                keysDB['keys'][key]['used'] = True
    else:
        adminKey = '0'

    json.dump(keysDB, open('keys.json','w', encoding='utf-8'))
    return (name, adminKey in hashedKeys and not key_used, nickname, yaContestName, adminKey)

def process_key(adminKey):
    keysDB = json.load(open('keys.json', encoding='utf-8'))
    key_used = any(hashlib.sha256(key.encode('utf-8')) == adminKey for key in keysDB['keys'].keys())

    hashedKeys = []


    for key in keysDB['keys'].keys():
        # print(key)
        hashedKeys.append(hashlib.sha256(key.encode('utf-8')).hexdigest())

    if adminKey in hashedKeys:
        for key in keysDB['keys']:
            if hashlib.sha256(key.encode('utf-8')).hexdigest() == adminKey:
                keysDB['keys'][key]['used'] = True
    else:
        adminKey = '0'

    json.dump(keysDB, open('keys.json','w', encoding='utf-8'))
    return (adminKey in hashedKeys and not key_used, adminKey)

def get_latest_ticket_num()->int:

    """
    Returns latest ticket num in ticket database
    """

    db = json.load(open('tickets.json','r', encoding='utf-8'))
    try:
        return int(db[-1]['id'])
    except:
        return 0
    
def get_ticket_data(id: int, usr: User) -> tuple:
    
    """
    Returns id of ticket (int), uid of user created this ticket (int), chat history (obj) and ticket status (bool)
    """

    db = json.load(open('tickets.json','r', encoding='utf-8'))

    for obj in db:
        if obj['id']==id:
            return tuple(obj.values())
    else:
        return tuple(1,usr.uid,{},'Не задан')