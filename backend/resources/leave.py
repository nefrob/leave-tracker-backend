'''
Api endpoints for leave management
'''

from requests.api import delete
from flask_restful import Resource

from backend.models.leave import LeaveModel
from backend.schemas.leave import LeaveSchema


leave_schema = LeaveSchema()
leave_list_schema = LeaveSchema(many=True)


class LeaveListResource(Resource):
    def get(self):
        '''
        Get all leave entries.
        '''
        return leave_list_schema.dump(LeaveModel.get_all()), 200


    def delete(self):
        '''
        Delete all leave entries
        '''
        deleted = LeaveModel.delete_all()
        return {'message': '%d leave(s) deleted' % (deleted)}, 200