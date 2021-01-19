# =======================================================================================
#                        IEXE Tec - Maestría en Ciencia de Datos
#                                  Productos de Datos
# ---------------------------------------------------------------------------------------
# Aquí se configura la aplicación de FLASK.
# https://flask.palletsprojects.com/en/1.1.x/config/
# =======================================================================================
import os

class Config(object):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
