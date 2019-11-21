from flask import Blueprint,request,send_from_directory
import db
import json
import os
import time
import tool_excel
server = Blueprint("server",__name__)
@server.route('/index')
def index():
    return "server is bule"
@server.route('/getall')
def getall():
    sql = "select * from server;"
    result = db.selectByParameters(sql)
    return json.dumps(result)
@server.route('/get_by_page',methods=['GET','POST'])
def get_by_page():
    info = request.get_data()
    info = json.loads(info)
    pagenow = info['pagenow']
    pagesize = info['pagesize']
    search = info['search']
    search = "%{0}%".format(search)
    sql = 'select * from server where name like %s or ip like %s  limit %s,%s'
    params = (search ,search,(pagenow-1)*pagesize,pagesize)
    result = db.selectByParameters(sql,params=params)
    return json.dumps(result)
@server.route('/get_by_id')
def get_by_id():
    id = int( request.args.get('id'))
    sql = "select * from server where id = %s"
    result = db.selectByParameters( sql, params=(id, ) )
    return json.dumps( result )
@server.route('/update', methods=['get', 'post'])
def update():
    info = request.get_data()
    info = json.loads(info)
    sql = 'replace into server (id,name,ip, port, user) VALUES(%s, %s, %s, %s, %s);'
    params = (info['id'], info['name'], info['ip'], info['port'], info['user'])
    db.updateByParameters( sql, params )
    return "Success"
@server.route('/insert', methods=['get', 'post'])
def insert():
    info = request.get_data()
    info = json.loads(info)
    sql = 'replace into server (name,ip, port, user) VALUES(%s, %s, %s, %s);'
    params = ( info['name'], info['ip'], info['port'], info['user'])
    db.updateByParameters( sql, params )
    return "Success"
@server.route('/getexcel')
def getexcel():
    curdir = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory( curdir + "/static/", "servers.xlsx", as_attachment=True )
@server.route('/insert_from_excel', methods=['get', 'post'])
def insert_from_excel():
    f = request.files.get('servers')
    ramname = int(time.time() * 1000)
    f.save('/tmp/{0}'.format( ramname ))
    tool_excel.insertFromExcel( '/tmp/{0}'.format( ramname ) )
    return "Success!"
@server.route('/delete_by_id')
def delete_by_id():
    id = int(request.args.get('id'))
    sql = 'delete from server where id = %s'
    db.updateByParameters( sql, (id) )
    return "Servers!"
@server.route('/mutidelete', methods=['get', 'post'])
def mutidelete():
    info = request.get_data()
    info = json.loads(info)
    for oneid in info:
        sql = 'delete from server where id = %s'
        db.updateByParameters(sql, (oneid, ))
    return "Success!"

