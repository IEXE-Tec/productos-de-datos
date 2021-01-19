# =======================================================================================
#                        IEXE Tec - Maestría en Ciencia de Datos
#                                  Productos de Datos
# ---------------------------------------------------------------------------------------
# En este script se definen los modelos o tablas que van a interactuar con tu la
# base de datos.
# =======================================================================================
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSON
from app import db


# =======================================================================================
class BaseModel:
    """ Modelo base que agrega dos columnas a cada tabla de la base de datos:
            - id: Llave primaria
            - api_id: Indentificador estándar UUID para usar desde el API REST
    """
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)


# =======================================================================================
class PredictionScore(db.Model, BaseModel):
    """ Modelo que almacena en la base de datos el resultado de una llamada al modelo
        predictivo.
        Hereda de dos clases: 
            - db.Model es la clase de la biblioteca de SQLAlchemy que contiene todo lo 
              necesario para interactuar con la base de datos.
            - BaseModel es la clase base del API, agrega las columnas id y api_id
    """

    __tablename__ = 'prediction_score'

    score = db.Column(db.Float, nullable=True)
    # agrega aquí otras propiedades relacionadas con la respuesta de tu modelo

    # -----------------------------------------------------------------------------------
    def __init__(self, score=None):
        """ Constructor
            :param score: El resultado de una llamada al modelo.
        """
        self.score = score

    # -----------------------------------------------------------------------------------
    def __repr__(self):
        """ Genera la representación en string de una instancia de un modelo.
        """
        return f"<Rate {self.id}: {self.score}>"


# =======================================================================================
class PredictionRequest(db.Model, BaseModel):
    """ Llena aquí las propiedades de tu modelo predictivo
    """
    pass
