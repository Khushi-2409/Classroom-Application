import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname('core')))

from flask import Blueprint, request, jsonify
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.teachers import Teacher

from core.apis.assignments.schema import AssignmentSchema, AssignmentGradeSchema

principal_resources = Blueprint('principal', __name__)

@principal_resources.route('/teachers', methods=['GET'])
@decorators.authenticate_principal
def get_all_teachers():
    teachers = Teacher.query.all()
    data = [teacher.to_dict() for teacher in teachers]
    return jsonify(data=data), 200
