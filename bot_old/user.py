import os
import json
import constants
from typing import *
import functions
import constants
import telebot

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class User:
    def __init__(self, available_nums: list, registered: bool, name: str, nickname: str, uid: str, is_admin: bool = False, yaContestName: str = ''):
        """
        Creates a User object
        """
        self._yaContestName = str(yaContestName).encode()
        self._nickname = str(nickname).encode()
        self._registered = registered
        self._available_nums = available_nums
        self._name = str(name).encode()
        self._uid = str(uid)
        self._solutions = []
        self._sent_nums = []
        self._is_admin = False
        self._bot_starts_count = 0

    @property
    def yaContestName(self):
        return self._yaContestName


    @property
    def name(self):
        return self._name
    
    @property
    def nickname(self):
        return self._nickname
    
    @property
    def uid(self):
        return self._uid

    @property
    def registered(self):
        return self._registered
    
    @property
    def available_nums(self):
        return self._available_nums
    
    @property
    def is_admin(self):
        return self._is_admin
    
    @property
    def bot_starts_count(self):
        return self._bot_starts_count
    
    @name.setter
    def name(self, value):
        self.name = value

    @available_nums.setter
    def available_nums(self, value):
        self._available_nums = value
        
    @yaContestName.setter
    def available_nums(self, value):
        self._yaContestName = value
        
    @nickname.setter
    def available_nums(self, value):
        self._nickname = value


    def register(self): # прописать логику регистрации
        """
        registers user and appends data to DB. Returns response
        """
        self._registered = True

        f = open('userDB.json','r', encoding='utf-8')
        db = json.load(f)
        f.close()

        db = dict(db)

        if not any([self.uid in db['users'][k].values() for k in range(len(db['users']))]): 
            db['users'].append({
                "uid":str(self.uid),
                "name":str(self.name),
                "nickname":str(self.nickname),
                "available_nums":[str(x) for x in self.available_nums],
                "registered":True,
                "is_admin":self.is_admin,
                "yaContestName": str(self.yaContestName),
                "rates":
                    {
                    
                    }
                })
        else:
            return "Авторизация прошла успешно"

        with open('userDB.json','w') as f:
            json.dump(db,f, ensure_ascii=False)
        
        return "Регистрация прошла успешно"

        
    def delete(self) -> str: # прописать логику удаления данных
        """
        deletes user from DB. Returns response
        """
        self._registered = False

        f = open('userDB.json','r', encoding='utf-8')
        db = json.load(f)
        f.close()

        db = dict(db)

        if any([self.uid in db['users'][k].values() for k in range(len(db['users']))]): 
            for x in db['users']:
                if x['uid']==self.uid:
                    db['users'].remove(x)
        else:
            return "Личные данные не найдены"

        with open('userDB.json','w', encoding='utf-8') as f:
            json.dump(db,f)

        return "Личные данные успешно удалены с сервера"


    def send(self, file: IO, number: str, filename: str = None) -> str:
        """
        Send solution of task to server in path solutions/uid/numer.pdf. Returns a respond
        """

        

        if number in self.available_nums:
            self.delete()
            self.available_nums = list(set(self.available_nums) - set(number))
            
            try:
                functions.push(f'solutions/{self.uid}', file, filename)
            except FileExistsError as e:
                self.register()
                return "Вы уже отправили решение этой задачи"
            self.register()
            print(self.available_nums)
            self._sent_nums.append(number)
       
        return "Решение принято"

    def get_rate(self, number: str):
        """
        Получить оценки с сервера
        """
        f = open('TasksDB.json','r', encoding='utf-8')
        tasksDB = dict(json.load(f))
        f.close()

        f = open('userDB.json','r', encoding='utf-8')
        userDB = dict(json.load(f))
        f.close()

        # sum = tasksDB[number]['rates'][number][f'{i}']

        if number in constants.NUM:
            msg = '\n'.join(f'К{i}....(/{tasksDB[number]['criteria'][f'{i}']['max']})' for i in tasksDB[number]["criteria"])
            return f'Ваши баллы по задаче {number} "{tasksDB[number]['name']}":\nSUM....(/{tasksDB[number]['max']})\n'+msg
    

# a = User(['1.1'],False,'a','12')

# respond = a.register()
# print(respond)
# respond = a.send(open('Комплект заданий.pdf','rb'),'1.1', '1.1')
# print(respond)

# respond = a.get_rate('1.1')
# print(respond)