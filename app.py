# =======================================================================================
#                        IEXE Tec - Maestría en Ciencia de Datos
#                                  Productos de Datos
# ---------------------------------------------------------------------------------------
# Este es el script que procesa las llamadas al API REST.
# =======================================================================================
import os
import json

from attr import attributes
from validators import (
    format_checker, CustomDateTime, GetLeadCategory,GetResourceMetadata)
from flask import Flask, request
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restx import Resource, fields

from models import PredictionScore, PredictionRequest
from model import Model
from config import Config


# =======================================================================================
# Definición de objetos y variables de configuración de la aplicación
# ---------------------------------------------------------------------------------------
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Puedes cambiar el título del API
api = Api(app, version='1.0', title='Productos de Datos', format_checker=format_checker)
app.config.from_object(Config)

# SQL Alchemy es una biblioteca para crear objetos que interactuan con la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

HOST_URL = os.environ['HOST_URL']
VERSION = 'v1'

# =======================================================================================
# Configuración del JSON de intercambio en el API REST.
# https://flask-restx.readthedocs.io/en/latest/marshalling.html#basic-usage
#
# Aqui declaras los recursos del API REST. Los nombres de sus propiedades y sus tipos 
#
# Datos de consulta al modelo
lead_display = api.model('Lead', {
    'client_name': fields.String(description="nombre completo", max_length=250, attribute='client_name'),
    'metadata': GetResourceMetadata(description="datos adicionales"),

})

# Datos del resultado del modelo
rate_display = api.model('PredictionScore', {
    'score': fields.Float(description="score del modelo predicitivo", attribute="score")
})

# Respuesta integrada de un resultado
response_display = api.model('RetrieveResponse', {
    'api_id': fields.String,
    'fecha_consulta': CustomDateTime(description="fecha de petición",
                                     attribute="request_date"),
    'calificacion': fields.Nested(rate_display, attribute="rate"),
    'lead': fields.Nested(lead_display),
})

# Crea aquí los demás recursos que vas a necesitar en tu API REST


# =======================================================================================
# Definición de Rutas del API REST
#
# ---------------------------------------------------------------------------------------
health_ns = api.namespace('health_check', description='Check health connection')
@health_ns.route('/', methods=['GET'])
class HealthCheck(Resource):
    """ Ruta necesaria para el funcionamiento del motor de Swagger
    """
    def get(self):
        return "It's fine"


# ---------------------------------------------------------------------------------------
lead_rating_ns = api.namespace(VERSION, description='Solicitud de modelo')
@lead_rating_ns.route('/', methods=['POST'])
class CreatePrediction(Resource):
    """ Recurso REST que contiene la llamada al modelo predictivo
    """

    @api.expect(create_request, validate=False)
    @api.marshal_with(create_response_display)
    def post(self):
        """ Aquí debes de invocar al modelo predictivo, crear los objetos necesarios y
            guardarlos en la base de datos.
            Además debes de construir una respuesta y devolverla como resultado
        """
        return None


# ---------------------------------------------------------------------------------------
@lead_rating_ns.route('/<uuid:api_id>', methods=['GET'])
class LeadRating(Resource):
    """ Recurso REST para procesar solicitudes históricas del modelo
    """

    @api.marshal_with(response_display)
    def get(self, api_id):
        """ Procesa aquí la solicitud a una llamada histórica y devuelve su resultado
        """
        return None
