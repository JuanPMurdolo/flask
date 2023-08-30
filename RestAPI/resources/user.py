from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256 as sha256
from models.user import UserModel
from schemas import UserSchema
from db import db

blp = Blueprint(
    "user", __name__, description="Operations on users"
)

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(400, message="User already exists.")
        user = UserModel(
            username=user_data["username"],
            password=sha256.hash(user_data["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
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