#!/bin/bash
cd /home/pi/Prog/django/gesfi
source ../venv_gesfi/bin/activate
gunicorn gesfi.wsgi:application --name "gesfi" \
	--workers=2 \
	--timeout=120 \
	--bind=192.168.3.13:8000 \
	--user="pi" \
	--group="pi"
	
