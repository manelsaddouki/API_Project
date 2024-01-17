import uuid

from flask import request, make_response
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from models import DonorModel
from schemas import DonorSchema, DonorUpdateSchema, DonorContinentSchema
from db import db

from sqlalchemy.exc import SQLAlchemyError
import jsonpatch


blp = Blueprint("Donors", __name__, description="Operations on donors")

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
        if DonorModel.query.filter( DonorModel.name == donor_data["name"] ).first(): 
            abort(409, message="Country already exists in the donors list.") 

        donor = DonorModel(**donor_data)
        
        db.session.add(donor)
        db.session.commit()

        return donor


@blp.route("/donor/<string:name>")
class DonorID (MethodView):
    @blp.response(200, DonorSchema)
    def get(self, name):
        # Find the DonorModel by name
        donor = DonorModel.query.filter_by(name=name).first()

        if donor:
            return {'id': donor.id}
        else:
            return {'message': 'donor not found'}, 404
        
    @blp.response(200)
    def head(self, name):
        # Check if a donor with the given name exists
        donor = DonorModel.query.filter_by(name=name).first()

        if donor:
            # Create a response with headers
            response = make_response()
            response.headers['Content-Type'] = 'application/json'
            response.headers['Donor-ID'] = str(donor.id)
            return response
        else:
            return {'message': 'donor not found'}, 404


@blp.route("/donor/<int:donor_id>")
class Donor(MethodView):
    #@jwt_required() 
    @blp.response(200, DonorSchema)
    def get(self, donor_id):
        donor = DonorModel.query.get_or_404(donor_id)
        return donor

    @jwt_required(fresh=True)
    def delete(self, donor_id):
        donor = DonorModel.query.get_or_404(donor_id)
        db.session.delete(donor)
        db.session.commit()
        return {"message": "Donor deleted."}

    @blp.arguments(DonorUpdateSchema)
    @blp.response(200, DonorSchema)
    def put(self, donor_data, donor_id):
        donor = DonorModel.query.get_or_404(donor_id)
        raise NotImplementedError("Update not done.")

@blp.route("/UpdateContinent/<int:donor_id>", methods=['PATCH'])
class updatefund(MethodView):
   @blp.arguments(DonorContinentSchema(partial=True))  # Use partial schema for partial updates
   @blp.response(200, DonorSchema)
   def patch(self, data, donor_id):
        donor = DonorModel.query.get_or_404(donor_id)
        key_value = request.args.get('continent')
        print (key_value) 
        if key_value:
            donor.continent = key_value
            db.session.commit()
            print ("fund type updated successfully")
        else:
             return {"error": "Missing 'continent' in query parameters"}, 400
