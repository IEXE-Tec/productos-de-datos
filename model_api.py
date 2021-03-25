# =======================================================================================
#                       IEXE Tec - Maestría en Ciencia de Datos 
#                       Productos de Datos. Proyecto Integrador
# =======================================================================================
import os
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

# ---------------------------------------------------------------------------------------
#                       Configuración del proyecto
# Se usa la biblioteca Flask-RESTX para convertir la aplicación web en un API REST.
# Consulta la documentación de la biblioteca aquí: https://flask-restx.readthedocs.io/en/latest/quickstart.html
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# El manejador de base de datos será SQLite (https://www.sqlite.org/index.html)
# Flask crea automáticamente un archivo llamado "prods_datos.db" en el directorio local
# *** IMPORTANTE: Si modificas los modelos de la base de datos es necesario que elimines
#     el archivo "prods_datos.db", para que Flask genere las nuevas tablas con los cambios
db_uri = 'sqlite:///{}/prods_datos.db'.format(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# La biblioteca SQLAlchemy permite modelar las tablas de la base de datos como objetos
# de Python. SQLAlchemy se encarga de hacer las consultas necesarias sin necesidad de
# escribir SQL. Consulta la documentación de SQLAlchemy aquí: https://www.sqlalchemy.org/
# Esta biblioteca te permite cambiar muy fácilmente de manejador de base de datos, puedes
# usar MySQL o Postgres sin tener que cambiar el código de la aplicación
db = SQLAlchemy(app)
db.init_app(app)

# El objeto "api" nos permite acceder a las funcionalidades de Flask-RESTX para la
# implementación de un API REST. Cambia el título y la descripción del proeyecto por uno
# más acorde a lo que hace tu modelo predictivo.
api = Api(
    app, 
    version='1.0', title='API REST',
    description='API REST para el Modelo de Ciencia de Datos',
)

# Los espacios de nombre o namespaces permiten estructurar el API REST según los distintos
# recursos que exponga el API. Para este proyecto se usa sólo un namespace de nombre
# "predicciones". Es un recurso genérico para crear este ejemplo. Cambia el nombre del
# espacio de nombres por uno más acorde a tu proyecto. 
# Consulta la documentación de los espacios de nombre aquí: https://flask-restx.readthedocs.io/en/latest/scaling.html
ns = api.namespace('predicciones', description='predicciones')

# Para evitar una referencia circular en las dependencias del código, los modelos que
# interactúan con la base de datos se importan hasta el final de la configuración del
# proyecto. 
# Consulta el script "models.py" para conocer y modificar los mapeos de tablas en la 
# base de datos.
from models import Prediction
db.create_all()

# =======================================================================================
observacion_repr = api.model('Observacion', {
    'variable_1': fields.String(description="Una variable de entrada"),
    'variable_2': fields.String(description="Una variable de entrada"),
    'variable_3': fields.Float(description="Una variable de entrada")
})

# ---------------------------------------------------------------------------------------
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
    