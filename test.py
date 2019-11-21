from flask import Flask,request
from flask import *
from blue import long
from upload import upload
from server import server
from login import login
import datetime
app = Flask(__name__)
# session方式要＋此secret_key
app.config['SECRET_KEY'] = 'wwwxxx'
app.permanent_session_lifetime = datetime.timedelta(minutes=1440)
app.register_blueprint(long,url_prefix="/long")
app.register_blueprint(upload,url_prefix="/upload")
app.register_blueprint(server,url_prefix="/server")
app.register_blueprint(login,url_prefix="/login")
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

@app.route('/post/',methods=['GET','POST'])
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

