from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256 #this is to hash the password of the client (transform it into unreadible msg)
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt

from db import db
from models import UserModel
from schemas import UserSchema, UserRegisterSchema
import requests 
import os 
from sqlalchemy import or_


blp = Blueprint("Users", "users", description="Operations on users")


def send_confirmation_email(to, subject, body):
    domain = os.getenv("MAILGUN_DOMAIN")
    return requests.post(
        f"https://api.mailgun.net/v3/sandbox80ba84e27fea4b139f31fed5120e3997.mailgun.org/messages",
        auth=("api", "956d0e2f11c1ff102a21063c45fd7245-5e3f36f5-5fa86440"),
        data={
            "from": f"Loss and Damage Funds Committee <mailgun@sandbox80ba84e27fea4b139f31fed5120e3997.mailgun.org>",
            "to": [to],
            "subject": subject,
            "text": body,
        },
    )


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"]
            )
        ).first(): 
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=user_data["username"], # user_data["username"] the one the user enters
            password=pbkdf2_sha256.hash(user_data["password"]),
            email=user_data["email"],
        )
        db.session.add(user)
        db.session.commit()

        send_confirmation_email(
            to=user.email,
            subject="Successfully signed up",
            body=f" {user.username}! You have successfully signed up."
        )

        return {"message": "User created successfully."}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):  #this verfies that user exist plus it verifies the password
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")

@blp.route("/refreshtoken")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False) # it will create new access token (token marked as non-fresh)
        return {"access_token": new_token}, 200        


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
    
@blp.route("/users")
class UsersList(MethodView):
    #@jwt_required()
    @blp.response(200, UserRegisterSchema(many=True))
    def get(self):
       return UserModel.query.all()