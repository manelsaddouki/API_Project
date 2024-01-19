from flask.views import MethodView
from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort

from db import db

from sqlalchemy.exc import SQLAlchemyError
from models import FundModel, AffectedModel, DonorModel
from schemas import FundSchema, FundAndDonorSchema, FundUpdateSchema

blp = Blueprint("Funds", "fund", description="Operations on funds")


@blp.route("/funds")
class AffectedList(MethodView):
    @blp.response(200, FundSchema(many=True))
    def get(self):
       return FundModel.query.all()

@blp.route("/fund/<int:affected_id>")
class FundsforAffected(MethodView):
    #@jwt_required()
    @blp.response(200, FundSchema(many=True))
    def get(self, affected_id):
        affected = AffectedModel.query.get_or_404(affected_id)
        return affected.funds.all()

    #@jwt_required()
    @blp.arguments(FundSchema)
    @blp.response(201, FundSchema)
    def post(self, fund_data, affected_id):

        fund = FundModel(**fund_data, affected_id=affected_id)

        try:
            db.session.add(fund)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return  {"id": fund.id}
    


@blp.route("/donor/<int:donor_id>/fund/<int:fund_id>")
class LinkFundsToDonors(MethodView):
    #@jwt_required()
    @blp.response(201, FundSchema)
    def post(self, donor_id, fund_id): #this is to link exisiting donor and fund
        donor = DonorModel.query.get_or_404(donor_id)
        fund = FundModel.query.get_or_404(fund_id)

        donor.funds.append(fund)

        try:
            db.session.add(donor)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the fund.")

        return fund

    @blp.response(200, FundAndDonorSchema)
    @jwt_required(fresh=True)
    def delete(self, donor_id, fund_id):
        donor = DonorModel.query.get_or_404(donor_id)
        fund = FundModel.query.get_or_404(fund_id)

        donor.funds.remove(fund)

        try:
            db.session.add(fund)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error.")

        return {"message": "Fund removed from Donor", "Donor": donor, "Fund": fund}


@blp.route("/funds/<int:fund_id>")
class fund(MethodView):
    @jwt_required()
    @blp.response(200, FundSchema)
    def get(self, fund_id):
        fund = FundModel.query.get_or_404(fund_id)
        return fund

    @jwt_required(fresh=True)
    def delete(self, fund_id):
        fund = FundModel.query.get_or_404(fund_id)

        if fund:
            db.session.delete(fund)
            db.session.commit()
            return {"message": "Fund deleted."}
        abort(
            400,
            message="Could not delete fund.",
        )

@blp.route("/fundtype/<int:fund_id>")
class updatefund(MethodView):
   @blp.arguments(FundUpdateSchema(partial=True))  # Use partial schema for partial updates
   @blp.response(200, FundSchema)
   def patch(self, data, fund_id):
        fund = FundModel.query.get_or_404(fund_id)
        key_value = request.args.get('type')
        print (key_value) 
        if key_value:
            fund.type = key_value
            db.session.commit()
            print ("fund type updated successfully")
        else:
             return {"error": "Missing 'continent' in query parameters"}, 400

        