from marshmallow import Schema, fields, validate

class JobSchema(Schema):
    id = fields.Int(dump_only=True)
    company = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    role = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    status = fields.Str(load_default="applied")
    applied_date = fields.Date(load_default=None)
    notes = fields.Str(load_default=None)