from flask import Blueprint
long = Blueprint("long",__name__)
@long.route('/')
def index():
    return "long is bule"
@long.route('/xxx')
def xxx():
    return "xxx is bule"

