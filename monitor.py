from flask import Blueprint,render_template,request
import os
import json
monitor = Blueprint("monitor",__name__)
@monitor.route('/')
def home():
    return render_template("monitor.html")
@monitor.route('/info',methods=['GET','POST'])
def info():
    ns = request.form.get('ns')
    os.environ['ns']=str(ns)
    all = os.popen("kubectl get pods -n $ns|sed -n '2,$p'|awk '{print $1,$3}'")
    print(all)
    moni1 = {}
    for i in all:
        list = i.split( )
        server = list[0]
        status = list[1]
        moni1[server] = status
       # print(type(mydict))
      
        #result = "{0}:{1}".format(server,status)
        #result = my_dict.append(result)
    print(moni1)
    #for key, value in moni.items():
    #    print(key,value) 
    #return moni
    #moni1 = {'1':'2','x':'y'}
    #print(type(moni1))
    return render_template('monitor1.html', moni1=moni1)
        
@monitor.route('/cm')
def cm():
    #ns = request.form.get('ns')
    #os.environ['ns']=str(ns)
    all = os.popen("kubectl describe cm config-center-data -n ib-test1|sed -n '/Data/,/Events/p'")
    #return render_template("monitor.html")
    all = all.read()
    print(all)
    print(type(all))
    #a = ' '.join(all)
    a = all.split('\n')
    print(a)
    #cmlist = a.split(' ')
    #print(cmlist)
    #return cmlist
    return render_template('cm.html',a=a)
