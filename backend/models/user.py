'''
User database entry model
'''

from datetime import datetime
from typing import List

from backend.models.db import db


class User(db.Model):
    '''
    Define user leave fields
    '''
    __tablename__ = 'user_table'

    id = db.Column('id', db.Integer, primary_key=True)
    start_date = db.Column('start_date', db.DateTime, primary_key=True)
    end_date = db.Column('end_date', db.DateTime, nullable=False)

    # todo: make id the only primary key with an array of start/end dates
    # leaves = db.Column('leaves', db.ARRAY(db.DateTime, dimensions=2), nullable=False)

    # todo: other user data like username, password, etc.

    def __init__(self, id: int, start_date: datetime, end_date: datetime) -> None:
        '''
        Initialize a new user
        '''
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        

    def __repr__(self) -> str:
        '''
        Return string representation of the user
        '''
        dates_str = self.start_date.strftime('%Y-%m-%d') + " - " \
            + self.end_date.strftime('%Y-%m-%d')
        return '<Employee %d, leave: %s>' % (self.employee_id, dates_str)


    @classmethod
    def str_to_datetime(cls, date_str) -> datetime:
        '''
        Converts a an iso formatted date string to a datetime object
        '''
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')


    @classmethod
    def datetime_to_str(cls, date: datetime) -> str:
        '''
        Converts a datetime object to an iso formatted date string
        '''
        return date.strftime('%Y-%m-%dT%H:%M:%S')


    @classmethod
    def get_all(cls) -> List['User']:
        '''
        Dump database contents to a list of User objects
        '''
        return cls.query.all()


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
