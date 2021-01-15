#!/bin/sh

python manage.py db upgrade

gunicorn -c g_config.py app:app
