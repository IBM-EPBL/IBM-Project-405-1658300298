import os
from flask import Flask,redirect, url_for, request
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table,Column,Integer,String,ForeignKey
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

current_dir=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(current_dir,'authenticate.sqlite3')
db=SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Users(db.Model):
    __tablename__='users'
    user_name=db.Column(db.String,primary_key=True,nullable=False)
    password=db.Column(db.String,nullable=False)

@app.route('/', methods=["GET","POST"])
def hello_world():
    if request.method=="GET":
        return render_template("login crudeoil.html")
    elif request.method=="POST":
        username=request.form["user_name"]
        #print(username)
        delt=Users.query.filter(Users.user_name==username)
        try:
            print(delt[0])
        except:
            print('hi')
            return render_template('error.html')
        password=request.form["password"]
        user=Users.query.all()
        delt1=Users.query.filter(Users.password==password)
        try:
            print(delt1[0])
        except:
            print('hey')
            return render_template('error.html')
        #print(user)
        return render_template('indexcrudeoil.html',user=user)
engine=create_engine("sqlite:///./authenticate.sqlite3")
@app.route('/register', methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("login crudeoil2.html")
    elif request.method=="POST":
        #username=request.form["user_name"]
        #password=request.form["password"]
        with Session(engine,autoflush=False) as session:
            session.begin()
            user=Users(user_name=request.form['user_name'],password=request.form['password'])
            session.add(user)
            session.flush()
            session.commit()
        return render_template("login crudeoil2.html")
if __name__=='__main__':
	app.debug=False
	app.run()
