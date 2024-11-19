from flask_restful import Api, Resource, reqparse
from .models import *
api=Api()

class TransApi(Resource):
    def get(self, slotid, day,month,year):
        import datetime
        date=datetime.date(year,month,day)
        appoint=Appointment.query.filter_by(slotid=slotid,date=date).first()
        slot=[]
        if appoint and not appoint.availability:
            slot=[{'avail':False}]
        else:
            slot=[{'avail':True}]
        return slot
    
api.add_resource(TransApi,'/api/appointment/<slotid>/<int:day>/<int:month>/<int:year>')
