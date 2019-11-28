from flask import Flask,request
from flask import *
from blue import long
from upload import upload
from server import server
from login import login
from postcm import postcm
from monitor import monitor
import os
import datetime
from time import time
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask_pymongo import PyMongo
from flask_ckeditor import CKEditor
from forms import RichTextForm

app = Flask(__name__)
# session方式要＋此secret_key
app.config['SECRET_KEY'] = 'wwwxxx'
app.config['MONGO_DBNAME'] = 'todolist'
app.config['MONGO_URI'] = 'mongodb://todo:towait.com@172.16.230.132:27020/todolist'
app.url_map.strict_slashes = False
mongo = PyMongo(app)
ckeditor = CKEditor(app)
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.permanent_session_lifetime = datetime.timedelta(minutes=1440)
app.register_blueprint(long,url_prefix="/long")
app.register_blueprint(upload,url_prefix="/upload")
app.register_blueprint(server,url_prefix="/server")
app.register_blueprint(login,url_prefix="/login")
app.register_blueprint(postcm,url_prefix="/postcm")
app.register_blueprint(monitor,url_prefix="/monitor")
data_path = "/home/ops/ib-apps/apps/"
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
@app.route('/ckeditor')
def ckeditor():
    form = RichTextForm()
    return render_template('ckeditor.html',form = form)

@app.route('/updatev',methods=['GET','POST'])
def updatev():
    if request.method == 'GET':
        return render_template('update.html')
    else:
        ns = request.form.get('ns')
        version = request.form.get('version')
        service = request.form.get('service')
        text = "bash updateversion.sh -n {0} -v {1} -d {2}".format(ns,version,service)
        return render_template('update.html',text=text)


    return render_template('update.html')
@app.route('/deploy',methods=['GET','POST'])
def deploy():
    if request.method == 'GET':
        scripts_path="/home/ops/ib-apps/apps/"
        file_list = []
        str1 = "find /home/ops/ib-apps/apps/ -name version* |awk -F '/' '{print $NF}'"
        str2 = "find /home/ops/ib-apps/apps/ -name glob* |awk -F '/' '{print $NF}'"
        list1 = os.popen(str1).readlines()
        list2 = os.popen(str2).readlines()
        #list2 = list2.split('/')[-1]
        print(type(list1))
        print(type(list2))
        print(list2) 
        for li2 in list2:
            print(li2)
        return render_template('deploy.html', list1=list1,list2=list2)
    else:
        ns = request.form.get('ns')
        version = request.form.get('version')
        globel = request.form.get('global')
        service = request.form.get('service')
        alis = request.form.get('alis')
        print(ns)
        print(ns,version,globel,service,alis)
        service1 = service.split('-',1)[0]
        service2 = "/home/ops/ib-apps/apps/charts/{0}/{1}".format(service1,service)
        text = "/home/ops/bin/helm install -n {0} {1} -f /home/ops/ib-apps/apps/{2} -f /home/ops/ib-apps/apps/{3} --namespace={4}".format(alis,service2,version,globel,ns)
        command = str(text)
        #print(type(command))
        #result = os.popen(command)
        #print(result.read())
        #print (type(result))
        #return jsonify({'result': result})
        return render_template('deploy.html', command=command)
        #os.environ['ns']=str(ns)

        
#@app.route('/<path>')
#def today(path):
    #base_dir = os.path.dirname(__file__)
#    base_dir = os.path.dirname("/home/ops/ib-apps/apps/")
#    resp = make_response(open(os.path.join(base_dir, path)).read())
#    resp.headers["Content-type"]="application/json;charset=UTF-8"
#    return resp
@app.route('/lists/')
def lists():
    items = get_file_list()
    return render_template("list.html", items=items)
def get_file_list():
    files = []
    for item in os.listdir(data_path):
        files.append(item)
    return files

@app.route('/cat/<item>')
def cat():
    file = os.path.join(data_path,item)
    print("xxxx")
    print(file)
    f = open(file, 'r')
    return f.readline()
    
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=9090,
        debug=True
    )

