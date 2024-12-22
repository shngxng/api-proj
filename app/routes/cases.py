from app.services.case_service import CaseService
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from flask_restx import Namespace,Resource,fields

case_ns=Namespace('therapy', description="Namespace for therapy cases")

add_case_model = case_ns.model('Add Case', {
    'name': fields.String(required=True, description='The name of patient'),
    'description': fields.String(required=True, description='The description of the therapy case')
})

# Fetch the list of all cases.
@case_ns.route('/cases')
class CaseList(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return CaseService.get_all_cases()
    
# Adds a case.
@case_ns.route('/case')
class AddCase(Resource):
    @case_ns.expect(add_case_model)
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        data = case_ns.payload
        name = data.get('name')
        desc = data.get('description')
        return CaseService.add_case(name, desc)
    