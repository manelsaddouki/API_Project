from marshmallow import Schema, fields


class PlainDonorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainAffectedSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class PlainFundSchema(Schema):
    id = fields.Int(dump_only=True)
    type = fields.Str(required=True)
    donation = fields.Float(required=True)

class DonorSchema(PlainDonorSchema):
    funds = fields.List(fields.Nested(PlainFundSchema()), dump_only=True)


class DonorUpdateSchema(Schema):
    name = fields.Str()


class AffectedSchema(PlainAffectedSchema):
    funds = fields.List(fields.Nested(PlainFundSchema()), dump_only=True)


class FundSchema(PlainFundSchema):
    affected_id = fields.Int(load_only=True)
    affected = fields.Nested(PlainAffectedSchema(), dump_only=True)
    donors = fields.List(fields.Nested(PlainDonorSchema()), dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True) #load_only=true so we just get it from client, it's never sent to them (try to delete it and the pwd will be returned in the get request (hashed password))
    
class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)
    
class FundAndDonorSchema(Schema):
    message = fields.Str()
    donor = fields.Nested(DonorSchema)
    fund = fields.Nested(FundSchema)