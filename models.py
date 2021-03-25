
from sqlalchemy.dialects.postgresql import UUID, JSON

from model_api import db


# =======================================================================================
class Prediction(db.Model):
    
    __tablename__ = 'prediction'

    prediction_id = db.Column('id', db.Integer, primary_key=True)
    prediction_input = db.Column('input', db.Text, nullable=False)
    score = db.Column('score', db.Float, nullable=False)

    # -----------------------------------------------------------------------------------
    def __init__(self, representation=None):
        super(Prediction, self).__init__()
        self.prediction_input = representation.get('input')
        self.score = representation.get('score')

    # -----------------------------------------------------------------------------------
    def __repr__(self):
        return '<Prediction %r: %r>' % (self.prediction_input, self.score)
