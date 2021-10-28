'''
Leave database entry model
'''

from datetime import datetime, timedelta
from typing import List
from sqlalchemy import and_, or_, extract

from backend.models.db import db
from backend.models.user import UserModel # needed for foreign key relationship


MAX_YEARLY_LEAVE = timedelta(weeks=12)


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
    def get_leave_remaining(cls, user_id: int, year: int) -> int:
        '''
        Get the number of remaining leave days for a user in the past year

        Assumes a leave can straddle one year boundary for both start/end date
        '''
        leave_year_start = datetime(year, 1, 1)
        leave_year_end = datetime(year, 12, 31)

        user_leaves = cls.query.filter(
            and_(
                cls.user_id == user_id, 
                or_(
                    and_(cls.start_date >= leave_year_start,
                        cls.end_date <= leave_year_end), # in leave year
                    extract('year', cls.end_date) == leave_year_start.year + 1, # starts previous year
                    extract('year', cls.start_date) == leave_year_end.year # ends after year
                )
            )
        ).all()

        print(user_leaves)

        days_used = sum([LeaveModel.get_leave_days_in_year(
            leave.start_date, leave.end_date, year) for leave in user_leaves])

        print('days used:', days_used)
        print('max yearly leave:', MAX_YEARLY_LEAVE.days)

        return MAX_YEARLY_LEAVE.days - days_used


    @classmethod
    def leave_period_valid(cls, leave: 'LeaveModel') -> bool:
        '''
        Check if a leave period does not exceed remaining leave days for the
        date range it spans
        '''
        for year in range(leave.start_date.year, leave.end_date.year + 1):
            remaining_leave_days = cls.get_leave_remaining(leave.user_id, year)
            new_leave_days = cls.get_leave_days_in_year(leave.start_date, leave.end_date, year)
            
            if remaining_leave_days - new_leave_days < 0:
                return False

        return True


    @classmethod
    def get_leave_from(cls, user_id: int, date_from: datetime) -> List['LeaveModel']:
        '''
        Get leave entries for a user starting on a given date moving forward
        '''
        return cls.query.filter(
            and_(
                cls.user_id == user_id,
                or_(
                    cls.start_date >= date_from,
                    cls.end_date >= date_from
                )
            )
        ).order_by(
            cls.start_date
        ).all()


    @staticmethod
    def get_leave_days(leave: 'LeaveModel') -> int:
        '''
        Return leave days used for given leave
        '''
        return (leave.end_date - leave.start_date).days + 1


    @staticmethod
    def get_leave_days_in_year(start_date: datetime, end_date: datetime, year: int) -> int:
        '''
        Return leave days used for given start and end date in given year
        '''
        if not (start_date.year <= year and end_date.year >= year):
            return 0

        if start_date.year < year:
            start_date = datetime(year, 1, 1)

        if end_date.year > year:
            end_date = datetime(year, 12, 31)

        return (end_date - start_date).days + 1


    @staticmethod
    def get_leave_too_long(leave: 'LeaveModel') -> bool:
        '''
        Check if leave is too long
        '''
        return (leave.end_date - leave.start_date) > MAX_YEARLY_LEAVE


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