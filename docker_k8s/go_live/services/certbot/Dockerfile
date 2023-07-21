FROM alpine:latest

### Environment variables
ENV LANG='en_US.UTF-8' \
    LANGUAGE='en_US.UTF-8' \
    TERM='xterm' 

### Install Application
RUN set -x && \
    apk --no-cache upgrade && \
    apk add --no-cache --virtual=run-deps \
      certbot \
      bash \
    && \
    rm -rf /tmp/* \
           /var/cache/apk/*  \
           /var/tmp/*

EXPOSE 9999
