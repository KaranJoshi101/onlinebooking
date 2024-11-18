from .database import db
class Hospital(db.Model):
    id=db.Column(db.String(),primary_key=True)
    name=db.Column(db.String())
    state=db.Column(db.String())
    city=db.Column(db.String())
    nDept=db.Column(db.Integer,default=0)
    rating=db.Column(db.Float,default=0)
    departments=db.relationship('Department',backref='hospital')

class Department(db.Model):
    id=db.Column(db.String(),primary_key=True)
    name=db.Column(db.String())
    nDoc=db.Column(db.Integer,default=0)
    rating=db.Column(db.Float)
    hid=db.Column(db.String(),db.ForeignKey('hospital.id'))
    deptdocs=db.relationship('Deptdoc',backref='department')

class Doctor(db.Model):
    id=db.Column(db.String(),primary_key=True)
    email=db.Column(db.String())
    password=db.Column(db.String())
    name=db.Column(db.String())
    gender=db.Column(db.String(1))
    qual=db.Column(db.String())
    exp=db.Column(db.Integer)
    photo=db.Column(db.String())
    deptdocs=db.relationship('Deptdoc',backref='doctor')

class Patient(db.Model):
    id=db.Column(db.String(),primary_key=True)
    name=db.Column(db.String())
    gender=db.Column(db.String(1))
    state=db.Column(db.String())
    city=db.Column(db.String())
    record=db.Column(db.Text)
    d_added=db.Column(db.DateTime)
    uid=db.Column(db.String(),db.ForeignKey('user.id'))
    patientlists=db.relationship('Patientlist',backref='patient')

class Deptdoc(db.Model):
    id=db.Column(db.String(),primary_key=True)
    deptid=db.Column(db.String(),db.ForeignKey('department.id'))
    docid=db.Column(db.String(),db.ForeignKey('doctor.id'))
    days=db.relationship('Days',backref='deptdoc')

class Appointment(db.Model):
    id=db.Column(db.String(),primary_key=True)
    date=db.Column(db.Date)
    slotid=db.Column(db.String(),db.ForeignKey('slots.id'))
    availability=db.Column(db.Boolean,default=True)
    tokenCount=db.Column(db.Integer,default=0)
    patientlists=db.relationship('Patientlist',backref='appointment')

class Patientlist(db.Model):
    id=db.Column(db.String(),primary_key=True)
    aid=db.Column(db.String(),db.ForeignKey('appointment.id'))
    pid=db.Column(db.String(),db.ForeignKey('patient.id'))
    token=db.Column(db.Integer)
    status=db.Column(db.String(),default='booked')

class User(db.Model):
    id=db.Column(db.String(),primary_key=True)
    password=db.Column(db.String())
    phone=db.Column(db.Integer)
    email=db.Column(db.String())
    nMembers=db.Column(db.Integer,default=0)
    d_created=db.Column(db.DateTime)
    otp=db.Column(db.String())
    verified=db.Column(db.Boolean)
    patients=db.relationship('Patient',backref='user')

class Days(db.Model):
    id=db.Column(db.String(),primary_key=True)
    ddid=db.Column(db.String(),db.ForeignKey('deptdoc.id'))
    day=db.Column(db.Integer)
    slots=db.relationship('Slots',backref='days')

class Slots(db.Model):
    id=db.Column(db.String(),primary_key=True)
    daysid=db.Column(db.String(),db.ForeignKey('days.id'))
    from_=db.Column(db.Time)
    to=db.Column(db.Time)
    appointments=db.relationship('Appointment',backref='slots')

