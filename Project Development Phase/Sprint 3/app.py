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
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import requests
import numpy as np


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
@app.route('/index',methods=['GET',"POST"])
def index_page():
    if request.method=="GET":
        return render_template('index_new.html')
    elif request.method=="POST":
        x_input=str(request.form["past"])
        
        x_input=x_input.split(',')
        for i in range(0,len(x_input)):
        	x_input[i]=float(x_input[i])
        print(x_input)
        x_input=np.array(x_input).reshape(1,-1)
        temp_input=list(x_input)
        temp_input=temp_input[0].tolist()
        lst_output=[]
        n_steps=10
        i=0
        while(i<1):
        	if(len(temp_input)>10):
        		print("temp_input",temp_input)
        		x_input=np.array(temp_input[1:])
        		print("{} day input {}".format(i,x_input))
        		x_input=x_input.reshape((1,n_steps,1))
        		print(x_input)
        		yhat=model.predict(x_input,verbose=0)
        		print("{} day output {}".format(i,yhat))
        		temp_input.extend(yhat[0].tolist())
        		temp_input=temp_input[1:]
        		print(temp_input)
        		lst_output.extend(yhat.tolist())
        		i=i+1
        	else:
        		x_input=x_input.reshape((1,n_steps,1))
        		yhat=model.predict(x_input,verbose=0)
        		print(yhat[0])
        		temp_input.extend(yhat[0].tolist())
        		print(len(temp_input))
        		lst_output.extend(yhat.tolist())
        		i=i+1
        	print(lst_output)
        return render_template('results.html',lst_output=lst_output)
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
        return redirect(url_for('index_page'))

        #return render_template('indexcrudeoil.html')
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
model=load_model("crude_oil.h5")
print("Loaded model from disk")
if __name__=='__main__':
	app.debug=False
	app.run()
