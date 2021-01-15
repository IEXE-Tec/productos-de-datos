import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSON
from app import db


class BaseModel:
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4,
                       unique=True, nullable=False)


class Rate(db.Model, BaseModel):
    __tablename__ = 'rate'

    conversion_score = db.Column(db.Float, nullable=True)
    category = db.Column(db.String(2), nullable=True)
    created_dt = db.Column(db.DateTime(), default=datetime.utcnow)
    lead = db.relationship('Lead', lazy='select', uselist=False, 
                           backref=db.backref('lead', lazy='joined'))

    def __init__(self, conversion_score=None, category=None):
        self.conversion_score = conversion_score
        self.category = category

    def __repr__(self):
        return f"<Rate {self.id}>"


class Lead(db.Model, BaseModel):
    __tablename__ = 'lead'
    registration_date = db.Column(db.DateTime())
    fullname = db.Column(db.String(250))
    phone = db.Column(db.String(250))
    query = db.Column(db.String(250))
    product = db.Column(db.String(250))
    campaign = db.Column(db.String(250))
    extra_data = db.Column(JSON)
    id_snl = db.Column(db.String(24), nullable=True)
    rate_id = db.Column(db.Integer, db.ForeignKey('rate.id'),
                        nullable=False)

    def __init__(self, registration_date=None, fullname=None, phone=None,
                 product=None, campaign=None, extra_data=None, query=None,
                 id_snl=None, rate_id=None):
        self.registration_date = registration_date
        self.fullname = fullname
        self.phone = phone
        self.product = product
        self.campaign = campaign
        self.extra_data = extra_data
        self.query = query
        self.id_snl = id_snl
        self.rate_id = rate_id

    def __repr__(self):
        return f"<Lead {self.fullname}>"


class RequestReceived(db.Model, BaseModel):
    __tablename__ = 'request'

    processed = db.Column(db.Boolean, nullable=False, default=False)
    request = db.Column(db.Text, nullable=False)

    def __init__(self, processed=None, request=None):
        self.processed = processed
        self.request = request

    def __repr__(self):
        return f"<Request {self.id}>"
