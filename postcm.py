from flask import Blueprint, render_template, request, jsonify
import os
import paramiko
import json
postcm = Blueprint("postcm",__name__)
@postcm.route('/')
def hello_world():
    return render_template('post.html',title="this is")

@postcm.route('/post1',methods=['POST','GET'])
def post1():
    name=request.form.get('name')
    hostname = 'ip'
    command = str(name)
    port = 22
    username = "username"
    password = "pwd"
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname, port, username, password)
    stdin, stdout, sterr = s.exec_command(command)
    z = stdout.read()
    s.close()
    return jsonify({'result': z})
@postcm.route('/postman',methods=['POST','GET'])
def postman():
    name=request.form.get('name')
    command = str(name)
    result = os.popen(command).read()
    print (type(result))
    return jsonify({'result': result})
