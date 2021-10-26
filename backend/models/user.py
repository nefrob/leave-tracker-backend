'''
User database entry model
'''

from backend.models.db import db


class User(db.Model):
    '''
    Define user database table
    '''
    __tablename__ = 'user_table'

    id = db.Column('id', db.Integer, primary_key=True)
    # todo: other user data like username, password, etc.

    children = db.relationship('Leave')

    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return '<User %d>' % (self.id)
