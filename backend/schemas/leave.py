'''
Leave model schema
'''

from backend.schemas.ma import ma
from backend.models.leave import LeaveModel


class LeaveSchema(ma.Schema):
    class Meta:
        model = LeaveModel
        fields = ('id', 'user_id', 'start_date', 'end_date')
        load_instance = True
        include_fk = True
