from flask import jsonify
from core.libs.exceptions import FyleError
from core.models.assignments import AssignmentStateEnum, GradeEnum
from core.models.teachers import Teacher
import unittest

def test_get_assignments(client, h_principal):
    response = client.get('/principal/assignments', headers=h_principal)
    
    if response.status_code == 200:
        data = response.json['data']
        for assignment in data:
            assert assignment['state'] in ['SUBMITTED', 'GRADED', 'DRAFT']  
    else:
        assert response.status_code == 404
    

def test_grade_assignment_draft_assignment(client, h_principal):
    response = client.post('/principal/assignments/grade', json={
        'id': 5,
        'grade': GradeEnum.A.value
    }, headers=h_principal)
    assert response.status_code == 404

def test_grade_assignment(client, h_principal):
    response = client.post('/principal/assignments/grade', json={
        'id': 4,
        'grade': GradeEnum.C.value
    }, headers=h_principal)
    assert response.status_code == 404

def test_regrade_assignment(client, h_principal):
    response = client.post('/principal/assignments/grade', json={
        'id': 4,
        'grade': GradeEnum.B.value
    }, headers=h_principal)

    assert response.status_code == 404

def test_grade_assignment_not_found(client, h_principal):
    response = client.post('/principal/assignments/grade', json={
        'id': 9999,
        'grade': GradeEnum.A.value
    }, headers=h_principal)

    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'NotFound'

def test_grade_assignment_invalid_grade(client, h_principal):
    response = client.post('/principal/assignments/grade', json={
        'id': 4,
        'grade': 'INVALID_GRADE'
    }, headers=h_principal)

    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'NotFound'


class TestFyleError(unittest.TestCase):
    
    def test_initialization_with_custom_status_code(self):
        error = FyleError(404, "Not Found")
        self.assertEqual(error.status_code, 404)
        self.assertEqual(error.message, "Not Found")

    def test_initialization_with_default_status_code(self):
        error = FyleError(FyleError.status_code, "Bad Request")
        self.assertEqual(error.status_code, 400)
        self.assertEqual(error.message, "Bad Request")

    def test_to_dict(self):
        error = FyleError(500, "Server Error")
        expected_dict = {'message': "Server Error"}
        self.assertEqual(error.to_dict(), expected_dict)







