from flask import Flask,request
from flask import *
from blue import long
from upload import upload
from server import server
from login import login
from postcm import postcm
from monitor import monitor

import datetime
from time import time
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask_pymongo import PyMongo

app = Flask(__name__)
# session方式要＋此secret_key
app.config['SECRET_KEY'] = 'wwwxxx'
app.config['MONGO_DBNAME'] = 'todolist'
app.config['MONGO_URI'] = 'mongodb://todo:towait.com@172.16.230.132:27020/todolist'
app.url_map.strict_slashes = False
mongo = PyMongo(app)
app.permanent_session_lifetime = datetime.timedelta(minutes=1440)
app.register_blueprint(long,url_prefix="/long")
app.register_blueprint(upload,url_prefix="/upload")
app.register_blueprint(server,url_prefix="/server")
app.register_blueprint(login,url_prefix="/login")
app.register_blueprint(postcm,url_prefix="/postcm")
app.register_blueprint(monitor,url_prefix="/monitor")
@app.before_request
def before_request():
    print(request.path)
    if request.path == "/login/" or request.path == "/login/auth" or request.path == "/home/" or request.path.endswith(".js") or request.path.endswith(".css"):
        pass
    else:
        #username = request.cookies.get('username') 这是cookie方式注释掉的
        username = session.get('username')
        if not username:
            return redirect('/login/')
@app.route('/')
def index():
    return 'hello world'
@app.route('/test/')
def xxx():
    return render_template('test.html')
@app.route('/home/')
def home():
    return render_template('home.html')
@app.route('/get/')
def get():
    print(request.args)
    server_name = request.args.get("server_name")
    server_ip = request.args.get("server_ip")
    return "servername is {0}, serverip is {1}".format(server_name,server_ip)
    #return render_template('home.html')

@app.route('/postx/',methods=['GET','POST'])
def post():
    print(request.form)
    username = request.form.get("username")
    password = request.form.get("passwd")
    return "username is {0}, password is {1}".format(username,password)
@app.route('/ajaxget/')
def ajaxget():
    server_name = request.args.get('server_name')
    server_ip = request.args.get('server_ip')
    return server_name + "ip is" + server_ip

@app.route('/ajaxpost',methods=['GET','POST'])
def ajaxpost():
    username = request.form.get('username')
    passwd = request.form.get('passwd')
    info = {"username":username,"password":passwd}
    return json.dumps(info)
    #return username + "is" + passwd

#todolist
@app.route("/haha", methods=['GET'])
def home_page():
    return "<h1>Hello World!</h1>"


class Todo(object):
    @classmethod
    def create_doc(cls,user,content):
        return {
            'user': user,
            'content': content,
            'created_at': time(),
            'is_finished': False,
            'finished_at': None
        }
@app.route('/task/',methods=['GET'])
def task():
    todos = mongo.db.todos.find({})
    return  render_template('todo.html',todos=todos)

@app.route('/todo/', methods=['POST'])
def add():
    user = request.form.get('user', None)
    content = request.form.get('content', None)
   # if not user:
   #     abort(400)
   # mongo.db.todos.insert(Todo.create_doc(user))
   # if not content:
   #     abort(400)
    mongo.db.todos.insert(Todo.create_doc(user,content))
    return redirect('/task/')

@app.route('/todo/<content>/finished')
def finish(content):
    result = mongo.db.todos.update_one(
        {'content':content},
        {
            '$set': {
                'is_finished': True,
                'finished_at': time()
            }
        }    
    )
    return redirect('/task/')

@app.route('/todo/<content>')
def delete(content):
    result = mongo.db.todos.delete_one(
        {'content':content}
    )
    return redirect('/task/')

@app.route('/todo/search/<content>')
def find():
    #content = request.form.get('content')   
   # todos = mongo.db.todos.find(
   #     {'user': {"$regex": content},'content': {"$regex": content}} 
   # )
    todos = mongo.db.todos.find({"$or" : [{ "user" : { "$regex" : content} }, { "content" : { "$regex" : content} }]})
    return  render_template('todo.html', todos=todos)


@app.route('/ajaxtest/')
def ajaxtest():
    return 'xxx test'
@app.route('/list/')
def list():
    return render_template('server.html')
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=9090,
        debug=True
    )

