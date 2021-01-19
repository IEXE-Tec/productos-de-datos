# =======================================================================================
#                        IEXE Tec - Maestría en Ciencia de Datos
#                                  Productos de Datos
# ---------------------------------------------------------------------------------------
# Este es el script que procesa las llamadas al API REST.
# =======================================================================================
import os
import json

from attr import attributes

from validators import (format_checker, CustomDateTime, GetLeadCategory,
                        GetLeadMetadata)
from flask import Flask, request
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from model import Model
from flask_restx import Resource, fields


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

from models import Lead, Rate, RequestReceived

########################################################################
# Define Response model
########################################################################

lead_display = api.model('Lead', {
    'fecha_registro': CustomDateTime(description="fecha de registro",
                                     attribute='registration_date'),
    'nombre': fields.String(description="nombre completo",
                            max_length=250, attribute='fullname'),
    'telefono': fields.String(description="teléfono",
                              max_length=250, attribute='phone'),
    'id_snl': fields.String(description="identificador de la base de datos "
                                        "de SN", max_length=250),
    'consulta': fields.String(description="texto de consulta",
                              max_length=250, attribute='query'),
    'producto': fields.String(description="producto de interés en la consulta",
                              max_length=250, attribute='product'),
    'campania': fields.String(description="campaña que generó el lead",
                              max_length=24, attribute='campaign'),
    'metadata': GetLeadMetadata(description="datos adicionales"),

})


rate_display = api.model('Rate', {
    'score_conversion': fields.Float(description="score de probabilidad de "
                                                 "conversión",
                                     attribute="conversion_score"),
    'categoria': GetLeadCategory(description='categoría del lead')
})


response_display = api.model('RetrieveResponse', {
    'api_id': fields.String,
    'fecha_consulta': CustomDateTime(description="fecha de petición",
                                     attribute="request_date"),
    'calificacion': fields.Nested(rate_display, attribute="rate"),
    'lead': fields.Nested(lead_display),
})

create_response_display = api.model('CreateResponse', {
    'url': fields.String(description="url de recurso"),
    'api_id': fields.String(description="id de score"),
    'calificacion': fields.Nested(rate_display, attribute="rate"),
})

create_request = api.model('CreateRequest', {
    'version': fields.String(description="version de api"),
    'lead': fields.Nested(lead_display),
})

########################################################################
# Define Routes
########################################################################

health_ns = api.namespace('health_check', description='Check health '
                                                      'connection')


@health_ns.route('/', methods=['GET'])
class HealthCheck(Resource):

    def get(self):
        return "It's fine"


lead_rating_ns = api.namespace(VERSION, description='Lead rating')


@lead_rating_ns.route('/', methods=['POST'])
class CreateLeadRating(Resource):

    # TODO: Activar validate y permitir json dinamico en metadata
    @api.expect(create_request, validate=False)
    @api.marshal_with(create_response_display)
    def post(self):
        data = request.get_json()
        request_r = RequestReceived(request=json.dumps(data))
        db.session.add(request_r)
        db.session.commit()
        score, category = Model.get_rating(data=data)
        new_rate = Rate(
            conversion_score=score,
            category=category)
        db.session.add(new_rate)
        db.session.commit()
        lead = data.get('lead')
        new_lead = Lead(
            registration_date=lead.get('fecha_registro'),
            fullname=lead.get('nombre'),
            phone=lead.get('telefono'),
            query=lead.get('consulta'),
            product=lead.get('producto'),
            campaign=lead.get('campania'),
            extra_data=lead.get('metadata'),
            id_snl=lead.get('id_snl'),
            rate_id=new_rate.id)
        db.session.add(new_lead)
        db.session.commit()
        ################################################################
        response = {
            "url": HOST_URL + VERSION + '/'+str(new_rate.api_id),
            "api_id": str(new_rate.api_id),
            "rate": new_rate
        }
        request_r.processed = True
        db.session.commit()
        return response


@lead_rating_ns.route('/<uuid:api_id>', methods=['GET'])
class LeadRating(Resource):

    @api.marshal_with(response_display)
    def get(self, api_id):
        rate = Rate.query.filter_by(api_id=api_id).first()
        response = {
            "api_id": rate.api_id,
            "request_date": rate.created_dt,
            "rate": rate,
            "lead": rate.lead
        }
        return response
