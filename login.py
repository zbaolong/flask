from flask import Blueprint, render_template, request,redirect,make_response, session
import db
login = Blueprint("login",__name__)
@login.route('/')
def index():
    return render_template("login.html")
@login.route('/auth1',methods=['get','post'])
def auth1():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == "test" and password == "test":
        response = make_response(redirect("/list/"))
        response.set_cookie('username',username, max_age=3600)
        return response
        #return "success"
        #return redirect("/list/")
    else:
        return redirect("/login/")
@login.route('/logout1')
def logout1():
    response = make_response(redirect("/login/"))
    response.delete_cookie('username')
    return response
    
@login.route('/auth',methods=['get','post'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')
    sql = "select * from user where username = %s and password = %s"
    result = db.selectByParameters(sql,(username,password))
    if result:
    #if username == "test" and password == "test":
        session['username'] = username
        return redirect("/list/")
    else:
        return redirect("/login/")
@login.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    return redirect("/login/")

