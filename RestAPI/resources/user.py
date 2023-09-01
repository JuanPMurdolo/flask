import os
import requests
from flask import current_app
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from passlib.hash import pbkdf2_sha256 as sha256
from RestAPI.schemas import UserRegisterSchema
from models.user import UserModel
from schemas import UserSchema
from db import db
from blocklist import BLOCKLIST
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity,  create_refresh_token
from tasks import send_registration_email

blp = Blueprint(
    "user", __name__, description="Operations on users"
)

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(UserModel.username == user_data["username"],
                UserModel.email == user_data["email"])).first():
            abort(400, message="User already exists.")
        user = UserModel(
            username=user_data["username"],
            email = user_data["email"],
            password=sha256.hash(user_data["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
            #current_app.queue.enqueue(send_registration_email, user)

        except SQLAlchemyError:
            abort(500, message="Internal server error.")

        return {"message": "User created successfully."}
    
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id: int):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id: int):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted."}
        except SQLAlchemyError:
            abort(500, message="Internal server error.")

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if user and sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        else:
            abort(401, message="Invalid username or password.")

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "User logged out."}
    
@blp.route("/refresh")
class UserRefresh(MethodView):
    @jwt_required(refresh=True)
    @blp.response(200, UserSchema)
    def post(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": access_token}