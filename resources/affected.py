import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import AffectedSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import AffectedModel

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt


blp = Blueprint("Affected Countries", __name__, description="Operations on affected countries")

@blp.route("/affected")
class AffectedList(MethodView):
    @blp.response(200, AffectedSchema(many=True))
    def get(self):
       return AffectedModel.query.all()

    @blp.arguments(AffectedSchema)
    @blp.response(201, AffectedSchema)
    def post(self, affected_data):
      affected = AffectedModel(**affected_data)
      try:
          db.session.add(affected)
          db.session.commit()
      except IntegrityError:
          abort( 400, message="An affected country with that name already exists.")
      except SQLAlchemyError:
          abort(500, message="An error occurred creating the store.")

      return affected


@blp.route("/affected/<string:name>")
class AffectedID (MethodView):
    @blp.response(200, AffectedSchema)
    def get(self, name):
        # Find the AffectedModel by name
        affected = AffectedModel.query.filter_by(name=name).first()

        if affected:
            return {'id': affected.id}
        else:
            return {'message': 'Affected not found'}, 404


@blp.route("/affected/<int:affected_id>")
class Affected (MethodView):
    @blp.response(200, AffectedSchema)
    def get(self, affected_id):
        affected = AffectedModel.query.get_or_404(affected_id)
        return affected

    @jwt_required(fresh=True)
    def delete(self, affected_id):
        affected = AffectedModel.query.get_or_404(affected_id)
        db.session.delete(affected)
        db.session.commit()
        return {"message": "Affected Country deleted"}, 200

