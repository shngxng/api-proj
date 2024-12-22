from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db


class UserService:
    @staticmethod
    def register_user(username, password):
        if User.query.filter_by(username=username).first():
            return {"message": "User already exists!"}, 400
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256").encode('utf-8')
        user = User(username=username, password=hashed_password, role='Junior')
        db.session.add(user)
        db.session.commit()
        return {"message": "User registered successfully"}, 201
    
    @staticmethod
    def login_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password.decode('utf-8'), password):  
            return {"message": f"Welcome, {user.first_name}. You are appointed as a {user.role}."}, 200
        return {"message": "Invalid credentials."}, 401

    # promote clinicians to Senior role
    @staticmethod
    def promote_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password.decode('utf-8'), password):  
            if user.role == 'Senior':
                return {"message": f"{user.first_name} is already a Senior."}
            user.role = 'Senior'
            db.session.commit()
            return {"message": f"{user.first_name} has been promoted to Senior."}
        return {"message": "User not found."}, 404
    
    # demote clinicians to Junior role
    @staticmethod
    def demote_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password.decode('utf-8'), password):  
            if user.role == 'Junior':
                return {"message": f"{user.first_name} is already a Junior."}
            user.role = 'Junior'
            db.session.commit()
            return {"message": f"{user.first_name} has been demoted to Junior."}
        return {"message": "User not found."}, 404
