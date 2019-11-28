from flask_ckeditor import CKEditor
from forms import RichTextForm

ckeditor = CKEditor(app)
app.config['CKEDITOR_SERVE_LOCAL'] = True

@app.route('/ckeditor')
def ckeditor():
    form = RichTextForm()
    return render_template('ckeditor.html',form = form)
