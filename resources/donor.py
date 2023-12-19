import uuid
from flask_jwt_extended import jwt_required
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import DonorSchema, DonorUpdateSchema

from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import DonorModel

blp = Blueprint("Donors", __name__, description="Operations on donors")


@blp.route("/donor/<int:donor_id>")
class Donor(MethodView):
    #@jwt_required() # require access token 
    @blp.response(200, DonorSchema)
    def get(self, donor_id):
        donor = DonorModel.query.get_or_404(donor_id)
        return donor

    #@jwt_required()
    def delete(self, donor_id):
        donor = DonorModel.query.get_or_404(donor_id)
        db.session.delete(donor)
        db.session.commit()
        return {"message": "Donor deleted."}

    #@jwt_required()
    @blp.arguments(DonorUpdateSchema)
    @blp.response(200, DonorSchema)
    def put(self, donor_data, donor_id):
        donor = DonorModel.query.get_or_404(donor_id)
        raise NotImplementedError("Updating a donor is not implemented.")

@blp.route("/donor")
class DonorList(MethodView):
    #@jwt_required()
    @blp.response(200, DonorSchema(many=True))
    def get(self):
       return DonorModel.query.all()

    #@jwt_required()
    @blp.arguments(DonorSchema)
    @blp.response(201, DonorSchema)
    def post(self, donor_data):
       donor = DonorModel(**donor_data)
        
       db.session.add(donor)
       db.session.commit()

       return donor