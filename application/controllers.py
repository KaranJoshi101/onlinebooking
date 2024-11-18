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
#code starting from here
days={1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday',7:'Sunday'}
states=['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Jammu and Kashmir', 'Karnataka', 'Kerala', 'Ladakh', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand','West Bengal']
CITIES=[['Port Blair'],['Adoni', 'Amaravati', 'Anantapur', 'Chandragiri', 'Chittoor', 'Dowlaiswaram', 'Eluru', 'Guntur', 'Kadapa', 'Kakinada', 'Kurnool', 'Machilipatnam', 'Nagarjunakoṇḍa', 'Rajahmundry', 'Srikakulam', 'Tirupati', 'Vijayawada', 'Visakhapatnam', 'Vizianagaram', 'Yemmiganur'],['Itanagar'],['Guwahati', 'Silchar', 'Dibrugarh', 'Jorhat', 'Nagaon'],['Ara', 'Barauni', 'Begusarai', 'Bettiah', 'Bhagalpur', 'Bihar Sharif', 'Bodh Gaya', 'Buxar', 'Chapra', 'Darbhanga', 'Dehri', 'Dinapur Nizamat', 'Gaya', 'Hajipur', 'Jamalpur', 'Katihar', 'Madhubani', 'Motihari', 'Munger', 'Muzaffarpur', 'Patna', 'Purnia', 'Pusa', 'Saharsa', 'Samastipur', 'Sasaram', 'Sitamarhi', 'Siwan'],['Chandigarh'],['Ambikapur', 'Bhilai', 'Bilaspur', 'Dhamtari', 'Durg', 'Jagdalpur', 'Raipur', 'Rajnandgaon'],['Daman','Diu','Silvassa'],['New Delhi'],['Madgaon', 'Panaji'],['Ahmadabad', 'Amreli', 'Bharuch', 'Bhavnagar', 'Bhuj', 'Dwarka', 'Gandhinagar', 'Godhra', 'Jamnagar', 'Junagadh', 'Kandla', 'Khambhat', 'Kheda', 'Mahesana', 'Morbi', 'Nadiad', 'Navsari', 'Okha', 'Palanpur', 'Patan', 'Porbandar', 'Rajkot', 'Surat', 'Surendranagar', 'Valsad', 'Veraval'],['Ambala', 'Bhiwani', 'Chandigarh', 'Faridabad', 'Firozpur Jhirka', 'Gurugram', 'Hansi', 'Hisar', 'Jind', 'Kaithal', 'Karnal', 'Kurukshetra', 'Panipat', 'Pehowa', 'Rewari', 'Rohtak', 'Sirsa', 'Sonipat'],['Bilaspur', 'Chamba', 'Dalhousie', 'Dharmshala', 'Hamirpur', 'Kangra', 'Kullu', 'Mandi', 'Nahan', 'Shimla', 'Una'],['Anantnag', 'Baramula', 'Doda', 'Gulmarg', 'Jammu', 'Kathua', 'Punch', 'Rajouri', 'Srinagar', 'Udhampur'],['Bokaro', 'Chaibasa', 'Deoghar', 'Dhanbad', 'Dumka', 'Giridih', 'Hazaribag', 'Jamshedpur', 'Jharia', 'Rajmahal', 'Ranchi', 'Saraikela'],['Badami', 'Ballari', 'Bengaluru', 'Belagavi', 'Bhadravati', 'Bidar', 'Chikkamagaluru', 'Chitradurga', 'Davangere', 'Halebid', 'Hassan', 'Hubballi-Dharwad', 'Kalaburagi', 'Kolar', 'Madikeri', 'Mandya', 'Mangaluru', 'Mysuru', 'Raichur', 'Shivamogga', 'Shravanabelagola', 'Shrirangapattana', 'Tumakuru', 'Vijayapura'],['Alappuzha', 'Vatakara', 'Idukki', 'Kannur', 'Kochi', 'Kollam', 'Kottayam', 'Kozhikode', 'Mattancheri', 'Palakkad', 'Thalassery', 'Thiruvananthapuram', 'Thrissur'],['Kargil', 'Leh'],['Balaghat', 'Barwani', 'Betul', 'Bharhut', 'Bhind', 'Bhojpur', 'Bhopal', 'Burhanpur', 'Chhatarpur', 'Chhindwara', 'Damoh', 'Datia', 'Dewas', 'Dhar', 'Dr. Ambedkar Nagar (Mhow)', 'Guna', 'Gwalior', 'Hoshangabad', 'Indore', 'Itarsi', 'Jabalpur', 'Jhabua', 'Khajuraho', 'Khandwa', 'Khargone', 'Maheshwar', 'Mandla', 'Mandsaur', 'Morena', 'Murwara', 'Narsimhapur', 'Narsinghgarh', 'Narwar', 'Neemuch', 'Nowgong', 'Orchha', 'Panna', 'Raisen', 'Rajgarh', 'Ratlam', 'Rewa', 'Sagar', 'Sarangpur', 'Satna', 'Sehore', 'Seoni', 'Shahdol', 'Shajapur', 'Sheopur', 'Shivpuri', 'Ujjain', 'Vidisha'],['Ahmadnagar', 'Akola', 'Amravati', 'Aurangabad', 'Bhandara', 'Bhusawal', 'Bid', 'Buldhana', 'Chandrapur', 'Daulatabad', 'Dhule', 'Jalgaon', 'Kalyan', 'Karli', 'Kolhapur', 'Mahabaleshwar', 'Malegaon', 'Matheran', 'Mumbai', 'Nagpur', 'Nanded', 'Nashik', 'Osmanabad', 'Pandharpur', 'Parbhani', 'Pune', 'Ratnagiri', 'Sangli', 'Satara', 'Sevagram', 'Solapur', 'Thane', 'Ulhasnagar', 'Vasai-Virar', 'Wardha', 'Yavatmal'],['Imphal'],['Cherrapunji','Shillong'],['Aizawl','Lunglei'],['Kohima', 'Mon', 'Phek', 'Wokha', 'Zunheboto'],['Balangir', 'Baleshwar', 'Baripada', 'Bhubaneshwar', 'Brahmapur', 'Cuttack', 'Dhenkanal', 'Kendujhar', 'Konark', 'Koraput', 'Paradip', 'Phulabani', 'Puri', 'Sambalpur', 'Udayagiri'],['Karaikal', 'Mahe', 'Puducherry', 'Yanam'],['Amritsar', 'Batala', 'Chandigarh', 'Faridkot', 'Firozpur', 'Gurdaspur', 'Hoshiarpur', 'Jalandhar', 'Kapurthala', 'Ludhiana', 'Nabha', 'Patiala', 'Rupnagar', 'Sangrur'],['Abu', 'Ajmer', 'Alwar', 'Amer', 'Barmer', 'Beawar', 'Bharatpur', 'Bhilwara', 'Bikaner', 'Bundi', 'Chittaurgarh', 'Churu', 'Dhaulpur', 'Dungarpur', 'Ganganagar', 'Hanumangarh', 'Jaipur', 'Jaisalmer', 'Jalor', 'Jhalawar', 'Jhunjhunu', 'Jodhpur', 'Kishangarh', 'Kota', 'Merta', 'Nagaur', 'Nathdwara', 'Pali', 'Phalodi', 'Pushkar', 'Sawai Madhopur', 'Shahpura', 'Sikar', 'Sirohi', 'Tonk', 'Udaipur'],['Gangtok', 'Gyalshing', 'Lachung', 'Mangan'],['Arcot', 'Chengalpattu', 'Chennai', 'Chidambaram', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul', 'Erode', 'Kanchipuram', 'Kanniyakumari', 'Kodaikanal', 'Kumbakonam', 'Madurai', 'Mamallapuram', 'Nagappattinam', 'Nagercoil', 'Palayamkottai', 'Pudukkottai', 'Rajapalayam', 'Ramanathapuram', 'Salem', 'Thanjavur', 'Tiruchchirappalli', 'Tirunelveli', 'Tiruppur', 'Thoothukudi', 'Udhagamandalam', 'Vellore'],['Hyderabad', 'Karimnagar', 'Khammam', 'Mahbubnagar', 'Nizamabad', 'Sangareddi', 'Warangal'],['Agartala'],['Agra', 'Aligarh', 'Amroha', 'Ayodhya', 'Azamgarh', 'Bahraich', 'Ballia', 'Banda', 'Bara Banki', 'Bareilly', 'Basti', 'Bijnor', 'Bithur', 'Budaun', 'Bulandshahr', 'Deoria', 'Etah', 'Etawah', 'Faizabad', 'Farrukhabad-cum-Fatehgarh', 'Fatehpur', 'Fatehpur Sikri', 'Ghaziabad', 'Ghazipur', 'Gonda', 'Gorakhpur', 'Hamirpur', 'Hardoi', 'Hathras', 'Jalaun', 'Jaunpur', 'Jhansi', 'Kannauj', 'Kanpur', 'Lakhimpur', 'Lalitpur', 'Lucknow', 'Mainpuri', 'Mathura', 'Meerut', 'Mirzapur-Vindhyachal', 'Moradabad', 'Muzaffarnagar', 'Partapgarh', 'Pilibhit', 'Prayagraj', 'Rae Bareli', 'Rampur', 'Saharanpur', 'Sambhal', 'Shahjahanpur', 'Sitapur', 'Sultanpur', 'Tehri', 'Varanasi'],['Almora', 'Dehra Dun', 'Haridwar', 'Mussoorie', 'Nainital', 'Pithoragarh'],['Alipore', 'Alipur Duar', 'Asansol', 'Baharampur', 'Bally', 'Balurghat', 'Bankura', 'Baranagar', 'Barasat', 'Barrackpore', 'Basirhat', 'Bhatpara', 'Bishnupur', 'Budge Budge', 'Burdwan', 'Chandernagore', 'Darjeeling', 'Diamond Harbour', 'Dum Dum', 'Durgapur', 'Halisahar', 'Haora', 'Hugli', 'Ingraj Bazar', 'Jalpaiguri', 'Kalimpong', 'Kamarhati', 'Kanchrapara', 'Kharagpur', 'Cooch Behar', 'Kolkata', 'Krishnanagar', 'Malda', 'Midnapore', 'Murshidabad', 'Nabadwip', 'Palashi', 'Panihati', 'Purulia', 'Raiganj', 'Santipur', 'Shantiniketan', 'Shrirampur', 'Siliguri', 'Siuri', 'Tamluk', 'Titagarh']]
cities={}
for i in range(len(CITIES)):
    cities[states[i]]=CITIES[i]

#methods imported from flask module
from flask import Flask,render_template, redirect, request,url_for, flash

from flask import current_app as app
import uuid as uuid
import os
import datetime
from werkzeug.utils import secure_filename
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
    today=datetime.date.today()
    monthly_booking={}
    for i in range(0,31):
        date=today+datetime.timedelta(days=i)
        appointments=Appointment.query.filter_by(date=date).all()
        daily_booking=[]
        for a in appointments:
            s=Slots.query.get(a.slotid)
            d=Days.query.get(s.daysid)
            dd=Deptdoc.query.get(d.ddid)
            daily_booking.append((a,dd,s))
        monthly_booking[date]=daily_booking




    return render_template('admin_dash.html',hospitals=Hospital.query.all(),deptdocs=deptdocs,departments=Department.query.all(),monthly_booking=monthly_booking)

@app.route('/admin/search')
def adminSearch():
    hospitals=Hospital.query.all()
    departments=Department.query.all()
    doctors=Doctor.query.all()
    return render_template('admin_search.html',hospitals=hospitals,departments=departments,doctors=doctors)

@app.route('/<docId>/doctor/delete')
def doctorDelete(docId):
    doc=Doctor.query.get(docId)
    dd=Deptdoc.query.filter_by(docId=docId).all()
    for i in dd:
        i.nDoc-=1
    db.session.delete(doc)
    db.session.commit()
    return redirect('/admin/dashboard')

@app.route('/<deptid>/<docid>/doctor/modify',methods=['GET','POST'])
def doctordeptModify(deptid,docid):
    return doctorModify(deptid=deptid,docid=docid)

@app.route('/<docid>/doctor/modify',methods=['GET','POST'])
def doctorModify(docid,deptid=None):
    if request.method=='POST':
        email=request.form.get('email')
        name=request.form.get('name')
        gender=request.form.get('gender')
        exp=request.form.get('exp')
        qual=request.form.get('qual')
        password=request.form.get('pass')
        from_=request.form.get('from').split(':')
        to=request.form.get('to').split(':')
        day=request.form.get('day')
        file=request.files["photo"]
        s=Doctor.query.get(docid)
        if name:
            s.name=name
        if gender:
            s.gender=gender
        if exp:
            s.exp=exp
        if qual:
            s.qual=qual
        if email:
            s.email=email
        if password:
            s.password=password
        deptid=request.form.get('deptid')
        modify=request.form.get('modify')
        if not modify:         
            Department.query.get(deptid).nDoc+=1
        dd=Deptdoc.query.filter_by(deptid=deptid,docid=docid).first()
        if not dd:
            dd=Deptdoc(id=idgen('DD'),deptid=deptid,docid=s.id)
            db.session.add(dd)
        
        if day:
            day=Days.query.filter_by(day=day,ddid=dd.id).first()
            if day:
                slot=Slots(id=idgen('SL'),daysid=day.id,from_=datetime.time(int(from_[0]),int(from_[1])),to=datetime.time(int(to[0]),int(to[1])))
            else:
                day=Days(id=idgen('DA'),ddid=dd.id,day=request.form.get('day'))
                db.session.add(day)
            slot=Slots(id=idgen('SL'),daysid=day.id,from_=datetime.time(int(from_[0]),int(from_[1])),to=datetime.time(int(to[0]),int(to[1])))
            db.session.add(slot)
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
    return render_template('doctor-modify.html',days=days,doctor=Doctor.query.get(docid),department=Department.query.get(deptid))

@app.route('/<docId>/doctor/details')
def docDetails(docId):
    deptdocs=[]
    for d in Deptdoc.query.filter_by(docid=docId).all():
        daysrec=Days.query.filter_by(ddid=d.id).all()
        schedule={}

        for day in daysrec:
            slots=Slots.query.filter_by(daysid=day.id).all()
            if(days[day.day] in schedule):
                schedule[days[day.day]]+=[(i.from_.strftime('%I:%M %p'),i.to.strftime('%I:%M %p')) for i in slots]
            else:
                schedule[days[day.day]]=[(i.from_.strftime('%I:%M %p'),i.to.strftime('%I:%M %p')) for i in slots]
        dept=Department.query.get(d.deptid)
        hosp=Hospital.query.get(dept.hid)
        deptdocs.append((hosp,dept,schedule))
    return render_template('doctor_details.html',doctor=Doctor.query.get(docId),deptdocs=deptdocs)

@app.route('/<hId>/hospital/details')
def hospitalDetails(hId):
    return render_template('hospital_details.html',Hospital=Hospital.query.get(hId))

@app.route('/<deptId>/department/details')
def departmentDetails(deptId):
    return render_template('department_details.html',Department=Department.query.get(deptId))

@app.route('/<appId>/appointment/details')
def appoinmentDetails(appId):
    app=Appointment.query.get(appId)
    return render_template('appointment_details.html',Appointment=app,patientlist=[(i,Patient.query.get(i.pid)) for i in app.patientlists])

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
def docCreate(hid,deptid,modify=None):
    if request.method=='POST':
        email=request.form.get('email')
        if (Doctor.query.filter_by(email=email).first() or User.query.filter_by(email=email).first()):
            flash('Account already exist')
        else:
            name=request.form.get('name')
            gender=request.form.get('gender')
            exp=request.form.get('exp')
            qual=request.form.get('qual')
            password=request.form.get('pass')
            from_=request.form.get('from').split(':')
            to=request.form.get('to').split(':')
            day=request.form.get('day')
            file=request.files["photo"]
            
            s=Doctor(id=idgen('Do'),name=name,gender=gender,exp=exp,qual=qual,email=email,password=password)
            db.session.add(s)
            Department.query.get(deptid).nDoc+=1
            d=Deptdoc(id=idgen('DD'),deptid=deptid,docid=s.id)
            db.session.add(d)
            day=Days(id=idgen('DA'),ddid=d.id,day=day)
            db.session.add(day)
            slot=Slots(id=idgen('SL'),daysid=day.id,from_=datetime.time(int(from_[0]),int(from_[1])),to=datetime.time(int(to[0]),int(to[1])))
            db.session.add(slot)
                
    
                
                


            
            
        
                

            
        
            
            
            
            
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
    return render_template('doc_create.html',days=days,hospital=Hospital.query.get(hid),department=Department.query.get(deptid),modify=Doctor.query.get(modify))


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form.get('email')
        u=User.query.filter_by(email=email).first()
        if(u and u.verified):
            flash('email already exist')
            
        else:    
            otp=str(Otp())
            
            
            sender='bookmydoctor01@gmail.com'
            pwd='dtnbgzyxldgnkjfc'
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
        db.session.commit
        return redirect(f'/{userId}/dashboard')
    maxi=False
    if(u.nMembers>=6):
        maxi=True
    global states,cities
    return render_template('add_member.html',user=u,states=states,cities=cities,maxi=maxi)

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
    patientsappointment=[]
    for i in u.patients:
        patientsappointment.append((i,i.patientlists,[Appointment.query.get(i.aid) for i in i.patientlists]))


        
    slots={}
    for day in Days.query.all():
        slots[day]=Slots.query.filter_by(daysid=day.id).all()

    global states,cities
    import datetime
    date=datetime.datetime.now()
    vdate=date+datetime.timedelta(days=15)
    
    return render_template('user_dash.html',slots=slots,docdays=docdays,date=date,vdate=vdate,user=u,patients=patients,states=states,cities=cities,hospitals=Hospital.query.all(),departments=Department.query.all(),deptdocs=deptdocs,patientsappointment=patientsappointment)

@app.route('/<userId>/book',methods=['GET','POST'])
def book(userId):
    if request.method=='POST':
        ddid=request.form.get('deptdoc')
        date=list(map(int,request.form.get('bookdate').split('-')))
        date=datetime.date(date[0],date[1],date[2])
        pid=request.form.get('patient')
        print(pid)
        slotid=request.form.get('slot')
        appoint=Appointment.query.filter_by(date=date,slotid=slotid).first()
        if(appoint):
            if(appoint.tokenCount==20):
                flash('sorry! booking already full')
            appoint.tokenCount+=1
            tokenCount=appoint.tokenCount
            aid=appoint.id
            
        else:
            newappoint=Appointment(id=idgen('AP'),date=date,slotid=slotid,tokenCount=1)
            tokenCount=1
            db.session.add(newappoint)
            aid=newappoint.id
        deptdoc=Deptdoc.query.get(ddid)
        dept=Department.query.get(deptdoc.deptid)
        hosp=Hospital.query.get(dept.hid)
        doc=Doctor.query.get(deptdoc.docid)
        newpatient=Patientlist(id=idgen('PL'),aid=aid,pid=pid,token=tokenCount)
        patient=Patient.query.get(pid)
        slot=Slots.query.get(slotid)
        email=User.query.get(patient.uid).email
        sender='bookmydoctor01@gmail.com'
        pwd='dtnbgzyxldgnkjfc'
        subject='Appointment Booking Details'
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
    Token No. : {newpatient.token}
    Patient Name : {patient.name}
    Gender : {patient.gender}
            
Regards,
Team BookMyDoctor
            """
        em=EmailMessage()
        em['Subject']=subject
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
            if(days[day.day] in schedule):
                schedule[days[day.day]]+=[(i.from_.strftime('%I:%M %p'),i.to.strftime('%I:%M %p')) for i in slots]
            else:
                schedule[days[day.day]]=[(i.from_.strftime('%I:%M %p'),i.to.strftime('%I:%M %p')) for i in slots]
        dept=Department.query.get(d.deptid)
        hosp=Hospital.query.get(dept.hid)
        deptdocs.append((hosp,dept,schedule))
        today=datetime.date.today()
        for i in range(0,31):
            date=today+datetime.timedelta(days=i)
            if days[date.weekday()+1] in schedule:
                for slot in  Slots.query.filter_by(daysid=Days.query.filter_by(ddid=d.id,day=date.weekday()+1).first().id).all():
                    appoint=Appointment.query.filter_by(date=date,slotid=slot.id).first()
                    if(appoint):
                        docdates.append((hosp,dept,date,slot.from_.strftime('%I:%M %p'),slot.to.strftime('%I:%M %p'),appoint.tokenCount))
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


