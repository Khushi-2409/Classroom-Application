import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname('core')))

from flask import jsonify, request
from marshmallow.exceptions import ValidationError
from core import app
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources
from core.apis.teachers import principal_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
app.register_blueprint(principal_resources, url_prefix='/principal')

# @app.route('/')
# def ready():
#     response = jsonify({
#         'status': 'ready',
#         'time': helpers.get_utc_now()
#     })
#     return response

@app.errorhandler(Exception)
def handle_error(err):
    if isinstance(err, FyleError):
        return jsonify(
            error=err.__class__.__name__, message=err.message
        ), err.status_code
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__, message=str(err.orig)
        ), 400
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__, message=str(err)
        ), err.code
    else:
        return jsonify(
            error='InternalServerError', message='An unexpected error occurred'
        ), 500
