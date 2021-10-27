'''
Api endpoints for leave management
'''

from flask import request
from flask_restful import Resource

from backend.models.leave import LeaveModel
from backend.schemas.leave import LeaveSchema


leave_schema = LeaveSchema()
leave_list_schema = LeaveSchema(many=True)


def update_leave(leave, json_data):
    '''
    Update a leave entry
    '''
    new_start = leave.start_date
    new_end = leave.end_date

    if 'start_date' in json_data:
        new_start = LeaveModel.str_to_datetime(json_data['start_date'])
    if 'end_date' in json_data:
        new_end = LeaveModel.str_to_datetime(json_data['end_date'])
    
    if new_start > new_end:
        return {'message': 'Invalid leave range'}, 400

    old_leave_days =  LeaveModel.get_leave_days(leave)

    leave.start_date = new_start
    leave.end_date = new_end

    new_leave_days =  LeaveModel.get_leave_days(leave)

    remaining_leave = LeaveModel.get_remaining_leave(
        leave.user_id, leave.start_date)

    if new_leave_days - old_leave_days > remaining_leave:
        leave.rollback()
        return {'message': 'Not enough leave days'}, 400

    leave.update()

    return leave_schema.dump(leave), 200


def create_leave(json_data):
    '''
    Create a new leave entry
    '''
    data = leave_schema.load(json_data)
    if (not 'user_id' in data
        or not 'start_date' in data
        or not 'end_date' in data):
        return {'message': 'Missing leave data'}, 400

    data['start_date'] = LeaveModel.str_to_datetime(data['start_date'])
    data['end_date'] = LeaveModel.str_to_datetime(data['end_date'])

    if data['start_date'] > data['end_date']:
        return {'message': 'Invalid leave range'}, 400
    
    leave = LeaveModel(**data)

    remaining_leave = LeaveModel.get_remaining_leave(
        data['user_id'], data['start_date'])
    new_leave_days =  LeaveModel.get_leave_days(leave)

    if new_leave_days > remaining_leave:
        return {'message': 'Not enough leave days'}, 400

    leave.add()

    return leave_schema.dump(leave), 201


class LeaveResource(Resource):
    def get(self, id):
        '''
        Get leave entry
        '''
        leave = LeaveModel.get_leave(id)
        
        if leave:
            return leave_schema.dump(leave), 200
        else:
            return {'message': 'Leave not found'}, 404


    def put(self, id):
        '''
        Update leave entry
        '''
        json_data = None
        try:
            json_data = request.get_json()
        except:
            return {'message': 'No leave data provided'}, 400
        
        leave = LeaveModel.get_leave(id)
        if leave:
           return update_leave(leave, json_data)
        else:
            return {'message': 'Leave not found'}, 404
    

    def delete(self, id):
        '''
        Delete leave entry
        '''
        leave = LeaveModel.get_leave(id)
        if leave:
            leave.delete()
            return {'message': 'Leave deleted'}, 200
        else:
            return {'message': 'Leave not found'}, 404


class LeaveCreateResource(Resource):
    def post(self):
        '''
        Create a new leave entry
        '''
        json_data = None
        try:
            json_data = request.get_json()
        except:
            return {'message': 'No leave data provided'}, 400

        return create_leave(json_data)


class LeaveRemainingResource(Resource):
    def get(self, user_id, date_str):
        '''
        Get remaining leave for a user in the leave year preceeding
        the provided date
        '''
        date = LeaveModel.str_to_datetime(date_str)
        remaining = LeaveModel.get_remaining_leave(user_id, date)
        
        return {'remaining': remaining}, 200


class LeaveListResource(Resource):
    def get(self):
        '''
        Get all leave entries
        '''
        return leave_list_schema.dump(LeaveModel.get_all()), 200


    def delete(self):
        '''
        Delete all leave entries
        '''
        deleted = LeaveModel.delete_all()
        return {'message': '%d leave(s) deleted' % (deleted)}, 200