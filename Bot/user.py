import constants
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class User:
    def __init__(self, uid = None, name = '', table_nick = '', ya_nick = ''):
        self.uid = uid
        self.name = name
        self.table_nick = table_nick
        self.ya_nick = ya_nick
        self.solved_tasks = []
        self.rates = {}
        
    def to_json(self):
        return {
            "uid" : self.uid,
            "name" : self.name,
            "table_nick" : self.table_nick,
            "ya_nick" : self.ya_nick,
            "solved_tasks" : self.solved_tasks,
            "rates" : self.rates
        }
    
    def register(self):
        
        db = json.loads(constants.userdb)
        
        db.dump(self.to_json())
        
f = User()
f.register()