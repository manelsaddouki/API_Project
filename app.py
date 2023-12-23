from flask import Flask, jsonify, render_template
from flask_smorest import Api
import secrets
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from routes import *


from db import db
import os
import models 

from resources.donor import blp as DonorDBBlueprint
from resources.fund import blp as FundDBBlueprint
from resources.affected import blp as AffectedDBBlueprint
from resources.user import blp as UserBlueprint

#function to create new app 
def create_app(db_url=None):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    load_dotenv()

    app.config['STATIC_URL_PATH'] = '/static'
    
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "L&D Funds Committee REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db") #connection to database: in case we have db_url as parameter it uses it, if not it tries to access env variable DATABASE_URL, if it does not exist called sqlite to create our db in data.db file
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app) #initialize sqlachemy extension given our created app so it connect them together
    migrate = Migrate(app, db)
    
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = str(secrets.SystemRandom().getrandbits(128))
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
      return (
         jsonify({"message": "The token has expired.", "error": "token_expired"}), #I cam change the msg and error msg displayed
        401,)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
       return ( jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"} ),401,)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
       return ( jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            } ), 401,)
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
      return (
         jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
        )


    @app.before_request
    def create_table():
        db.create_all()
    

    api.register_blueprint(DonorDBBlueprint)
    api.register_blueprint(AffectedDBBlueprint)
    api.register_blueprint(FundDBBlueprint)
    api.register_blueprint(UserBlueprint)

    return app   

app = create_app()

@app.route("/welcome")
def index():
    return render_template(r'base.html')

                            
