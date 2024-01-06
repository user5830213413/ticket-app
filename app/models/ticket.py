from app.models.db import db
from app.models.user import UserModel

import json
from itertools import chain

class TicketModel(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True)
    ticket_key = db.Column(db.TEXT)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel', backref=db.backref('tickets', lazy='dynamic'))

    def json(self):
        return{
            'id': self.id,
            'ticket_key': self.ticket_key,
            'user_id': self.user_id
        }
    
    @classmethod
    def get_ticket_by_user_id(cls, _user_id):
        """
        получить билеты пользователя по id
        """
        return cls.query.filter_by(user_id=_user_id).first()
    
    @classmethod
    def get_ticket_key_all(cls):
        """
        вывод всех билетов. используя chain.from_iterable проходим по вложенным массивам чтоб обьединить в единный массив
        """
        return list(chain.from_iterable(json.loads(tickets[0])['ticket'] for tickets in cls.query.with_entities(cls.ticket_key).all()))
    
    @classmethod
    def create_ticket(cls, _ticket_key, _user_id):
        """
        создание нового билета или добавление в текущие билеты
        """
        current_ticket = cls.query.filter_by(user_id=_user_id).with_entities(cls.ticket_key).first()
        
        if current_ticket is not None:
            current_ticket_json = json.loads(current_ticket[0])['ticket']
            current_ticket_json.append(_ticket_key)
            cls.query.filter_by(user_id=_user_id).update({'ticket_key': json.dumps({'ticket': current_ticket_json})})
            db.session.commit()
            return True
        else:
            user = UserModel.get_user_by_id(_user_id)
            new_ticket = json.dumps({'ticket': [_ticket_key]})
            new_ticket_save_db = cls(ticket_key=new_ticket, user_id=user.id, user=user)
            new_ticket_save_db.save_db()
            return False
        
    @classmethod
    def ticket_for_win(cls, _ticket_key):
        """
        определяет победителя
        """
        all_tickets = cls.query.all()
        results = {}

        for ticket in all_tickets:
            if _ticket_key in json.loads(ticket.ticket_key)['ticket']:
                results[str(ticket.user_id)] = _ticket_key
                break
        return results
        
    def save_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_db(self):
        db.session.delete(self)
        db.session.commit()