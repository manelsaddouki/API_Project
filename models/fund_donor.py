from db import db


class FundDonors(db.Model):
    __tablename__ = "funds_donors"

    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey("donors.id"))
    fund_id = db.Column(db.Integer, db.ForeignKey("funds.id"))