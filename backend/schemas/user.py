'''
User model schema
'''

from backend.schemas.ma import ma
from backend.models.user import UserModel


class UserSchema(ma.Schema):
    class Meta:
        model = UserModel
        fields = ('id', 'children')
        load_instance = True
