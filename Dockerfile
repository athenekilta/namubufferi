FROM python:alpine

EXPOSE 8080

RUN apk add --no-cache nodejs postgresql-dev curl-dev gcc musl-dev

RUN mkdir /namubufferi
WORKDIR /namubufferi

ADD requirements.txt /namubufferi
RUN pip install -r /namubufferi/requirements.txt

ADD package.json /namubufferi
# Npm fails without --no-optional flag for some reason
RUN npm install --no-optional --unsafe-perm

COPY ./ /namubufferi
RUN /namubufferi/node_modules/.bin/webpack --config /namubufferi/webpack.prod.config.js -p

RUN python3 manage.py collectstatic --noinput

RUN mkdir /static
RUN cp -R namubufferi/staticfiles/* /static/

CMD ["gunicorn", "namubufferi.wsgi", "--name", "namubufferi", "--bind", "0.0.0.0:8080", "--reload", "--log-level=info", "--log-file=-", "--access-logfile=-"]
