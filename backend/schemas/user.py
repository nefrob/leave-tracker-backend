'''
User model schema
'''

from backend.schemas.ma import ma
from backend.models.user import UserModel


class UserSchema(ma.Schema):
    class Meta:
        model = UserModel
        fields = ('id',)
        load_instance = True
