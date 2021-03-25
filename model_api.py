import os
import random

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
db_uri = 'sqlite:///{}/prods_datos.db'.format(os.path.dirname(__file__))
print(db_uri)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app, 
    version='1.0', title='My Model API',
    description='API para el Modelo de Ciencia de Datos',
)
ns = api.namespace('predicciones', description='predicciones')

from models import Prediction
db.create_all()

# =======================================================================================
observacion_repr = api.model('Observacion', {
    'variable_1': fields.String(description="Una variable de entrada"),
    'variable_2': fields.String(description="Una variable de entrada"),
    'variable_3': fields.Float(description="Una variable de entrada")
})

# =======================================================================================
prediction_repr = api.model('Prediccion', {
    'variable_1': fields.String(description="Una variable de entrada"),
    'variable_2': fields.String(description="Una variable de entrada"),
    'variable_3': fields.Float(description="Una variable de entrada"),
    'score': fields.Float(description="Resultado del modelo predicitivo")
})


# =======================================================================================
@ns.route('/', methods=['GET', 'POST'])
class PredictionListAPI(Resource):
    """
    """

    # -----------------------------------------------------------------------------------
    def get(self):
        return [
            marshall_prediction(prediction) for prediction in Prediction.query.all()
        ], 200

    # -----------------------------------------------------------------------------------
    @ns.expect(observacion_repr)
    def post(self):
        prediction = Prediction(representation=api.payload)
        # Aqui llama a tu modelo
        prediction.score = trunc(random.random(), 3)
        db.session.add(prediction)
        db.session.commit()
        response_url = api.url_for(PredictionAPI, prediction_id=prediction.prediction_id)
        response = {
            "score": prediction.score,
            "url": f'{api.base_url[:-1]}{response_url}',
            "api_id": prediction.prediction_id
        }
        return response, 201

# =======================================================================================
@ns.route('/<int:prediction_id>', methods=['GET'])
class PredictionAPI(Resource):
    """
    """

    # -----------------------------------------------------------------------------------
    @ns.doc({'prediction_id': 'Identificador de la predicción'})
    def get(self, prediction_id):
        prediction = Prediction.query.filter_by(prediction_id=prediction_id).first()
        if not prediction:
            return 'Id {} no existe en la base de datos'.format(prediction_id), 404
        else:
            return marshall_prediction(prediction), 200


# =======================================================================================
def marshall_prediction(prediction):
    """
    """
    response_url = api.url_for(PredictionAPI, prediction_id=prediction.prediction_id)
    model_data = {
        'variable_1': prediction.variable_1,
        'variable_2': prediction.variable_2,
        'variable_3': prediction.variable_3,
        "score": prediction.score
    }
    response = {
        "api_id": prediction.prediction_id,
        "url": f'{api.base_url[:-1]}{response_url}',
        "created_date": prediction.created_date.isoformat(),
        "prediction": model_data
    }
    return response

# ---------------------------------------------------------------------------------------
def trunc(number, digits):
    """
    """
    import math
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper
    