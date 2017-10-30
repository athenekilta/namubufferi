#!/bin/sh
python3 manage.py migrate
./node_modules/.bin/webpack --config /namubufferi/webpack.config.js
python3 manage.py collectstatic --noinput
