'''
User database entry model
'''

from typing import List

from backend.models.db import db


class UserModel(db.Model):
    '''
    Define user database table
    '''
    __tablename__ = 'user_table'

    id = db.Column('id', db.Integer, primary_key=True)
    # todo: other user data like username, password hash, etc.

    children = db.relationship('LeaveModel')

    def __init__(self) -> None:
        '''
        Initialize a new user entry
        '''
        pass

    def __repr__(self) -> str:
        '''
        Return string representation of the user entry
        '''
        return '<User %d>' % (self.id)

    
    @classmethod
    def get_all(cls) -> List['UserModel']:
        '''
        Get all user entries from the database
        '''
        return cls.query.all()


    @classmethod
    def delete_all(cls) -> int:
        '''
        Delete all user entries from the database
        '''
        deleted = cls.query.delete()
        db.session.commit()
        return deleted


    @classmethod
    def get_user(cls, id: int) -> 'UserModel':
        '''
        Get user from the database
        '''
        return cls.query.filter(cls.id == id).first()


    def add(self) -> None:
        '''
        Add new user to the database
        '''
        db.session.add(self)
        db.session.commit()


    def delete(self) -> None:
        '''
        Delete user from the database
        '''
        db.session.delete(self)
        db.session.commit()


    def update(self) -> None:
        '''
        Update user in the database
        '''
        # fixme: db.session.update(self)
        db.session.commit()
