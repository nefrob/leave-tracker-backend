'''
User model schema
'''

from backend.schemas.ma import ma
from backend.models.user import User


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ('id', 'start_date', 'end_date')
        load_instance = True
