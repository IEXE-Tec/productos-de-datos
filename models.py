# =======================================================================================
#                       IEXE Tec - Maestría en Ciencia de Datos 
#                       Productos de Datos. Proyecto Integrador
# =======================================================================================
import math
from datetime import datetime
from model_api import db


# =======================================================================================
# Esta clase mapea una predicción a una tabla en la base de datos mediante la biblioteca
# SQL Alchemy. Consulta la documentación de SQL Alchemy aquí:
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# Modifica el nombre de esta clase para que sea más acorde a lo que hace tu modelo
# predictivo.
#
# ** IMPORTANTE: ** Cualquier modificación a las bases de datos requiere eliminar el
#       archivo de SQLite3 para que SQL Alchemy pueda reconstruir la base de datos
class Prediction(db.Model):
    """ Una predicción en la base de datos.
    """
    __tablename__ = 'prediction'  # Nombre de la tabla en la base de datos

    # Declaración de columnas de la tabla. Modifica estas propiedades para que sean
    # más acorde a las variables que componen una observación de tu modelo.
    prediction_id = db.Column('id', db.Integer, primary_key=True)
    variable_1 = db.Column('variable_1', db.Text, nullable=False)
    variable_2 = db.Column('variable_2', db.Text, nullable=False)
    variable_3 = db.Column('variable_3', db.Float, nullable=False)
    score = db.Column('score', db.Float, nullable=False)
    # El campo que tiene fecha de creación de este modelo. Por defecto toma la fecha
    # actual del sistema en UTC.
    # https://docs.python.org/3/library/datetime.html
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # -----------------------------------------------------------------------------------
    def __init__(self, representation=None):
        """ Construye una Prediccion nueva usando su representación REST
        """
        super(Prediction, self).__init__()
        # Modifica estas líneas para que se guarde en la base de datos la representación
        # de una observación de tu modelo.
        # 
        # ** IMPORTANTE: ** Cualquier modificación a las bases de datos requiere eliminar 
        #     el archivo de SQLite3 para que SQL Alchemy pueda reconstruir la base de datos
        self.variable_1 = representation.get('variable_1')
        self.variable_2 = representation.get('variable_2')
        self.variable_3 = representation.get('variable_3')

    # -----------------------------------------------------------------------------------
    def __repr__(self):
        """ Convierte una Predicción a una cadena de texto
        """
        return '<Prediction [{}]: var1={}, var2={}, var3={}, score={}>'.format(
            str(self.prediction_id) if self.prediction_id else 'NOT COMMITED', 
            self.variable_1, self.variable_2, self.variable_3,
            str(self.score) if self.score is not None else 'No calculado'
        )