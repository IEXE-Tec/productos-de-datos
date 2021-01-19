# =======================================================================================
#                        IEXE Tec - Maestría en Ciencia de Datos
#                                  Productos de Datos
# ---------------------------------------------------------------------------------------
# Configuración de GUnicorn.
# https://docs.gunicorn.org/en/stable/configure.html
# =======================================================================================
import multiprocessing

bind = "0.0.0.0:80"
workers = multiprocessing.cpu_count() * 2 + 1
keep_alive = 5
max_requests = 3
worker_class = "gevent"
