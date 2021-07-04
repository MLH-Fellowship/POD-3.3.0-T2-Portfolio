#!/bin/sh
flask db migrate
flask db upgrade
gunciorn wsgi:app -w 4 -b 0.0.0.0:80 --capture-out --log-level debug
