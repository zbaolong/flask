from flask import Blueprint,render_template,request,send_from_directory
from werkzeug.utils import secure_filename
import os
upload = Blueprint("upload",__name__)
@upload.route('/up/',methods=['GET','POST'])
def up():
    if request.method == 'GET':
        return render_template("upload.html")
    else:
        file = request.files.get('file')
        filename = file.filename
        filename = secure_filename(filename)
        file.save('/tmp/{0}'.format(filename))
        return 'upload success'
@upload.route('/down/')
def down():
    print(os.path.realpath(__file__))
    print(os.path.dirname(os.path.realpath(__file__)))
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory(cur_dir+"/static","info.xlsx",as_attachment=True)
