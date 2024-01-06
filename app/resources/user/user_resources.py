from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from app.models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from app.blacklist import BLACKLIST

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str)
user_parser.add_argument('password', type=str)
user_parser.add_argument('balance', type=float)


class UserRegister(Resource):
    def post(self):
        data = user_parser.parse_args()
        
        if UserModel.get_user_by_username(data['username']):
            return {'message': 'пользователь с таким именем уже существует'}, 400
        
        user = UserModel(
            username = data['username'],
            password = generate_password_hash(data['password'], method='scrypt'),
            balance = data['balance']
        )
        user.save_db()

        return {'message': 'успешно зарегистрирован'}, 201

class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()

        user = UserModel.get_user_by_username(data['username'])

        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        
        return {'message': 'ошибка'}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)

        return {'message': 'успешный выход'}, 200

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current = get_jwt_identity()
        new_token = create_access_token(identity=current, fresh=False)
        return {'access_token': new_token}, 200

class User(Resource):
    def get(self, user_id):
        user = UserModel.get_user_by_id(user_id)
        if not user:
            return {'message': 'пользователь не найден!'}, 404
        return user.json(), 200
    
    def delete(self, user_id):
        user = UserModel.get_user_by_id(user_id)
        if not user:
            return {'message': 'пользователь не найден!'}, 404
        user.delete_db()
        return {'message': 'пользователь удален!'}, 200