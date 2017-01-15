FROM phusion/baseimage:0.9.19

MAINTAINER Sami-Petteri Pukkila

CMD ["/sbin/my_init"]

RUN apt-get -y update
RUN apt-get install -y python3 python3-pip gunicorn3
RUN apt-get install -y libpq-dev postgresql

RUN mkdir /static

RUN mkdir /etc/service/namubufferi
ADD docker-files/namubufferi/namubufferistart.sh /etc/service/namubufferi/run
RUN chmod +x /etc/service/namubufferi/run

RUN mkdir /namubufferi
ADD requirements.txt /namubufferi
RUN pip3 install -r /namubufferi/requirements.txt

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./ /namubufferi
