# =======================================================================================
#                        IEXE Tec - Maestría en Ciencia de Datos
#                                  Productos de Datos
# ---------------------------------------------------------------------------------------
# Validadores de datos de entrada del API REST
# =======================================================================================
import re
import json
from datetime import datetime
from jsonschema import FormatChecker
# https://flask-restx.readthedocs.io/en/latest/marshalling.html#custom-fields
from flask_restx import fields

# https://python-jsonschema.readthedocs.io/en/stable/validate/#jsonschema.FormatChecker
format_checker = FormatChecker()


# =======================================================================================
@format_checker.checks("custom_date", ValueError)
def custom_date_check(value):
    """ Valida una fecha dentro del JSON de consulta con un formato específico
        :param value: La fecha a verificar 
    """
    datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    return True


# =======================================================================================
class CustomDateTime(fields.DateTime):
    """ Fecha específica para el API REST
    """
    
    # Propiedades para la documentación REST
    # https://flask-restx.readthedocs.io/en/latest/quickstart.html
    __schema_format__ = "custom_date"
    __schema_example__ = "2019-03-07 15:40:01.000"

    # -----------------------------------------------------------------------------------
    def format(self, value: datetime):
        """ Devuelve la fecha en el mismo formato esperado
        """
        try:
            return datetime.strftime(value, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError as e:
            raise fields.MarshallingError(e)


# =======================================================================================
class GetLeadMetadata(fields.Raw):
    """ Valor adicional en el JSON de consulta con un diccionario libre, de la forma
        llave:valor
    """
    __schema_type__ = "json"
    __schema_example__ = "{'key1': 'value1', 'key2': 2}"

     # -----------------------------------------------------------------------------------
    def output(self, key, obj, ordered=False):
        """ Genera la salida en formato JSON
        """
        return obj.extra_data
