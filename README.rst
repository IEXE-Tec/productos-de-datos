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

3. Ubícate en alguna de las versiones dedicadas a cada entregable

   .. code-block:: console

      $ git checkout entregable_n

   Donde ``entregable_n`` es el número de entregable:
   
   * ``entregable_2`` contiene los archivos para integrar tu modelo predictivo
   * ``entregable_3`` contiene los archivos para procesar solicitudes POST al modelo
   * ``entregable_4`` contiene los archivos para procesar solicitudes GET del histórico de predicciones
   * ``entregable_5`` contiene los archivos para actualizar una predicción mediante PUT
   * ``entregable_6`` contiene los archivos para integrar un dashboard simple

***********

Entregable 3
------------

En este entregable debes de procesar solicitudes POST que agreguen una nueva inferencia

Entregable 4
------------

En este entregable debes de procesar solicitudes GET que devuelven la lista de inferencias
históricas que existen en la base de datos.

