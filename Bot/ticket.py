import json

class Ticket:
    def __init__(self, id, uid, chat_history, status):
        self._id = id
        self._uid = uid 
        self._chat_history = chat_history
        self._status = status

    @property
    def id(self):
        return self._id

    @property
    def uid(self):
        return self._uid
    
    @property
    def chat_history(self):
        return self._chat_history

    @property
    def status(self):
        return str(self._status).decode()
    
    @status.setter
    def status(self, value):
        self._status = str(value).encode()

    def push_question(self, Q: object = {"id":0,"text":"text"}) -> None:
        """
        Appends given question (Q: object) to current ticket's chat history
        """
        if Q['id']=='latest':
            Q['id'] = [obj['id'] for obj in self.chat_history][-1]+1

        self._chat_history[f"Q_{id}"]=str(Q['text']).encode()

        db = json.load(open('tickets.json','r'))

        for obj in db:

            if obj['id']==self.id:
                obj['chat_history'][f'Q_{id}']=self._chat_history[f"Q_{id}"]

        
        json.dump(db, open('tickets.json','w'))


    def push_answer(self, A: object = {"id":0,"text":"text"}) -> None:

        """
        Appends given answer (A: object) to current ticket's chat history
        """
        if A['id']=='latest':
            A['id'] = [obj['id'] for obj in self.chat_history][-1]+1
        
        self._chat_history[f"Q_{id}"]=str(A['text']).encode()

        db = json.load(open('tickets.json','r'))

        for obj in db:

            if obj['id']==self.id:
                obj['chat_history'][f'A_{id}']=self._chat_history[f"A_{id}"]

        
        json.dump(db, open('tickets.json','w'))