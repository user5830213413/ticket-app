from app.models.db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Float, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }
    
    @classmethod
    def get_user_by_username(cls, username):
        """
        получить пользователя по имени
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_id(cls, _id):
        """
        получить пользователя по id
        """
        return cls.query.filter_by(id=_id).first()
    
    def save_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_db(self):
        db.session.delete(self)
        db.session.commit()