from flask import Flask
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////prods_datos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
db.create_all()

app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app, 
    version='1.0', title='My Model API',
    description='API para el Modelo de Ciencia de Datos',
)

from models import Prediction

ns = api.namespace('predicciones', description='predicciones')

# =======================================================================================
prediction_repr = api.model('Prediccion', {
    'input': fields.String(description="datos de entrada del modelo"),
    'score': fields.Float(description="score de probabilidad de conversión")
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
    @ns.expect(prediction_repr)
    def post(self):
        prediction = Prediction(representation=api.payload)
        db.session.add(prediction)
        db.session.commit()
        print(prediction)
        response = {
            "url": 'yeah' + '/'+str(prediction.prediction_id),
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
