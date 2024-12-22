from app.services.user_service import UserService
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify

# auth_bp = Blueprint('auth', __name__, url_prefix='/')

auth_ns = Namespace('auth', description='Authentication operations')
auth_model = auth_ns.model('Login/Register', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password')
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(auth_model)
    def post(self):
        data = auth_ns.payload 
        username = data.get('username')
        password = data.get('password')
        response, status = UserService.register_user(username, password)
        if status == 201:
            access_token = create_access_token(identity=username)
            return {"message": response["message"], "access_token": access_token}, 201
        return response, status
        # return UserService.register_user(username, password) 

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(auth_model)
    def post(self):
        data = auth_ns.payload
        username = data.get('username')
        password = data.get('password')
        response, status = UserService.login_user(username, password)
        if status == 200:
            access_token = create_access_token(identity=username)
            return {"message": response["message"], "access_token": access_token}, 200
        return response, status
        # return UserService.login_user(username, password)
    

@auth_ns.route('/promote')
class Promote(Resource):
    @auth_ns.expect(auth_model)
    @auth_ns.doc(security="Bearer Auth") 
    @jwt_required() 
    def post(self):
        user = get_jwt_identity() 
        current_user=User.query.filter_by(username=user).first()
        data = auth_ns.payload  
        username = data.get('username')
        password = data.get('password')
        return UserService.promote_user(username, password)

@auth_ns.route('/demote')
class Demote(Resource):
    @auth_ns.expect(auth_model)
    @auth_ns.doc(security="Bearer Auth")
    @jwt_required() 
    def post(self):
        current_user = get_jwt_identity() 
        data = auth_ns.payload
        username = data.get('username')
        password = data.get('password')
        return UserService.demote_user(username, password)
    
    