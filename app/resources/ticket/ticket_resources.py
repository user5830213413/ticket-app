from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

from app.models import UserModel, TicketModel
from random import randint

ticket_parser = reqparse.RequestParser()
ticket_parser.add_argument('ticket_key', type=int)

TICKET_AMOUNT = 20

class TicketBuy(Resource):
    @jwt_required()
    def post(self):
        data = ticket_parser.parse_args()
        current_user_id = get_jwt_identity()
        user = UserModel.get_user_by_id(current_user_id) 

        if not user:
            return {'message': 'пользователь не найден!'}, 404

        if 1 < data['ticket_key'] <= 1000 and user.balance >= TICKET_AMOUNT and data['ticket_key'] not in TicketModel.get_ticket_key_all():
            if TicketModel.create_ticket(data['ticket_key'], user.id):
                user.balance -= TICKET_AMOUNT
                user.save_db()
                return {'message': 'успешно поплнили арсенал билетов'}, 200
            else:
                user.save_db()
                return {'message': 'вы успешно купили билет'}, 200

        return {'message': 'ошибка!!!'}, 402

class TicketWin(Resource):
    @jwt_required()
    def post(self):
        flag = True

        while flag:
            generate_random_ticket = randint(2, 1000)
            win_ticket = TicketModel.ticket_for_win(generate_random_ticket)
            if len(win_ticket) == 1:
                flag = False
            
        return {'user_winner': win_ticket}, 200 

class Ticket(Resource):
    def get(self, user_id):
        user_ticket = TicketModel.get_ticket_by_user_id(user_id)
        
        if not user_ticket:
            return {'message': 'пользователь не найден!'}, 404
        return user_ticket.json()

    def delete(self, user_id):
        user_ticket = TicketModel.get_ticket_by_user_id(user_id)

        if not user_ticket:
            return {'message': 'пользователь не найден!'}, 404
        user_ticket.delete_db()
        return {'message': 'успешно удалены билеты у пользователя!'}, 200