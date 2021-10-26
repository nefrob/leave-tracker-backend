'''
Api endpoints for user management
'''

from flask_restful import Resource

from backend.models.user import User
from backend.schemas.user import UserSchema


user_schema = UserSchema()
user_list_schema = UserSchema(many=True)


class UserList(Resource):
    def get(self):
        '''
        Get all leave entries.
        '''
        return user_list_schema.dump(User.get_all()), 200