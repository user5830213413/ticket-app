from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from app.models.db import db
from app.blacklist import BLACKLIST
from config import Config
from configparser import ConfigParser


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)

jwt = JWTManager(app)

config = ConfigParser()
config.read('config.ini')
admin_id = config.getint('Admin', 'admin_id')

@jwt.additional_claims_loader
def claims_jwt(identity):
    if identity == admin_id:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blocklist_loader
def check_token_in_blacklist(token):
    return token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token():
    return jsonify({'message': 'токен истёк'}), 401


with app.app_context():
    db.create_all()


from app.resources import (
    UserLogin,
    UserRegister,
    UserLogout,
    User,
    TokenRefresh,
    Ticket,
    TicketBuy,
    TicketWin
)

#user
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')

#ticket
api.add_resource(Ticket, '/ticket/<int:user_id>')
api.add_resource(TicketBuy, '/ticket/buy')
api.add_resource(TicketWin, '/ticket/winner')