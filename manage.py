# =======================================================================================
#                        IEXE Tec - Maestría en Ciencia de Datos
#                                  Productos de Datos
# ---------------------------------------------------------------------------------------
# Punto de entrada a la aplicación. Este script se invoca desde el administrador de 
# aplicaciones -en este caso GUnicorn- para crear una instancia de la aplicación 
# =======================================================================================
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import Config

from app import app, db


app.config.from_object(Config)

migrate = Migrate(app=app, db=db, compare_type=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
