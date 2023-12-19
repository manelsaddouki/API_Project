from sqlalchemy import ForeignKey
from db import db


class DonorModel(db.Model):
    __tablename__ = "donors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    continent = db.Column (db.String)
    
    funds = db.relationship ("FundModel", back_populates="donors", secondary="funds_donors" ) #secondary the table we created 