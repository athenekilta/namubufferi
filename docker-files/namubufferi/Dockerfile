FROM phusion/baseimage:0.9.19

MAINTAINER Sami-Petteri Pukkila

CMD ["/sbin/my_init"]

RUN apt-get -y update
RUN apt-get install -y python2.7 python-pip gunicorn
RUN apt-get install -y libpq-dev postgresql

RUN mkdir /static

RUN mkdir /etc/service/namubufferi
ADD docker-files/namubufferi/namubufferistart.sh /etc/service/namubufferi/run
RUN chmod +x /etc/service/namubufferi/run

RUN mkdir /namubufferi
ADD requirements.txt /namubufferi
RUN pip install -r /namubufferi/requirements.txt

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./ /namubufferi
ADD docker-files/namubufferi/docker_local_settings.py /namubufferi/namubufferi/local_settings.py
