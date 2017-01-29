FROM phusion/baseimage:0.9.19

MAINTAINER Sami-Petteri Pukkila

CMD ["/sbin/my_init"]

RUN apt-get -y update
RUN apt-get install -y python3 python3-pip gunicorn3 npm nodejs-legacy
RUN apt-get install -y libpq-dev postgresql

RUN mkdir /static

RUN mkdir /etc/service/namubufferi
ADD docker-files/namubufferi/namubufferistart.sh /etc/service/namubufferi/run
RUN chmod +x /etc/service/namubufferi/run

RUN mkdir /etc/service/namubufferildapsync
ADD docker-files/namubufferi/namubufferiupdateldap.sh /etc/service/namubufferildapsync/run
RUN chmod +x /etc/service/namubufferildapsync/run

RUN mkdir /namubufferi
ADD requirements.txt /namubufferi
RUN pip3 install -r /namubufferi/requirements.txt

ADD package.json /namubufferi
WORKDIR /namubufferi
RUN npm install --no-optional

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./ /namubufferi

