FROM ubuntu:16.04

MAINTAINER Sami-Petteri Pukkila

EXPOSE 8080

RUN apt-get -y update && apt-get install -y python3 python3-pip gunicorn3 npm nodejs-legacy libpq-dev postgresql libcurl4-openssl-dev
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN mkdir /namubufferi
WORKDIR /namubufferi

ADD requirements.txt /namubufferi
RUN pip3 install -r /namubufferi/requirements.txt

ADD package.json /namubufferi
# Npm fails without --no-optional flag for some reason
RUN npm install --no-optional --unsafe-perm

COPY ./ /namubufferi
# We cant use this as a postinstall hook in package.json as we want to copy
# project files after npm install
RUN /namubufferi/node_modules/.bin/webpack --config /namubufferi/webpack.prod.config.js -p

RUN python3 manage.py collectstatic --noinput

RUN mkdir /static
RUN cp -R namubufferi/staticfiles/* /static/

CMD ["gunicorn3", "namubufferi.wsgi", "--name", "namubufferi", "--bind", "0.0.0.0:8080", "--reload", "--log-level=info", "--log-file=-", "--access-logfile=-"]
