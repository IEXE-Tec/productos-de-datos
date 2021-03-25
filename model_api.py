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
# El siguiente objeto modela un Recurso REST con los datos de entrada para crear una 
# predicción. Para este ejemplo una observación tiene el nombre genérico "Observacion" 
# con tres variables. Reemplaza el nombre del objeto por uno más apropiado para el
# objetivo de tu modelo, además reemplaza las variables y agrega las que sean necesarias
# para recibir los datos de una observación para que la pueda procesar tu modelo. 
observacion_repr = api.model('Observacion', {
    'variable_1': fields.String(description="Una variable de entrada"),
    'variable_2': fields.String(description="Una variable de entrada"),
    'variable_3': fields.Float(description="Una variable de entrada")
})


# =======================================================================================
# Las siguientes clases modelan las solicitudes REST al API. Usamos el objeto del espacio
# de nombres "ns" para que RESTX comprenda que estas clases y métodos son los manejadores
# del API REST. 

# La siguiente línea indica que esta clase va a manejar los recursos que se encuentran en
# el URI raíz (/), y que soporta los métodos GET y POST.
@ns.route('/', methods=['GET', 'POST'])
class PredictionListAPI(Resource):
    """ Manejador del listado de predicciones.
        GET devuelve la lista de predicciones históricas
        POST agrega una nueva predicción a la lista de predicciones
    """

    # -----------------------------------------------------------------------------------
    def get(self):
        """ Maneja la solicitud GET del listado de predicciones
        """
        # La función "marshall_prediction" convierte un objeto de la base de datos de tipo
        # Prediccion en su representación en JSON.
        # Prediction.query.all() obtiene un listado de todas las predicciones de la base
        # de datos. Internamente ejecuta un "SELECT * FROM predicciones".
        # Consulta el script models.py para conocer más de este mapeo.
        # Además, consulta la documentación de SQL Alchemy para conocer los métodos 
        # disponibles para consultar la base de datos desde los modelos de Python.
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#querying-records
        return [
            marshall_prediction(prediction) for prediction in Prediction.query.all()
        ], 200

    # -----------------------------------------------------------------------------------
    # La siguiente línea de código sirve para asegurar que el método POST recibe un
    # recurso representado por la observación descrita arriba (observacion_repr).
    @ns.expect(observacion_repr)
    def post(self):
        """ Procesa un nuevo recurso para que se agregue a la lista de predicciones
        """

        # La siguiente línea convierte una representación REST de una Prediccion en
        # un Objeto Prediccion mapeado en la base de datos mediante SQL Alchemy
        prediction = Prediction(representation=api.payload)

        # ---------------------------------------------------------------------
        # Aqui llama a tu modelo predictivo para crear un score o una inferencia
        # o el nombre del valor que devuelve el modelo. Para fines de este
        # ejemplo simplemente se calcula un valor aleatorio.        
        prediction.score = trunc(random.random(), 3)
        # ---------------------------------------------------------------------

        # Las siguientes dos líneas de código insertan la predicción a la base
        # de datos mediante la biblioteca SQL Alchemy.
        db.session.add(prediction)
        db.session.commit()

        # Las siguientes líneas son para devolver los datos de la nueva prediccion
        response_url = api.url_for(PredictionAPI, prediction_id=prediction.prediction_id)
        response = {
            "score": prediction.score,  # el score que generó el modelo
            "url": f'{api.base_url[:-1]}{response_url}',  # el URL de esta predicción
            "api_id": prediction.prediction_id  # El identificador de la base de datos
        }

        # La siguiente línea devuelve la respuesta a la solicitud POST con los datos
        # de la nueva predicción, acompañados del código HTTP 201: Created
        return response, 201

# =======================================================================================
# La siguiente línea de código maneja las solicitudes GET del listado de predicciones 
# acompañadas de un identificador de predicción, para obtener los datos de una particular
# Si el API permite modificar predicciones particulares, aquí se debería de manejar el
# método PUT o PATCH para una predicción en particular.
@ns.route('/<int:prediction_id>', methods=['GET'])
class PredictionAPI(Resource):
    """ Manejador de una predicción particular
    """

    # -----------------------------------------------------------------------------------
    @ns.doc({'prediction_id': 'Identificador de la predicción'})
    def get(self, prediction_id):
        """ Procesa las solicitudes GET de una predicción particular
            :param prediction_id: El identificador de la predicción a buscar
        """

        # Usamos la clase Prediction que mapea la tabla en la base de datos para buscar
        # la predicción que tiene el identificador que se usó como parámetro de esta
        # solicitud. Si no existe entonces se devuelve un mensaje de error 404 No encontrado
        prediction = Prediction.query.filter_by(prediction_id=prediction_id).first()
        if not prediction:
            return 'Id {} no existe en la base de datos'.format(prediction_id), 404
        else:
            # Se usa la función "marshall_prediction" para convertir la predicción de la
            # base de datos a un recurso REST
            return marshall_prediction(prediction), 200


# =======================================================================================
def marshall_prediction(prediction):
    """ Función utilería para transofmrar una Predicción de la base de datos a una 
        representación de un recurso REST.
        :param prediction: La predicción a transformar
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
    """ Función utilería para truncar un número a un número de dígitos
    """
    import math
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper
    