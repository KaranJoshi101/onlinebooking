from flask import Flask
from application.database import db
#create flask object
app=None
def create_app():
    app=Flask(__name__) #__name__ gives file and we encapsulate with flask
    app.debug=True
    password='Joshi098!'
    app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql://postgres.yxdrmxtcbaqchvrhqfwv:a-g4SGTknzENbpu@aws-0-us-east-1.pooler.supabase.com:6543/postgres'
    UPLOAD_FOLDER='https://drive.google.com/drive/folders/1G6PiaNCPTb4MB16HkEbkuDcM_bzJ2OsL'
    app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
    app.config['SECRET_KEY']="this is my secret key"
    db.init_app(app)
 
    app.app_context().push() #not very clear about this as of now but it kind of tells the 
    return app
    
app=create_app()
from application.controllers import * #imports endpoints from controllers.py

 #runs the flask object with debug on so that every change reflects on server automatically
