#otp generating function
def Otp():
    import random
    k=0
    for i in range(6):
        k=k*10+random.randrange(1,9)
    return k

def idgen(i):
    from uuid import uuid4
    return i+str(uuid4())[:5]

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

days={1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday',7:'Sunday'}
states=['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Jammu and Kashmir', 'Karnataka', 'Kerala', 'Ladakh', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand']
CITIES=[['Port Blair'],['Adoni', 'Amaravati', 'Anantapur', 'Chandragiri', 'Chittoor', 'Dowlaiswaram', 'Eluru', 'Guntur', 'Kadapa', 'Kakinada', 'Kurnool', 'Machilipatnam', 'Nagarjunakoṇḍa', 'Rajahmundry', 'Srikakulam', 'Tirupati', 'Vijayawada', 'Visakhapatnam', 'Vizianagaram', 'Yemmiganur'],['Itanagar'],['Guwahati', 'Silchar', 'Dibrugarh', 'Jorhat', 'Nagaon'],['Ara', 'Barauni', 'Begusarai', 'Bettiah', 'Bhagalpur', 'Bihar Sharif', 'Bodh Gaya', 'Buxar', 'Chapra', 'Darbhanga', 'Dehri', 'Dinapur Nizamat', 'Gaya', 'Hajipur', 'Jamalpur', 'Katihar', 'Madhubani', 'Motihari', 'Munger', 'Muzaffarpur', 'Patna', 'Purnia', 'Pusa', 'Saharsa', 'Samastipur', 'Sasaram', 'Sitamarhi', 'Siwan'],['Chandigarh'],['Ambikapur', 'Bhilai', 'Bilaspur', 'Dhamtari', 'Durg', 'Jagdalpur', 'Raipur', 'Rajnandgaon'],['Ambikapur', 'Bhilai', 'Bilaspur', 'Dhamtari', 'Durg', 'Jagdalpur', 'Raipur', 'Rajnandgaon'],['New Delhi'],['Madgaon', 'Panaji'],['Ahmadabad', 'Amreli', 'Bharuch', 'Bhavnagar', 'Bhuj', 'Dwarka', 'Gandhinagar', 'Godhra', 'Jamnagar', 'Junagadh', 'Kandla', 'Khambhat', 'Kheda', 'Mahesana', 'Morbi', 'Nadiad', 'Navsari', 'Okha', 'Palanpur', 'Patan', 'Porbandar', 'Rajkot', 'Surat', 'Surendranagar', 'Valsad', 'Veraval'],]
cities={}
for i in range(len(CITIES)):
    cities[states[i]]=CITIES[i]

#methods imported from flask module
from flask import Flask,render_template, redirect, request,url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app as app
import uuid as uuid
import os
import datetime
from email.message import EmailMessage
import ssl,smtplib

#models content imported in this file
from .models import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        
        if(email=='iamadmin@gmail.com' and password=='123'):
            return redirect('/admin/dashboard')
        d=Doctor.query.filter_by(email=email).first()
        if(d):
            return redirect(f'/{d.id}/doctor/dashboard')
        u = User.query.filter_by(email=email).first()
        if(u):
            if(u.password == password):
                return redirect(f'/{u.id}/dashboard')
            else:
                flash("Invalid Credentials")
        else:
            flash("Account does not exist.")

    return render_template('login_page.html')       
        
@app.route('/admin/dashboard',methods=['GET','POST'])
def adminDashboard():
    deptdocs=[]
    for i in Deptdoc.query.all():
        deptdocs.append((i,Doctor.query.get(i.docid)))
    return render_template('admin_dash.html',hospitals=Hospital.query.all(),deptdocs=deptdocs,departments=Department.query.all())

@app.route('/hospital/create',methods=['GET','POST'])
def hospitalCreate():
    if request.method=='POST':
        h=Hospital(id=idgen('H'),name=request.form.get('name'),state=request.form.get('state'),city=request.form.get('city'))
        db.session.add(h)
        db.session.commit()
        return redirect('/admin/dashboard')
    global states,cities
    return render_template('hosp_create.html',states=states,cities=cities)

@app.route("/<hId>/department/create",methods=['GET','POST'])
def deptCreate(hId):
    hospital=Hospital.query.get(hId)
    if request.method=='POST':
        h=Department(id=idgen('D'),name=request.form.get('name'),hid=hId)
        hospital.nDept+=1
        db.session.add(h)
        db.session.commit()
        return redirect('/admin/dashboard')
    
    return render_template('dept_create.html',hospital=hospital)

@app.route('/<hid>/<deptid>/doctor/create',methods=['GET','POST'])
def docCreate(hid,deptid):
    if request.method=='POST':
        s=Doctor(id=idgen('Do'),name=request.form.get('name'),gender=request.form.get('gender'),exp=request.form.get('exp'),qual=request.form.get('qual'),email=request.form.get('email'),password=request.form.get('pass'))
        db.session.add(s)
        
        from_=request.form.get('from').split(':')
        to=request.form.get('to').split(':')
        Department.query.get(deptid).nDoc+=1
        d=Deptdoc(id=idgen('DD'),deptid=deptid,docid=s.id)
        db.session.add(d)
    
        
        day=Days(id=idgen('DA'),ddid=d.id,day=request.form.get('day'))
        db.session.add(day)
        slot=Slots(id=idgen('SL'),daysid=day.id,from_=datetime.time(int(from_[0]),int(from_[1])),to=datetime.time(int(to[0]),int(to[1])))
        db.session.add(slot)
        file=request.files["photo"]
        if(file):
            max_size = 1024 * 1024
    

            if file and allowed_file(file.filename):
                # Process the file (e.g., save it)
                if len(file.read()) > max_size:
                    flash('Image size too large!')
                else:
                    file.seek(0)
                    s.photo=file
                    dp=secure_filename(s.photo.filename)
                    photo=str(uuid.uuid1())+"_"+dp
                    s.photo.save(os.path.join(app.config['UPLOAD_FOLDER'],photo))
                    s.photo=photo
                    
                    db.session.commit()
                    return redirect('/admin/dashboard')
            else:
                flash('Invalid image type')
        else:
            db.session.commit()
            return redirect('/admin/dashboard')
        global days
    return render_template('doc_create.html',days=days,hospital=Hospital.query.get(hid),department=Department.query.get(deptid))


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form.get('email')
        u=User.query.filter_by(email=email).first()
        if(u and u.verified):
            flash('email already exist')
            
        else:    
            otp=str(Otp())
            
            
            sender='wevoteteam@gmail.com'
            pwd='bdsdenzmphtgrymb'
            body="""

            Your otp to login: """+otp+"""
            Do not share the OTP with anyone.
            
            Regards,
            Team BookYourDoctor
            """
            em=EmailMessage()
            em['From']=sender
            em['To']=email
            em.set_content(body)
            context=ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(sender,pwd)
                smtp.sendmail(sender,email,em.as_string())
            if(u):
                u.otp=otp
            else:
                u=User(id=idgen('U'),email=email,otp=otp)
                db.session.add(u)
            db.session.commit()
            return redirect(f'/{u.id}/otp')

    return render_template('register.html')

@app.route('/<userId>/otp',methods=['GET','POST'])
def otpVerify(userId):
    u=User.query.get(userId)
    if request.method=='POST':
        otp=request.form.get('one')+request.form.get('two')+request.form.get('three')+request.form.get('four')+request.form.get('five')+request.form.get('six')
        u=User.query.get(userId)
        if(u.otp==otp):
            return redirect(f'/{userId}/setPassword')
        else:
            flash('Wrong otp! Try again')
    return render_template('otp.html',u=u)

@app.route('/<userId>/setPassword',methods=['GET','POST'])
def setPassword(userId):
    u=User.query.get(userId)
    if request.method=='POST':
        password=request.form.get('pass')
        u.password=password
        db.session.commit()
        if(u.nMembers):
            return redirect(f'/{userId}/dashboard')
            
        return redirect(f'/{userId}/addMember')
    return render_template('set_password.html',user=u)

@app.route('/<userId>/addMember', methods = ["GET","POST"])
def addMember(userId):
    u=User.query.get(userId)
    if request.method=='POST':
        name=request.form.get('name')
        gender=request.form.get('gender')
        state=request.form.get('state')
        city=request.form.get('city')
        import datetime
        p=Patient(id = idgen('P'),name=name,gender=gender,state=state,city=city,d_added=datetime.datetime.now(),uid=userId)
        db.session.add(p)
        u.verified=True
        u.nMembers+=1
        db.session.commit()
        return redirect(f'/{userId}/dashboard')
    global states,cities
    return render_template('add_member.html',user=u,states=states,cities=cities)

@app.route('/<userId>/dashboard')
def userDashboard(userId):
    u=User.query.get(userId)
    patients=Patient.query.filter_by(uid=userId).all()
    deptdocs=[]
    docdays=[]
    for i in Deptdoc.query.all():
        deptdocs.append((i,Doctor.query.get(i.docid)))
        global days
        docdays.append((Doctor.query.get(i.docid),i,[days[i.day] for i in Days.query.filter_by(ddid=i.id).all()]))

       
        

        

    slots=[(Days.query.get(i.daysid),i) for i in Slots.query.all()]

    global states,cities
    import datetime
    date=datetime.datetime.now()
    vdate=date+datetime.timedelta(days=15)
    
    return render_template('user_dash.html',slots=slots,docdays=docdays,date=date,vdate=vdate,user=u,patients=patients,states=states,cities=cities,hospitals=Hospital.query.all(),departments=Department.query.all(),deptdocs=deptdocs)

@app.route('/<userId>/book',methods=['GET','POST'])
def book(userId):
    if request.method=='POST':
        ddid=request.form.get('deptdoc')
        date=list(map(int,request.form.get('bookdate').split('-')))
        date=datetime.date(date[0],date[1],date[2])
        pid=request.form.get('patient')
        slotid=request.form.get('slot')
        appoint=Appointment.query.filter_by(date=date,slotid=slotid).first()
        if(appoint):
            if(appoint.token==20):
                return 'already full'
            appoint.token+=1
            token=appoint.token
            aid=appoint.id
            
        else:
            newappoint=Appointment(id=idgen('AP'),date=date,slotid=slotid,token=1)
            token=1
            db.session.add(newappoint)
            aid=newappoint.id
        deptdoc=Deptdoc.query.get(ddid)
        dept=Department.query.get(deptdoc.deptid)
        hosp=Hospital.query.get(dept.hid)
        doc=Doctor.query.get(deptdoc.docid)
        newpatient=Patientlist(id=idgen('PL'),aid=aid,pid=pid)
        patient=Patient.query.get(pid)
        slot=Slots.query.get(slotid)
        email=User.query.get(patient.uid).email
        sender='wevoteteam@gmail.com'
        pwd='bdsdenzmphtgrymb'
        body=f"""
Dear {patient.name},
Your appointment has been successfully booked.


Appointment Details given below:

    
    Hospital : {hosp.name}
    Department : {dept.name}
    Address : {hosp.city}, {hosp.state}
    Doctor : Dr. {doc.name}
    Date : {date}
    Slot : {slot.from_.strftime('%I:%M %p')} - {slot.to.strftime('%I:%M %p')}
    Token No. : {token}
    Patient Name : {patient.name}
    Gender : {patient.gender}
            
Regards,
Team BookYourDoctor
            """
        em=EmailMessage()
        em['From']=sender
        em['To']=email
        em.set_content(body)
        context=ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(sender,pwd)
            smtp.sendmail(sender,email,em.as_string())
        db.session.add(newpatient)
        db.session.commit()
        return redirect(f'/{userId}/dashboard')





@app.route('/<docid>/doctor/dashboard')
def doctorDashboard(docid): 
    deptdocs=[]
    docdates=[]
    for d in Deptdoc.query.filter_by(docid=docid).all():
        daysrec=Days.query.filter_by(ddid=d.id).all()
        schedule={}

        for day in daysrec:
            slots=Slots.query.filter_by(daysid=day.id).all()
            schedule[days[day.day]]=[(i.from_.strftime('%I:%M %p'),i.to.strftime('%I:%M %p')) for i in slots]
        dept=Department.query.get(d.deptid)
        hosp=Hospital.query.get(dept.hid)
        deptdocs.append((hosp,dept,schedule))
        print(schedule)
        today=datetime.date.today()
        for i in range(0,31):
            date=today+datetime.timedelta(days=i)
            if days[date.weekday()+1] in schedule:
                for slot in  Slots.query.filter_by(daysid=Days.query.filter_by(ddid=d.id,day=date.weekday()+1).first().id).all():
                    appoint=Appointment.query.filter_by(date=date,slotid=slot.id).first()
                    if(appoint):
                        docdates.append((hosp,dept,date,slot.from_,slot.to,appoint.token))
                    else:
                        docdates.append((hosp,dept,date,slot.from_.strftime('%I:%M %p'),slot.to.strftime('%I:%M %p'),0))
    print(docdates)
    return render_template('doctor_dash.html',doctor=Doctor.query.get(docid),deptdocs=deptdocs,docdates=docdates)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"),500


