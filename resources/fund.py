from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import FundModel, AffectedModel, DonorModel
from schemas import FundSchema, FundAndDonorSchema

blp = Blueprint("Funds", "fund", description="Operations on funds")


@blp.route("/fund/<int:affected_id>")
class FundsforAffected(MethodView):
    @jwt_required() # require access token 
    @blp.response(200, FundSchema(many=True))
    def get(self, affected_id):
        affected = AffectedModel.query.get_or_404(affected_id)
        return affected.funds.all()

    @jwt_required()
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

        return fund


@blp.route("/funds/<int:fund_id>")
class fund(MethodView):
    @jwt_required()
    @blp.response(200, FundSchema)
    def get(self, fund_id):
        fund = FundModel.query.get_or_404(fund_id)
        return fund
    
    @blp.response(
        202,
        description="Deletes a fund if no donor is linked with it.",
        example={"message": "Donor deleted."},
    )
    @blp.alt_response(404, description="Fund not found.")
    @blp.alt_response(
        400,
        description="Returned if the fund is assigned to one or more donors. In this case, the fund is not deleted.",
    )

    @jwt_required()
    def delete(self, fund_id):
        fund = FundModel.query.get_or_404(fund_id)

        if not fund.donors:
            db.session.delete(fund)
            db.session.commit()
            return {"message": "Fund deleted."}
        abort(
            400,
            message="Could not delete fund. Make sure tag is not associated with any donor, then try again.",
        )
    


@blp.route("/donor/<int:donor_id>/fund/<int:fund_id>")
class LinkFundsToDonors(MethodView):
    @jwt_required()
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
    @jwt_required()
    def delete(self, donor_id, fund_id):
        donor = DonorModel.query.get_or_404(donor_id)
        fund = FundModel.query.get_or_404(fund_id)

        donor.funds.remove(fund)

        try:
            db.session.add(fund)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while removing the link.")

        return {"message": "Fund removed from Donor", "Donor": donor, "Fund": fund}