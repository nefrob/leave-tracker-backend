'''
Api endpoints for user management
'''

from requests.api import delete
from flask_restful import Resource

from backend.models.user import UserModel
from backend.schemas.user import UserSchema


user_schema = UserSchema()
user_list_schema = UserSchema(many=True)


class UserResource(Resource):
    def get(self, id):
        '''
        Get user entry
        '''
        a = UserModel.get_user(id)
        
        if a:
            return user_schema.dump(a), 200
        else:
            return {'message': 'User not found'}, 404


    def put(self, id):
        '''
        Add user entry
        '''
        user = UserModel.get_user(id)
       
        if user: # fixme: update user fields here
            return {'message': 'User already exists'}, 400
        else:
            user = UserModel()
            user.add()

            return user_schema.dump(user), 201


    def delete(self, id):
        '''
        Delete user entry
        '''
        user = UserModel.get_user(id)
        
        if user:
            user.delete()
            return {'message': 'User deleted'}, 200
        else:
            return {'message': 'User not found'}, 404


class UserListResource(Resource):
    def get(self):
        '''
        Get all user entries
        '''
        users = UserModel.get_all()
        return user_list_schema.dump(users), 200


    def delete(self):
        '''
        Delete all user entries
        '''
        deleted = UserModel.delete_all()
        return {'message': '%d user(s) deleted' % (deleted)}, 200