'''
Api endpoints for leave management
'''

from flask_restful import Resource

from backend.models.leave import Leave
from backend.schemas.leave import LeaveSchema


leave_schema = LeaveSchema()
leave_list_schema = LeaveSchema(many=True)


class LeaveList(Resource):
    def get(self):
        '''
        Get all leave entries.
        '''
        return leave_list_schema.dump(Leave.get_all()), 200