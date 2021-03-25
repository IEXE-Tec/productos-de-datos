import os

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

from models import Prediction

db.create_all()

ns = api.namespace('predicciones', description='predicciones')

# =======================================================================================
observacion_repr = api.model('Observacion', {
    'variable_1': fields.String(description="Una variable de entrada"),
    'variable_2': fields.String(description="Una variable de entrada"),
    'variable_3': fields.Float(description="Una variable de entrada"),
})


# =======================================================================================
@ns.route('/', methods=['GET', 'POST'])
class PredictionListAPI(Resource):
    """
    """

    # -----------------------------------------------------------------------------------
    @ns.doc('list_preds')
    #@ns.marshal_list_with(prediction_repr)
    def get(self):
        return '', 200

    # -----------------------------------------------------------------------------------
    #@ns.doc('list_preds')
    #@ns.marshal_list_with(prediction_repr)
    @ns.expect(observacion_repr)
    def post(self):
        prediction = Prediction(representation=api.payload)
        # Aqui llama a tu modelo
        prediction.score = 0.99
        print(prediction)
        db.session.add(prediction)
        db.session.commit()
        response_url = api.url_for(PredictionAPI, prediction_id=prediction.prediction_id)
        response = {
            "score": prediction.score,
            "url": f'{api.base_url[:-1]}{response_url}',
            "api_id": str(prediction.prediction_id)
        }
        return response, 200

# =======================================================================================
@ns.route('/<int:prediction_id>', methods=['GET'])
class PredictionAPI(Resource):
    """
    """

    # -----------------------------------------------------------------------------------
    def get(self):
        return '=)', 200
