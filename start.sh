#!/bin/sh

./manage.py migrate
./manage.py runserver 0:8000
