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
        '''
        Initialize a new user entry
        '''
        pass

    def __repr__(self) -> str:
        '''
        Return string representation of the user entry
        '''
        return '<User %d>' % (self.id)


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
