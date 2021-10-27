'''
Leave database entry model
'''

from datetime import datetime, timedelta
from typing import List
from sqlalchemy import and_
from sqlalchemy.sql.expression import nullslast

from backend.models.db import db
from backend.models.user import UserModel # needed for foreign key relationship


MAX_LEAVE = timedelta(weeks=12)
LEAVE_PERIOD = timedelta(days=365) # 1 standard year


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
    # todo: add remaining leave days
    # remaining_leave_days = db.Column('remaining_leave_days', db.Integer, nullable=False)


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
        dates_str = self.start_date.strftime('%Y-%m-%d') + '-' \
            + self.end_date.strftime('%Y-%m-%d')
        return '<Leave %d, %s>' % (self.user_id, dates_str)


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


    @classmethod
    def get_remaining_leave(cls, user_id: int, date: datetime) -> int:
        '''
        Get the number of remaining leave days for a user in the leave
        year preceding the provided date
        '''
        user_leaves = cls.query.filter(
            and_(cls.user_id == user_id, cls.start_date >= date - LEAVE_PERIOD)
        ).all()

        # fixme: track leave remaining so we don't have to recalculate
        days_used = sum([LeaveModel.get_leave_days(leave) for leave in user_leaves])

        return MAX_LEAVE.days - days_used


    @staticmethod
    def get_leave_days(leave: 'LeaveModel') -> int:
        '''
        Return leave days used for given leave
        '''
        return (leave.end_date - leave.start_date).days + 1


    @staticmethod
    def get_leave_too_long(leave: 'LeaveModel') -> bool:
        '''
        Check if leave is too long
        '''
        return (leave.end_date - leave.start_date) > MAX_LEAVE


    @staticmethod
    def str_to_datetime(date_str: str) -> datetime:
        '''
        Converts a an iso formatted date string to a datetime object
        '''
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')


    @staticmethod
    def datetime_to_str(date: datetime) -> str:
        '''
        Converts a datetime object to an iso formatted date string
        '''
        return date.strftime('%Y-%m-%dT%H:%M:%S')


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

    
    def rollback(self) -> None:
        '''
        Rollback changes to leave in the database
        '''
        db.session.rollback()