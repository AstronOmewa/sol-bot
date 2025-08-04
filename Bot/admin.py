from user import *
import json
import hashlib


class Admin(User):
    def __init__(self, available_nums, registered, name, nickname, uid, is_admin = True, activation_key: str = '', yaContestName: str = ''):
        super().__init__(available_nums, registered, name, nickname, uid, is_admin, yaContestName)
        self._is_admin = True
        self._activation_key = activation_key

    @property
    def activation_key(self):
        return self._activation_key

    def create_task(self, number: str, name: str):
        f = open('TasksDB.json','r')
        db = json.load(f)
        f.close()

        db = dict(db)

        if number not in db.keys():
            db[number]={"name":name}
        else:
            return "Этот номер уже есть, вы можете редактировать его критерии"

        with open('TaskDB.json','w') as f:
            json.dump(db,f)

        return "Задача внесена в базу. Добавьте критерии"
    
    def get_criteria(self, number: str):
        f = open('TasksDB.json','r')
        db = json.load(f)
        f.close()

        db = dict(db)

        return(db)

    def set_criteria(self, number: str, max: int, criteria: dict):
        f = open('TasksDB.json','r')
        db = json.load(f)
        f.close()

        db = dict(db)

        if number not in db.keys():
            db[number]={
                "max":max
            }
        
        db[number]["criteria"] = criteria

        with open('TasksDB.json','w') as f:
            json.dump(db,f)


    def rate(self, number: str, user: User, rates: dict):
        f = open('userDB.json','r')
        db = json.load(f)
        f.close()

        db = dict(db)

        for u in db["users"]:
            if u.uid == user.uid:
                u["rates"] = rates

    def register(self):
        """
        registers admin and appends data to DB. Returns response
        """
        self._registered = True

        f = open('userDB.json','r')
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
                "adminKey":str(self.activation_key),
                "is_admin":self.is_admin,
                "yaContestName": self.yaContestName,
                "rates":
                    {
                    
                    }
                })
        else:
            return "Авторизация прошла успешно"

        with open('userDB.json','w') as f:
            json.dump(db,f, ensure_ascii=False)
        
        return "Регистрация прошла успешно"
        
    def delete(self):

        """
        deletes admin from DB. Returns response
        """
        self._registered = False

        f = open('userDB.json','r')
        db = json.load(f)
        f.close()

        db = dict(db)

        if any([self.uid in db['users'][k].values() for k in range(len(db['users']))]): 
            for x in db['users']:
                if x['uid']==self.uid:
                    db['users'].remove(x)
            
            keysFile = open('keys.json','r+')
            obj = dict(json.load(keysFile))
            for key in obj['keys']:
                if key == hashlib.sha256(key.encode('utf-8')):
                    obj['keys'][key]['used'] == False
            keysFile = open('keys.json','w')
            json.dump(obj, keysFile)
        else:
            return "Личные данные не найдены"

        with open('userDB.json','w') as f:
            json.dump(db,f)

        return "Личные данные успешно удалены с сервера"



# a = Admin([],True,'a','1')
# a.set_criteria('1.1', 8, {"1":{"max":1}})