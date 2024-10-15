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

states=['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Jammu and Kashmir', 'Karnataka', 'Kerala', 'Ladakh', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand']
CITIES=[['Port Blair'],['Adoni', 'Amaravati', 'Anantapur', 'Chandragiri', 'Chittoor', 'Dowlaiswaram', 'Eluru', 'Guntur', 'Kadapa', 'Kakinada', 'Kurnool', 'Machilipatnam', 'Nagarjunakoṇḍa', 'Rajahmundry', 'Srikakulam', 'Tirupati', 'Vijayawada', 'Visakhapatnam', 'Vizianagaram', 'Yemmiganur'],['Itanagar'],]
cities={}
for i in range(len(CITIES)):
    cities[states[i]]=CITIES[i]

#methods imported from flask module
from flask import Flask,render_template, redirect, request,url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app as app
import uuid as uuid
import os

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
        Department.query.get(deptid).nDoc+=1
        d=Deptdoc(id=idgen('DD'),deptid=deptid,docid=s.id)
        db.session.add(d)
        file=request.files["photo"]
        if(file):
            max_size = 1024 * 1024
    
            print('yes')

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
                    print('wow')
                    return redirect('/admin/dashboard')
            else:
                flash('Invalid image type')
        else:
            db.session.commit()
            return redirect('/admin/dashboard')
    return render_template('doc_create.html',hospital=Hospital.query.get(hid),department=Department.query.get(deptid))


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form.get('email')
        u=User.query.filter_by(email=email).first()
        if(u and u.verified):
            flash('email already exist')
            
        else:    
            otp=str(Otp())
            
            from email.message import EmailMessage
            import ssl,smtplib
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
        address=request.form.get('address')
        import datetime
        p=Patient(id = idgen('P'),name=name,gender=gender,location=address,d_added=datetime.datetime.now(),uid=userId)
        db.session.add(p)
        u.verified=True
        db.session.commit()
        return render_template(f'/{userId}/dashboard')
    return render_template('add_member.html',user=u)

@app.route('/<userId>/dashboard')
def userDashboard(userId):
    u=User.query.get(userId)
    patient=Patient.query.filter_by(uid=userId).first()
    return render_template('user_dash.html',user=u,patient=patient)

@app.route('/<pid>/book')
def patientBook(pid):
    
    global states,cities
    return render_template('selecthost.html',states=states,cities=cities)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"),500


