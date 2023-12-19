from db import db


class FundModel(db.Model):
    __tablename__ = "funds"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), unique=False, nullable=False)
    donation = db.Column(db.Float(precision=2), unique=False, nullable=False)

    affected_id = db.Column(db.Integer, db.ForeignKey("affected.id"), nullable=False)
    affected = db.relationship("AffectedModel", back_populates="funds")
    
    donors = db.relationship ("DonorModel", back_populates="funds", secondary="funds_donors" ) #secondary the table we created 