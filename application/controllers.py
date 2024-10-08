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

from flask import Flask,render_template, redirect, request,url_for,flash
from flask import current_app as app
from .models import *

@app.route('/')
def index():
    return render_template('index.html')

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
            u.verified=True
            db.session.commit()
            if(u.nMembers):
                return redirect(f'/{userId}/dashboard')
            
            return redirect(f'/{userId}/addMember')
        else:
            flash('Wrong otp! Try again')
    return render_template('otp.html',u=u)