FROM phusion/baseimage:0.9.19

MAINTAINER Sami-Petteri Pukkila

CMD ["/sbin/my_init"]
EXPOSE 8080

RUN apt-get -y update && apt-get install -y python3 python3-pip gunicorn3 npm nodejs-legacy libpq-dev postgresql
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p /static

RUN mkdir /etc/service/namubufferi
ADD docker-files/namubufferi/namubufferistart.sh /etc/service/namubufferi/run
RUN chmod +x /etc/service/namubufferi/run

RUN mkdir /etc/service/namubufferildapsync
ADD docker-files/namubufferi/namubufferiupdateldap.sh /etc/service/namubufferildapsync/run
RUN chmod +x /etc/service/namubufferildapsync/run

RUN mkdir /namubufferi
WORKDIR /namubufferi

ADD requirements.txt /namubufferi
RUN pip3 install -r /namubufferi/requirements.txt

ADD package.json /namubufferi
# Npm fails without --no-optional flag for some reason
RUN npm install --no-optional --unsafe-perm

COPY ./ /namubufferi
# We cant use this as a postinstall hook for npm as we want to copy
# project files after npm install
RUN /namubufferi/node_modules/.bin/webpack --config /namubufferi/webpack.prod.config.js -p
RUN python3 manage.py collectstatic --noinput
RUN rm -rf /namubufferi/node_modules

