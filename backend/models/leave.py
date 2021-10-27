'''
Leave database entry model
'''

from datetime import datetime
from typing import List

from backend.models.db import db
from backend.models.user import UserModel # needed for foreign key relationship


class LeaveModel(db.Model):
    '''
    Define leave database table
    '''
    __tablename__ = 'leave_table'

    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    start_date = db.Column('start_date', db.DateTime, nullable=False)
    end_date = db.Column('end_date', db.DateTime, nullable=False)

    # todo: make id the only primary key with an array of start/end dates
    # leaves = db.Column('leaves', db.ARRAY(db.DateTime, dimensions=2), nullable=False)


    def __init__(self, user_id: int, start_date: datetime, end_date: datetime) -> None:
        '''
        Initialize a new leave entry
        '''
        self.user_id = user_id
        self.start_date = start_date
        self.end_date = end_date
        

    def __repr__(self) -> str:
        '''
        Return string representation of the leave entry
        '''
        dates_str = self.start_date.strftime('%Y-%m-%d') + " - " \
            + self.end_date.strftime('%Y-%m-%d')
        return '<Leave %d, %s>' % (self.user_id, dates_str)


    @classmethod
    def str_to_datetime(cls, date_str: str) -> datetime:
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
    def get_all(cls) -> List['LeaveModel']:
        '''
        Dump database contents to a list of User objects
        '''
        return cls.query.all()


    @classmethod
    def delete_all(cls) -> int:
        '''
        Delete all leaves from the database
        '''
        deleted = cls.query.delete()
        db.session.commit()
        return deleted


    @classmethod
    def get_leave(cls, id: int) -> 'LeaveModel':
        '''
        Get a leave entry from the database
        '''
        return cls.query.get(id)


    def add(self) -> None:
        '''
        Add new leave to the database
        '''
        db.session.add(self)
        db.session.commit()


    def delete(self) -> None:
        '''
        Delete leave from the database
        '''
        db.session.delete(self)
        db.session.commit()


    def update(self) -> None:
        '''
        Update leave in the database
        '''
        # fixme: db.session.update(self)
        db.session.commit()