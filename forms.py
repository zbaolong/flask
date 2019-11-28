from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,TextAreaField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

class RichTextForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(1,50)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Publish')
