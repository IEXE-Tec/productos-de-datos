======================================= 
IEXE Tec - Maestría en Ciencia de Datos 
=======================================

Código fuente para crear proyecto de la materia Productos de Datos

Instalación
-----------

1. Descarga este repositorio:

   .. code-block:: console

       $ git clone https://github.com/IEXE-Tec/productos-de-datos.git

2. Crea un ambiente autocontenido:

   .. code-block:: console

      $ python3 -m venv ~/entornos/productos_de_datos/
      $ source ~/entornos/productos_de_datos/bin/activate
      $ pip install -m requirements.txt

3. Ubícate en alguna de las versiones dedicadas a cada entregable:

   .. code-block:: console

      $ git checkout entregable_n

   Donde ``entregable_n`` es el número de entregable:
   
   * ``entregable_2`` contiene los archivos para integrar tu modelo predictivo
   * ``entregable_3`` contiene los archivos para procesar solicitudes POST al modelo
   * ``entregable_4`` contiene los archivos para procesar solicitudes GET del histórico de predicciones
   * ``entregable_5`` contiene los archivos para actualizar una predicción mediante PUT
   * ``entregable_6`` contiene los archivos para integrar un dashboard simple

Ejecución
---------

1. Exporta la variable de entorno ``FLASK_APP``:

   Windows:

   .. code-block:: console

      $ export FLASK_APP=model_api.py

   Linux / Mac:

   .. code-block:: console

      $ set FLASK_APP=model_api.py      

2. Inicia el servidor de pruebas de Flask:

   .. code-block:: console

      $ flask run

   La salida de este comando debe ser algo así::

           * Serving Flask app "model_api.py" (lazy loading)
           * Environment: development
           * Debug mode: on
           * Restarting with stat
           * Debugger is active!
           * Debugger PIN: 216-201-467
           * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

3. Abre un navegador en http://127.0.0.1:5000/. 
   
   Si usas Cloud9 debes de abrir el firewall de AWS. Consulta los manuales de la clase para saber cómo.

4. Lee con cuidado los comentarios del código fuente para modificar cada entrega.
