'''
User model schema
'''

from backend.schemas.ma import ma
from backend.models.user import User


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id')
        load_instance = True
