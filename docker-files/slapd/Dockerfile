FROM nickstenning/slapd:latest
MAINTAINER Sami-Petteri Pukkila

RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive apt-get update -y
RUN LC_ALL=C DEBIAN_FRONTEND=noninteractive apt-get install -y ldap-utils

COPY fixtures.ldif /

RUN mkdir -p /etc/service/setupfixtures
COPY setupfixtures.sh /etc/service/setupfixtures/run
RUN chmod +x /etc/service/setupfixtures/run


RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

