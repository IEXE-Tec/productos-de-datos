import math
from datetime import datetime

from model_api import db


# =======================================================================================
class Prediction(db.Model):
    
    __tablename__ = 'prediction'

    prediction_id = db.Column('id', db.Integer, primary_key=True)
    variable_1 = db.Column('variable_1', db.Text, nullable=False)
    variable_2 = db.Column('variable_2', db.Text, nullable=False)
    variable_3 = db.Column('variable_3', db.Float, nullable=False)
    score = db.Column('score', db.Float, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # -----------------------------------------------------------------------------------
    def __init__(self, representation=None):
        super(Prediction, self).__init__()
        self.variable_1 = representation.get('variable_1')
        self.variable_2 = representation.get('variable_2')
        self.variable_3 = representation.get('variable_3')

    # -----------------------------------------------------------------------------------
    def __repr__(self):
        return '<Prediction [{}]: var1={}, var2={}, var3={}, score={}>'.format(
            str(self.prediction_id) if self.prediction_id else 'NOT COMMITED', 
            self.variable_1, self.variable_2, self.variable_3,
            str(self.score) if self.score is not None else 'No calculado'
        )
