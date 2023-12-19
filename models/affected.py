from db import db


class AffectedModel(db.Model):
    __tablename__ = "affected"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    funds = db.relationship("FundModel", back_populates="affected", lazy="dynamic", cascade="all, delete") # back populate matches the db.relationship in FundModel