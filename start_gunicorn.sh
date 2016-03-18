#!/bin/bash
cd /home/pi/Prog/django/gesfi
source ../venv_gesfi/bin/activate
gunicorn gesfi.wsgi:application --name "gesfinancière" \
	--workers=2 \
	--bind=192.168.3.13:8000 \
	--user="www-data" \
	--group="www-data"
	
